from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, time


class RoomBookingLine(models.Model):
    _name = "room.booking.line"
    _description = "Hotel Folio Line"

    room_booking_id = fields.Many2one("room.booking", string="Room Booking")
    hotel_room_id = fields.Many2one("hotel.room", string="Room", required=True)
    room_type = fields.Selection(related="hotel_room_id.room_type", string="Room Type")
    checkin_date = fields.Datetime(string="Check In",
                                   help="You can choose the date,"
                                        " Otherwise sets to current Date",
                                   default=lambda self: self._get_default_check_in(),
                                   required=True)
    checkout_date = fields.Datetime(string="Check Out",
                                    help="You can choose the date,"
                                         " Otherwise sets to current Date",
                                    default=lambda self: self._get_default_check_out(),
                                    required=True)
    uom_qty = fields.Float(string="Duration",
                           compute="_compute_duration", store=True)
    uom_rent = fields.Selection([('day', "Days"), ('hour', "Hours")],
                                string="Unit of Measure", default="day", required=True)
    price_unit = fields.Float(string="Rent", compute="_compute_rent", store=True)
    price_surcharge = fields.Float(string="Surcharge",
                                   compute="_compute_duration", store=True,
                                   readonly=False)
    price_subtotal = fields.Float(string="Subtotal",
                                  compute="_compute_price_total", store=True)
    price_total = fields.Float(string="Total",
                               compute="_compute_price_total", store=True)

    def _set_default_uom_id(self):
        return self.env.ref('uom.product_uom_day')

    def _get_default_check_in(self):
        return datetime.combine(datetime.now().date(), time(5, 0, 0))

    def _get_default_check_out(self):
        check_in = self._get_default_check_in()
        return check_in + timedelta(days=1)

    @api.depends("checkin_date", "checkout_date", "uom_rent", "hotel_room_id")
    def _compute_duration(self):
        for line in self:
            if line.checkin_date > line.checkout_date:
                raise ValidationError(_("Checkout must be greater or equal checkin date"))
            if line.checkin_date and line.checkout_date:
                match line.uom_rent:
                    case "day":
                        diffdate = line.checkout_date - line.checkin_date
                        line.uom_qty = diffdate.days
                        line.price_surcharge = (diffdate.seconds / 3600) * line.hotel_room_id.rent_by_hour
                    case "hour":
                        diffdate = line.checkout_date - line.checkin_date
                        line.uom_qty = diffdate.seconds / 3600
                        line.price_surcharge = 0.0

    @api.depends("hotel_room_id", "uom_rent")
    def _compute_rent(self):
        for line in self:
            match line.uom_rent:
                case "day":
                    line.price_unit = line.hotel_room_id.rent_by_day
                case "hour":
                    line.price_unit = line.hotel_room_id.rent_by_hour

    @api.depends("uom_qty", "price_unit", "price_subtotal", "price_surcharge")
    def _compute_price_total(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.uom_qty
            line.price_total = line.price_subtotal + line.price_surcharge

    @api.constrains('hotel_room_id', 'checkin_date', 'checkout_date')
    def _check_booking_overlap(self):
        for line in self:
            domain = [
                ('hotel_room_id', '=', line.hotel_room_id.id),
                ('id', '!=', line.id),
                '|',
                '&', ('checkin_date', '<=', line.checkin_date), ('checkout_date', '>=', line.checkin_date),
                '&', ('checkin_date', '<=', line.checkout_date), ('checkout_date', '>=', line.checkout_date),
            ]
            overlapping_lines = self.search(domain)
            if overlapping_lines:
                raise ValidationError("The selected room is not available for the chosen dates.")