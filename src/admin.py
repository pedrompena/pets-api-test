import os
from flask_admin import Admin
from models import db, Clients, Pets, Services, Contracts, Messages, Images
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')


    admin.add_view(ModelView(Clients, db.session))
    admin.add_view(ModelView(Pets, db.session))
    admin.add_view(ModelView(Services, db.session))
    admin.add_view(ModelView(Contracts, db.session))
    admin.add_view(ModelView(Messages, db.session))
    admin.add_view(ModelView(Images, db.session))

