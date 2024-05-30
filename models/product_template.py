from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type_hotel = fields.Selection([('food', 'Food'), ('service', 'Service'), ('vehicle', 'Vehicle')],
                                          string="Product Type for Hotel")
    license_plates = fields.Char(string="License Plates")
    owner = fields.Many2one("res.partner", string="Owner")
