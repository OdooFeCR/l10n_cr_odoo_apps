/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";


patch(PaymentScreen.prototype, {
    shouldDownloadInvoice() {
        return false;
    },
    async validateOrder(isForceValidate) {
         // Get the selected order
        const order = this.pos.get_order();
         // Verifica si la configuración de la compañía tiene factura_electronica en true
        if (this.pos.company.invoice_is_electronic) {
            if (order){
                order.to_invoice = true;
                const partner_domain = order.get_partner() === null ? [["id", "=", this.pos.config.default_partner_id[0]]] : [["id", "=", order.get_partner().id]]; 
                const checkPartner  = await this.pos.orm.call(
                    "res.partner",
                    "search_read",
                    [],
                    {
                      domain: partner_domain,
                      fields: ["id", "name", "inscribed"]
                    }
                ).then(function(result){return result;});
                if (order.get_partner() === null) {
                    order.set_partner(checkPartner[0]);
                }
                //Valida si el cliente tiene estado 'Inscrito' en hacienda para emitir Factura Electronica.
                order.set_tipo_documento(checkPartner[0].inscribed ? "FE" : "TE");
                order.set_journal_id(this.pos.config.invoice_journal_id[0])
                
                if (order.get_number_electronic() === null){
                    const electronic_number = await order.generate_number_electronic(order.get_tipo_documento());
                    order.set_number_electronic(electronic_number);
                }
            }
        }
        await super.validateOrder(...arguments);
    },
    
});
