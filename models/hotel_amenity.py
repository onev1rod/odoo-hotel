from odoo import api, models, fields, _

class HotelAmenity(models.Model):
    _name = "hotel.amenity"
    _description = "Hotel Amenity"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    image_amenity = fields.Image(string="Image", copy=False)
    description = fields.Html(string="About",
                              help="Specify the amenity description")
    color = fields.Integer(string="Color")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _('%s (copy)', self.name)
        return super().copy(default)

    _sql_constraints = [
        ('unique_hotel_amenity', 'unique (name)', 'Name be must unique')
    ]