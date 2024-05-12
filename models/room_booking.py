from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RoomBooking(models.Model):
    """Model that handles the hotel room booking and all operations related
     to booking"""
    _name = "room.booking"
    _description = "Hotel Room Reservation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 required=True, tracking=True)
    order_date = fields.Datetime(string="Order Date",
                                 help="Date of Order",
                                 required=True, tracking=True,
                                 default=fields.Datetime.now())
    checkin_date = fields.Datetime(string="Check In",
                                   help="Date of Checkin",
                                   default=fields.Datetime.now())
    number_of_persons = fields.Integer(string="Number Of Persons", default=1, required=True, tracking=True)
    need_service = fields.Boolean(string="Need Service", default=False)
    need_food = fields.Boolean(string="Need Food", default=False)
    state = fields.Selection(selection=[('draft',"Draft"),
                                        ('reserved',"Reserved"),
                                        ('check-in',"Check-In"),
                                        ('check-out',"Check-Out"),
                                        ('done', "Done"),
                                        ('cancel', "Cancelled")],
                             string="Status", default='draft',
                             required=True, tracking=True)
    room_booking_line_ids = fields.One2many("room.booking.line","room_booking_id",
                                            string="Room Booking Line")
    service_booking_line_ids = fields.One2many("service.booking.line","room_booking_id",
                                            string="Service Booking Line")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('room.booking')
        return super().create(vals_list)

    @api.onchange('need_service')
    def _onchange_need_service(self):
        if not self.need_service and self.service_booking_line_ids:
            for serv in self.service_booking_line_ids:
                serv.unlink()

    # @api.onchange('need_food')
    # def _onchange_need_food(self):
    #     if not self.need_food:
    #         self.unlink()





    def action_reserve(self):
        for record in self:
            record.state = 'reserved'

    def action_checkin(self):
        for rec in self:
            rec.state = 'check-in'

    def action_checkout(self):
        for rec in self:
            rec.state = 'check-out'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'