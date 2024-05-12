{
    'name': 'Hotel management - OV',
    'description': 'Manage rooms booking',
    'author': 'onev1rod',
    'version': '17.0.1.0.1',
    'category': 'Industries',
    'sequence': '1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_data_sequence.xml',
        'views/menu.xml',
        'views/room_booking_views.xml',
        'views/hotel_room_views.xml',
        'views/hotel_amenity_views.xml',
        'views/hotel_service_views.xml',
    ],
    'demo': [],
    'images': [],
    'application': 'True',
    'installable': 'True',
    'license': 'LGPL-3',
    'assets': {},
}
