
{
    'name': "Real Estate DX4 | Property Management System",
    'version': '17.0.1.0',  # Update version to reflect Odoo 17
    'sequence': 1,
    'summary': """
            Real estate system manages viewing, brochures, auctions, mapping, commissions, reporting, invoicing, payments, blacklist.
        """,
    'description': """
            Real Estate Management System
        """,
    'author': 'GeekXDigital',
    'maintainer': 'GeekXDigital',
    'price': '50.0',
    'currency': 'USD',
    'website': 'https://www.geekxdigital.com/',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'sale_management',
        'website',
        'base_geolocalize',
        'web',
        'sale',
        'board',
    ],
    'data': [
        'security/user_groups.xml',
        'security/property_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/real_estate_management_data.xml',
        'data/ir_cron_data.xml',
        'views/property_property_views.xml',
        'views/property_facility_views.xml',
        'views/property_tag_views.xml',
        'views/property_search_pannel_views.xml',  # Typo fix: "pannel" -> "panel" (optional)
        'views/property_templates.xml',
        'views/property_commision_views.xml',  # Typo fix: "commision" -> "commission" (optional)
        'views/property_sale_views.xml',
        'views/property_rental_views.xml',
        'views/res_partner_views.xml',
        'views/rental_bill_views.xml',
        'views/property_auction_views.xml',
        'views/sales_dashboard.xml',
        'reports/property_sale_report.xml',
        'reports/property_report.xml',
        'wizards/property_sale_report_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'real_estate_management/static/src/js/property_website.js',
            'real_estate_management/static/src/js/property_item.js',
        ],
        'web.assets_backend': [
            'real_estate_management/static/src/components/**/*.js',
            'real_estate_management/static/src/components/**/*.xml',
            'real_estate_management/static/src/components/**/*.scss',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js',
            '/real_estate_management/static/src/js/sales_dashboard.js',
        ],
    },
    'demo': [],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
