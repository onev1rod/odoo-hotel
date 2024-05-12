from odoo import models, api, fields, _

class ServiceBookingLine(models.Model):
    _name = "service.booking.line"
    _description = "Service Booking Line"

    room_booking_id = fields.Many2one("room.booking", string="Room Booking")
    hotel_service_id = fields.Many2one("hotel.service", string="Service", required=True)
    unit_price = fields.Float(related="hotel_service_id.price_unit", string="Price", readonly=False)