from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type_hotel = fields.Selection([('food', 'Food'), ('service', 'Service')], string="Product Type for Hotel")
