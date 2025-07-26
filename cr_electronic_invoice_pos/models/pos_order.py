# Module refactored by @jartavia05 to be used with version 17.0
import logging
from odoo import models, fields, api, _
from threading import Lock
lock = Lock()

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _name = "pos.order"
    _inherit = ["pos.order"]

    tipo_documento = fields.Selection(
        selection=[
            ('FE', 'Electronic Invoice'),
            ('TE', 'Electronic Ticket'),
            ('NC', 'Electronic Credit Note')
            ],
        string="Receipt Type",
        default='TE',
        help='Show document type in concordance with Ministerio de Hacienda classification')
    payment_methods_id = fields.Many2one(
        comodel_name="payment.methods",
        string="Payment methods"
    )
    number_electronic = fields.Char(string="Electronic Number", copy=False, index=True)
    sequence = fields.Char(string='Consecutive', readonly=True)
    journal_id = fields.Char(string='Journal ID',copy=False)

    def _prepare_invoice_vals(self):
        """Override to include custom fields in account.move."""
        vals = super()._prepare_invoice_vals()
        journal = self.session_id.config_id.invoice_journal_id
        if not journal or journal.type != 'sale':
            raise ValueError("The selected journal is not a sales journal. Please check POS settings.")
        
        # Obtener la secuencia de facturación del diario
        if journal.FE_sequence_id or journal.TE_sequence_id:
            if self.tipo_documento == 'FE':
                sequence = journal.FE_sequence_id.next_by_id()
            elif self.tipo_documento == 'TE':
                sequence =  journal.TE_sequence_id.next_by_id()
        else:
            raise ValidationError(_("The selected journal does not have an assigned sequence."))

        vals.update({
            'journal_id': journal.id,  # Set the correct sales journal.
            'tipo_documento': self.tipo_documento,
            'sequence': self.number_electronic[21:41],
            'number_electronic': self.number_electronic,
            'name': self.number_electronic[21:41],
            'payment_methods_id': self.payment_ids.mapped('payment_method_id').account_payment_method_id.id if len(self.payment_ids.mapped('payment_method_id').account_payment_method_id) == 1 else self.payment_ids.mapped('payment_method_id').account_payment_method_id[0].id
        })
        return vals
   
   
    def _order_fields(self, ui_order):
        vals = super()._order_fields(ui_order)
        _logger.info("DATOS EN ORDER FIELDS")
        _logger.info(ui_order)
        vals['tipo_documento'] = ui_order.get('tipo_documento')
        vals['sequence'] = ui_order.get('sequence')
        vals['number_electronic'] = ui_order.get('number_electronic')
        return vals

    
