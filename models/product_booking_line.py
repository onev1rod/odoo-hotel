from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ProductBookingLine(models.Model):
    _name = "product.booking.line"
    _description = "Product Booking Line"

    room_booking_id = fields.Many2one("room.booking", string="Room Booking")
    product_id = fields.Many2one("product.template", string="Product", required=True, domain=[('product_type_hotel', 'in', ('food', 'service'))])
    uom_qty = fields.Float(string="Quantity", default=1, required=True)
    price_unit = fields.Float(related="product_id.list_price", string="Unit Price")
    price_total = fields.Float(string="Total", compute="_compute_price")

    @api.depends("uom_qty", "price_unit")
    def _compute_price(self):
        for line in self:
            line.price_total = line.uom_qty * line.price_unit