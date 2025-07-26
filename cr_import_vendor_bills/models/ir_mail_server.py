# -*- coding:utf-8 -*-
import logging
import email
import base64
import pathlib
import zipfile
import io
from lxml import etree
from datetime import datetime
from odoo.addons.cr_electronic_invoice.models.api_facturae import load_xml_data

import re

from odoo import api, fields, models, _
from odoo.tests.common import Form

_logger = logging.getLogger(__name__)

class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    def fetch_mail(self):
        _logger.info("Test from ir.cron")
        res_companies_ids = self.env['res.company'].sudo().search([])
        for res_company_id in res_companies_ids:
            if res_company_id.import_bill_automatic:
                additionnal_context = {'fetchmail_cron_running': True}
                MailThread = self.env['mail.thread']
                server = res_company_id.import_bill_mail_server_id
                additionnal_context['fetchmail_server_id'] = server.id
                additionnal_context['server_type'] = server.server_type

                _logger.info('Start checking for new emails on %s server %s', server.server_type, server.name)
                count, failed = 0, 0
                imap_server = None

                if server.server_type == 'imap':
                    try:
                        imap_server = server.connect()
                        imap_server.select(mailbox=res_company_id.import_bill_folder_import or 'INBOX')
                        result, data = imap_server.search(None, '(UNSEEN)')
                        if not data[0]:
                            _logger.info("Empty Folder (Stop Execute)")
                            return
                        for num in data[0].split():
                            result, data = imap_server.fetch(num, '(RFC822)')
                            imap_server.store(num, '-FLAGS', '\\Seen')
                            message = data[0][1]
                            try:
                                if isinstance(message, str):
                                    message = message.encode('utf-8')
                                message = email.message_from_bytes(message, policy=email.policy.SMTP)
                                msg = MailThread.message_parse(message, save_original=False)

                                _logger.info("------ Process Message --------")
                                _logger.info("Subject : %s ", msg.get('subject', ''))
                                _logger.info("From: %s ", msg.get('from', ''))
                                _logger.info("To: %s ", msg.get('to', ''))

                                result = self.create_invoice_with_attamecth(msg, res_company_id)
                                if result and not isinstance(result, bool):
                                    if not server.original:
                                        imap_server.store(num, '+FLAGS', '\\Deleted')
                                    _logger.info("Invoice created correctly %s", str(result))
                                elif result:
                                    if not server.original:
                                        imap_server.store(num, '+FLAGS', '\\Deleted')
                                    _logger.info("Repeated Invoice")
                                else:
                                    _logger.info("Ignore email")
                            except Exception as e:
                                _logger.exception("Failed to process mail.")
                                failed += 1
                            imap_server.store(num, '+FLAGS', '\\Seen')
                            self._cr.commit()
                            count += 1
                            _logger.info("------ End Process Message -------")

                        _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.server_type, server.name, (count - failed), failed)
                    except Exception as e:
                        _logger.exception("General failure when trying to fetch mail.")
                    finally:
                        if imap_server:
                            try:
                                moves_to_delete = self.env['account.move'].search([
                                    ('partner_id', '=', False),
                                    ('ref', '=', False),
                                    ('state', '=', 'draft'),
                                    ('move_type', '=', 'in_invoice'),
                                    ('line_ids', '=', False),
                                ])
                                _logger.info('Se encontraron %d documentos creados erroneamente, se eliminarán.', len(moves_to_delete))
                                moves_to_delete.unlink()
                            except Exception:
                                _logger.warning("Error al eliminar facturas incorrectas. Se intentará en la próxima ejecución.")

                            imap_server.close()
                            imap_server.logout()
                    server.write({'date': fields.Datetime.now()})
                else:
                    _logger.info("Only Support for IMAP Server")
                    server.write({'date': fields.Datetime.now()})
                    return super(FetchmailServer, self).fetch_mail()

    @staticmethod
    def is_xml_file_in_attachment(attach):
        file_name = attach.fname or 'item.ignore'
        return pathlib.Path(file_name.upper()).suffix == '.XML'

    def get_bill_exist_or_false(self, invoice_xml):
        namespaces = invoice_xml.nsmap
        inv_xmlns = namespaces.pop(None)
        namespaces['inv'] = inv_xmlns
        electronic_number = invoice_xml.xpath("inv:Clave", namespaces=namespaces)[0].text
        domain = [('number_electronic', '=', electronic_number)]
        return self.env['account.move'].search(domain, limit=1)

    def create_ir_attachment_invoice(self, invoice, attach, mimetype):
        content = attach['content']
        if isinstance(content, str):
            content = content.encode('utf-8')
        return self.env['ir.attachment'].create({
            'name': attach['fname'],
            'type': 'binary',
            'datas': base64.b64encode(content),
            'store_fname': attach['fname'],
            'res_model': 'account.move',
            'res_id': invoice.id,
            'mimetype': mimetype
        })

    def extract_attachments_from_zip(self, content):
        attachments = []
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            for file_info in z.infolist():
                with z.open(file_info) as file:
                    attachments.append({
                        'fname': file_info.filename,
                        'content': file.read()
                    })
        return attachments

    def create_invoice_with_attamecth(self, msg, company_id):
        attachments = []

        for attach in msg.get('attachments'):
            fname = attach.fname or 'item.ignore'
            suffix = pathlib.Path(fname.lower()).suffix
            if suffix == '.zip':
                try:
                    content = attach.content if isinstance(attach.content, bytes) else attach.content.encode('utf-8')
                    extracted = self.extract_attachments_from_zip(content)
                    attachments.extend(extracted)
                    _logger.info("Archivo ZIP extraído: %s", fname)
                except Exception as e:
                    _logger.warning("Error al extraer ZIP %s: %s", fname, e)
            else:
                attachments.append({
                    'fname': fname,
                    'content': attach.content,
                })

        for attach in attachments:
            if pathlib.Path(attach['fname'].upper()).suffix != '.XML':
                continue
            try:
                attachencode = base64.encodebytes(attach['content']) if isinstance(attach['content'], bytes) else base64.encodebytes(attach['content'].encode('utf-8'))
                invoice_xml = etree.fromstring(base64.b64decode(attachencode))
                match = re.search('FacturaElectronica|NotaCreditoElectronica|NotaDebitoElectronica|TiqueteElectronico|MensajeHacienda', invoice_xml.tag)
                if not match:
                    _logger.info("Documento con etiqueta desconocida: %s", invoice_xml.tag)
                    continue
                document_type = match.group(0)

                if document_type == 'TiqueteElectronico':
                    _logger.info("Este es un Tiquete Electronico no válido para impuestos.")
                    continue

                exist_invoice = self.get_bill_exist_or_false(invoice_xml)

                if document_type == 'MensajeHacienda' and exist_invoice:
                    attachment_id = self.create_ir_attachment_invoice(exist_invoice, attach, 'application/xml')
                    exist_invoice.message_post(attachment_ids=[attachment_id.id])
                    _logger.info('Mensaje Hacienda agregado a factura existente.')
                    return exist_invoice

                if document_type in ['FacturaElectronica', 'NotaCreditoElectronica'] and exist_invoice:
                    _logger.info("Factura duplicada (%s), se ignorará.", exist_invoice.ref)
                    return True

                type_invoice = 'in_invoice' if document_type in ['FacturaElectronica', 'NotaDebitoElectronica'] else 'in_refund'

                self = self.with_context(
                    default_journal_id=company_id.import_bill_journal_id.id,
                    default_move_type='in_invoice',
                    move_type=type_invoice,
                    journal_type='purchase',
                    default_payment_methods_id=1
                )

                invoice_form = Form(self.env['account.move'].with_context(default_payment_methods_id=1), view='account.view_move_form')
                invoice_form._values['payment_methods_id'] = 1
                invoice_form._values['move_type'] = type_invoice
                invoice = invoice_form.save()

                invoice.fname_xml_supplier_approval = attach['fname']
                content_supplier_approval = attach['content']
                if isinstance(content_supplier_approval, str):
                    content_supplier_approval = content_supplier_approval.encode('utf-8')
                invoice.xml_supplier_approval = base64.encodebytes(content_supplier_approval)

                load_xml_data(
                    invoice, True,
                    company_id.import_bill_account_id,
                    company_id.import_bill_product_id,
                    company_id.import_bill_account_analytic_id
                )

                list_attachment = [self.create_ir_attachment_invoice(invoice, attach, 'application/xml').id]
                for a in attachments:
                    suffix = pathlib.Path(a['fname'].upper()).suffix
                    if suffix == '.XML':
                        invoice_xml = etree.fromstring(a['content'])
                        if re.search('MensajeHacienda', invoice_xml.tag):
                            list_attachment.append(self.create_ir_attachment_invoice(invoice, a, 'application/xml').id)
                    elif suffix == '.PDF':
                        list_attachment.append(self.create_ir_attachment_invoice(invoice, a, 'application/pdf').id)

                invoice.message_post(attachment_ids=list_attachment)
                return invoice
            except Exception as e:
                _logger.warning("Error procesando archivo XML: %s", e)
                continue
        return False
