{
    'name': 'Doctor Appointment',
    'author': 'Nidal SJ',
    'category': 'Health',
    'summary': 'Manage Doctors and Patients',
    'license': 'LGPL-3',
    'version': '1.0',
    'depends': ['base', 'hr', 'stock', 'report_xlsx'], 
    'data':[
        'security/ir.model.access.csv',
        'views/doctor_view.xml',
        'views/menu.xml',
        'wizard/add_to_prescription.xml',
        'report/prescription_report_template.xml',
        'report/prescription_report_views.xml',
        'data/header.xml',
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
}
