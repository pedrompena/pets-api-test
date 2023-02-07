from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String,  unique=True)
    password = db.Column(db.String)
    avatar = db.Column(db.String)
    description = db.Column(db.String)
    city = db.Column(db.String)

    def __repr__(self):
        return '<Clients %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'avatar': self.avatar,
                'city': self.city,
                'description': self.description}


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'clients.id'), nullable=False)

    def __repr__(self):
        return '<Pets %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'image': self.image,
                'description': self.description,
                'owner_id': self.owner_id}


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    carer_id = db.Column(db.Integer, db.ForeignKey(
        'clients.id'), nullable=False)

    def __repr__(self):
        return '<Services %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'price': self.price,
                'description': self.description,
                'carer_id': self.carer_id}


class Contracts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id'), nullable=False)
    date = db.Column(db.String)
    price = db.Column(db.Integer)
    assessment = db.Column(db.Integer)
    comments = db.Column(db.String)

    def __repr__(self):
        return '<Contracts %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'pet_id': self.pet_id,
                'service_id': self.service_id,
                'date': self.date,
                'price': self.price,
                'assessment': self.assessment,
                'comments': self.comments}


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transmitter_id = db.Column(
        db.Integer, db.ForeignKey('clients.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date = db.Column(db.String)
    content = db.Column(db.String)

    def __repr__(self):
        return '<Messages %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'transmitter_id': self.transmitter_id,
                'receiver_id': self.receiver_id,
                'date': self.date,
                'content': self.content}


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey(
        'clients.id'), nullable=False)
    url = db.Column(db.String)
    alt = db.Column(db.String)
    caption = db.Column(db.String)

    def __repr__(self):
        return '<Images %r>' % self.id

    def serialize(self):
        return {'id': self.id,
                'client_id': self.client_id,
                'url': self.url,
                'alt': self.alt,
                'caption': self.caption}
