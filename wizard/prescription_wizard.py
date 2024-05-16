from odoo import models, fields

class PrescriptionWizard(models.TransientModel):
    _name = "prescription.wizard"
    _description = "Open Prescription Wizard"

    product_id = fields.Many2one('product.product', string="Medicine")
    dosage = fields.Char(string="Specify Dosage")
    appointment_id = fields.Many2one('patient.appointment', string="Appointment") #use of this field?
    treatment_id = fields.Many2one('appointment.lines', string="Treatment") #use of this field?

    def action_submit(self):
        if self.appointment_id:
            prescription_line = {
                'product_id': self.product_id.id,
                'dosage': self.dosage,
                'appointment_id': self.appointment_id.id,
            }
            self.env['prescription.lines'].create(prescription_line)
            self.treatment_id.in_prescription = True
        return {'type': 'ir.actions.act_window_close'} #close window after completing the action
            