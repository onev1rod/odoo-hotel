from odoo import api, models, fields
from datetime import date, datetime

class CancelRoomBookingWizard(models.TransientModel):
    _name = "cancel.room.booking.wizard"
    _description = "Cancel Room Booking Wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    room_booking_id = fields.Many2one("room.booking", string="Room Booking", readonly=True)
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date", default=datetime.now(), readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get('active_id'):
            res['room_booking_id'] = self.env.context.get('active_id')
        return res

    def action_cancel(self):
        for rec in self:
            reason_text = "Cancellation date: " + rec.date_cancel.strftime("%d-%m-%Y") + "\nCancellation Reason: " + rec.reason
            rec.room_booking_id.message_post(body=reason_text)
            rec.room_booking_id.state = 'cancel'