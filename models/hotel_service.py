from odoo import api, models, fields

class HotelService(models.Model):
    _name = "hotel.service"
    _description = "Hotel Service"

    name = fields.Char(string="Service", required=True)
    price_unit = fields.Float(string="Price", default=0.0)