from odoo import api, models, fields, _

class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = "Hotel Room"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    image_room = fields.Image(string="Image", store=True)
    rent_by_day = fields.Float(string="Rent By Day", help="The rent of the room by days", tracking=True)
    rent_by_hour = fields.Float(string="Rent By Hour", help="The rent of the room by hours", tracking=True)
    room_type = fields.Selection([('single', "Single"),('double', "Double"), ('dormitory', "Dormitory")],
                                 string="Room Type", required=True,
                                 help="Automatically selects the Room Type",
                                 tracking=True, default="single")
    number_of_persons = fields.Integer(string="Max Number Of Persons", required=True,tracking=True)
    room_amenities_ids = fields.Many2many("hotel.amenity", string="Room Amenities")
