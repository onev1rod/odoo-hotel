from odoo import api, fields, models, _
from datetime import datetime, time

class SearchAvailableRoom(models.Model):
    _name = "search.available.room"
    _description = "Search for available rooms"

    name = fields.Char(string="", default="Search Available Rooms")
    checkin_date = fields.Datetime(string="Check-in", default=lambda self: self._get_default_check_date())
    checkout_date = fields.Datetime(string="Check-out", default=lambda self: self._get_default_check_date())
    result = fields.Text(string="Result",  readonly=True)

    def _get_default_check_date(self):
        return datetime.combine(datetime.now().date(), time(5, 0, 0))

    # @api.depends("checkin_date", "checkout_date")
    # def _compute_available_rooms(self):
    #     for record in self:
    #         if not record.checkin_date or not record.checkout_date:
    #             record.result = ""
    #             continue
    #
    #         # Access room and booking line models (assuming names)
    #         room_model = self.env['hotel.room']
    #         booking_line_model = self.env['room.booking.line']
    #
    #         # Filter booked rooms based on check-in and check-out dates (inclusive)
    #         overlapping_bookings = booking_line_model.search([
    #             ('checkin_date', '<=', record.checkout_date),
    #             ('checkout_date', '>=', record.checkin_date),
    #         ])
    #
    #         # Get booked room IDs
    #         booked_room_ids = overlapping_bookings.mapped('hotel_room_id.id')
    #
    #         # Find available room IDs (excluding booked rooms)
    #         available_room_ids = list(set(room_model.search([]).ids) - set(booked_room_ids))
    #
    #         # Construct result message
    #         if available_room_ids:
    #             available_rooms = room_model.browse(available_room_ids)
    #             room_names = ', '.join([room.name for room in available_rooms])
    #             record.result = f"Available rooms: {room_names}"
    #         else:
    #             record.result = "No rooms available for these dates."

    def action_search(self):
        self.ensure_one()
        room_booking_model = self.env['room.booking']
        room_booking_line_model = self.env['room.booking.line']

        # Lấy tất cả các đặt phòng trong trạng thái 'reserved' và 'check-in'
        occupied_rooms = room_booking_line_model.search([
            ('checkin_date', '<', self.checkout_date),
            ('checkout_date', '>', self.checkin_date),
        ]).mapped('hotel_room_id.id')

        # Lấy tất cả các phòng còn trống
        available_rooms = self.env['hotel.room'].search([
            ('id', 'not in', occupied_rooms)
        ])

        result = ''
        for room in available_rooms:
            result += f"- {room.name}\n"

        self.result = result