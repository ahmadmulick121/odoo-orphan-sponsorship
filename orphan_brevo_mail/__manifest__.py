{
    'name': 'Brevo Email Connector',
    'version': '16.0.1.0.0',
    'summary': 'Send emails via Brevo HTTPS API instead of SMTP (bypasses port 587 blocks)',
    'author': 'TeamCoopTech',
    'category': 'Discuss',
    'depends': ['mail'],
    'data': [
        'data/ir_config_parameter.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
