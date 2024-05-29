from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RoomBooking(models.Model):
    """Model that handles the hotel room booking and all operations related
     to booking"""
    _name = "room.booking"
    _description = "Hotel Room Reservation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(string="Name", readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 required=True, tracking=True, copy=False)
    order_date = fields.Datetime(string="Order Date",
                                 help="Date of Order",
                                 default=fields.Datetime.now(),
                                 required=True, tracking=True, readonly=True, copy=False)
    number_of_persons = fields.Integer(string="Number Of Persons", default=1, required=True, tracking=True)
    need_service = fields.Boolean(string="Need Service", default=False, copy=False)
    need_food = fields.Boolean(string="Need Food", default=False, copy=False)
    need_vehicle = fields.Boolean(string="Need Vehicle", default=False, copy=False)
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
    product_booking_line_ids = fields.One2many("product.booking.line", "room_booking_id",
                                               string="Product Booking Line")
    service_booking_line_ids = fields.One2many("service.booking.line","room_booking_id",
                                            string="Service Booking Line")
    vehicle_booking_line_ids = fields.One2many("vehicle.booking.line", "room_booking_id",
                                               string="Vehicle Booking Line")


    # Override Create Method to generate sequential values
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('room.booking')
        return super().create(vals_list)

    # Override Unlink Method
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You cannot delete a booking with 'Done' status"))
        return super().unlink()

    @api.onchange('need_service')
    def _onchange_need_service(self):
        if not self.need_service and self.service_booking_line_ids:
            for serv in self.service_booking_line_ids:
                serv.unlink()

    @api.onchange('need_food')
    def _onchange_need_food(self):
        if not self.need_food and self.product_booking_line_ids:
            for serv in self.product_booking_line_ids:
                serv.unlink()

    @api.onchange('need_vehicle')
    def _onchange_need_food(self):
        if not self.need_vehicle and self.vehicle_booking_line_ids:
            for serv in self.vehicle_booking_line_ids:
                serv.unlink()

    # Button type Object
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

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
