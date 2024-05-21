from odoo import api, models, fields, _

class HotelAmenity(models.Model):
    _name = "hotel.amenity"
    _description = "Hotel Amenity"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    image_amenity = fields.Image(string="Image")
    description = fields.Html(string="About",
                              help="Specify the amenity description")
    color = fields.Integer(string="Color")