from odoo import models, api, fields, _

class ServiceBookingLine(models.Model):
    _name = "service.booking.line"
    _description = "Service Booking Line"

    room_booking_id = fields.Many2one("room.booking", string="Room Booking")
    service_id = fields.Many2one("product.template", string="Service", required=True,
                                 domain=[('product_type_hotel', '=', 'service')])
    uom_qty = fields.Float(string="Quantity", default=1, required=True)
    price_unit = fields.Float(related="service_id.list_price", string="Unit Price")
    price_total = fields.Float(string="Total", compute="_compute_price")

    @api.depends("uom_qty", "price_unit")
    def _compute_price(self):
        for line in self:
            line.price_total = line.uom_qty * line.price_unit