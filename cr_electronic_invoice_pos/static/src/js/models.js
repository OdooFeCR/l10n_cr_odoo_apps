/** @odoo-module alias=cr_electronic_invoice_pos.models **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

console.log("POS Factura Electrónica");

patch(Order.prototype, {
  setup() {
    super.setup(...arguments);
    this.tipo_documento = "TE";
    this.number_electronic = null;
    this.sequence = null;
    this.journal_id = null;
    
  },
  
  // Override init_from_JSON to load the field
  init_from_JSON(json) {
    super.init_from_JSON(...arguments); 
    this.number_electronic = json.number_electronic || null;
    this.tipo_documento = json.tipo_documento || null;
    this.sequence = json.sequence || null;
    this.journal_id = json.journal_id || null;
    
  },

  // Override export_as_JSON to save the field
  export_as_JSON() {
    const json = super.export_as_JSON(...arguments);
    json.number_electronic = this.number_electronic;
    json.tipo_documento = this.tipo_documento;
    json.sequence = this.sequence;
    json.journal_id = this.journal_id;
    
    return json;
  },
  
  // Override export_for_printing to save the new fields to be used in the Order Receipt. 
  export_for_printing() {
    const json = super.export_for_printing(...arguments);
    json.headerData.number_electronic = this.number_electronic;
    json.headerData.tipo_documento = this.tipo_documento;
    json.headerData.partner = this.get_partner() || false;

    return json;
  },

  // Add a method to update the tipo_documento field  
  set_tipo_documento(tipoDoc) {
    this.tipo_documento = tipoDoc;
  },
  get_tipo_documento() {
    return this.tipo_documento;
  },

  // Add a method to update the number_electronic field
  set_number_electronic(number) {
    this.number_electronic = number;
  },
  get_number_electronic() {
      return this.number_electronic;
  },

  // Add a method to update the journal_id field
  set_sequence(number) {
    this.sequence = number;
  },
  get_sequence() {
      return this.sequence;
  },

  // Add a method to update the journal_id field
  set_journal_id(number) {
    this.journal_id = number;
  },
  get_journal_id() {
      return this.journal_id;
  },

  async generate_number_electronic() {    
    
    // Getting the journal data in a variable journal_data.
    try {        
      const journal_domain = [["id", "=", this.journal_id]];  
      const journal_data = await this.pos.orm.call(
            "account.journal",
            "search_read",
            [],
            {
              domain: journal_domain,
              fields: ["sucursal", "terminal", "FE_sequence_id", "TE_sequence_id"]
            }
      ).then(function(result){return result;});
      const seq_id = this.tipo_documento === "FE" ? journal_data[0].FE_sequence_id : journal_data[0].TE_sequence_id;
      const seq_domain = [["id", "=", seq_id[0]]];  
      const seq_data = await this.pos.orm.call(
            "ir.sequence",
            "search_read",
            [],
            {
              domain: seq_domain,
              fields: ["name", "id", "number_next_actual", "prefix", "suffix", "number_increment", "padding"]
            }
      ).then(function(result){return result;});
      const idict = {
        year: luxon.DateTime.local().toFormat("yyyy"),
        month: luxon.DateTime.local().toFormat("MM"),
        day: luxon.DateTime.local().toFormat("dd"),
        y: luxon.DateTime.local().toFormat("yy"),
        h12: luxon.DateTime.local().toFormat("hh"),
      };
    
      function pad(n, width, z) {
        z = z || "0";
        n = n + "";
        return n.length < width ? new Array(width - n.length + 1).join(z) + n : n;
      };
      
      const vat = this.pos.company.vat
      const num = seq_data[0].number_next_actual
      const tipo_doc = this.tipo_documento === "FE" ? "01" : "04";
      const num_consecutivo = pad(journal_data[0].sucursal,3)+pad(journal_data[0].terminal,5)+tipo_doc+pad(num, seq_data[0].padding);
      const prefix = "506"+idict['day']+idict['month']+idict['y']+pad(vat,12);
      const suffix = "1"+idict['h12']+idict['day']+idict['month']+idict['y'];
      return prefix + num_consecutivo + suffix;
    
    } catch (error){
      console.error("Error fetching the sequence id:", error);
      return null;
    }

    
  }
});