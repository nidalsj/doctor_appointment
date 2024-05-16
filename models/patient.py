from odoo import api, models, fields


class PatientAppointment(models.Model):
    _name = "patient.appointment"
    _description = "Manage Patient Appointments"

    patient_id = fields.Many2one('res.partner', string="Patient")
    appointment_date = fields.Datetime(string="Appointment Date")
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    appointment_type = fields.Selection([
        ('checkup', 'Checkup'),
        ('treatment', 'Treatment'),
        ('consultation', 'Consultation')],
        string='Appointment Type')
    prescription = fields.Text(string="Prescription")
    pharmacy_line_ids = fields.One2many('appointment.lines', 'appointment_id', string="Pharmacy Lines") #use of appointent_id?
    prescription_line_ids = fields.One2many('prescription.lines', 'appointment_id', string="Prescription Lines") 
    grand_total = fields.Float(compute="_compute_grand_total", string="Grand Total")


    @api.depends('pharmacy_line_ids.total_price')
    def _compute_grand_total(self):
        for appointment in self:
            appointment.grand_total = sum(appointment.pharmacy_line_ids.mapped('total_price'))
    

    # EXCEL SHEET OBJECT BUTTON FUNCTION
    def patient_report_sheet(self):
        pass

    
# TABLE FOR TREATMENTS PAGE - INVENTORY MODULE - UNIT PRICE - GRAND TOTAL
class AppointmentLines(models.Model):
    _name = "appointment.lines"
    _description = "Appointment Lines"

    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Integer(string="Quantity", default="1")
    unit_price = fields.Float(related='product_id.list_price', string="Unit Price")
    total_price = fields.Float(compute="_compute_total", string="Total Price")
    appointment_id = fields.Many2one('patient.appointment', string="Appointment")
    in_prescription = fields.Boolean(string="In Prescription", default=False) 


    @api.depends('qty', 'unit_price')
    def _compute_total(self):
        for line in self:
            line.total_price = line.qty * line.unit_price


    # FUNCTION TO OPEN WIZARD - TAKING DEFAULT VALUES ON CONTEXT    
    def addto_prescription(self):
        return {
            'name': 'Add Medicine to Prescription',
            'view_mode': 'form',
            'res_model': 'prescription.wizard',          
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_product_id':self.product_id.id,
                'default_appointment_id':self.appointment_id.id,
                'default_treatment_id':self.id,
            }
        }
    

    # REMOVING PRODUCT FROM PRESCRIPTION PAGE
    def removefrom_prescription(self):
        find_id = self.env['prescription.lines'].search([('appointment_id','=',self.appointment_id.id),
                                                         ('product_id','=',self.product_id.id)])
        find_id.unlink()
        self.in_prescription = False
        
# TABLE FOR NEW PRESCRIPTION PAGE ON FORM VIEW NOTEBOOK
class PrescriptionLines(models.Model):
    _name = "prescription.lines"    
    _description = "Prescribed Medicines"

    product_id = fields.Many2one('product.product', required=True)
    appointment_id = fields.Many2one('patient.appointment', string="Appointment")
    treatment_id = fields.Many2one('appointment.lines', string="Treatment")
    dosage = fields.Char(string="Dosage")
    
       