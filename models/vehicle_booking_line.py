from odoo import models, api, fields, _

class VehicleBookingLine(models.Model):
    _name = "vehicle.booking.line"
    _description = "Vehicle Booking Line"

    room_booking_id = fields.Many2one("room.booking", string="Room Booking")
    vehicle_id = fields.Many2one("product.template", string="Vehicle", required=True, domain=[('product_type_hotel', '=','vehicle')])
    uom_qty = fields.Float(string="Quantity", default=1, required=True)
    price_unit = fields.Float(related="vehicle_id.list_price", string="Unit Price")
    price_total = fields.Float(string="Total", compute="_compute_price")

    @api.depends("uom_qty", "price_unit")
    def _compute_price(self):
        for line in self:
            line.price_total = line.uom_qty * line.price_unit