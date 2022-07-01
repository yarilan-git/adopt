"""Models for Blogly."""
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Specie(db.Model):
    __tablename__ = 'specie'

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

    @classmethod
    def initial_setup(self):
        recs = [Specie(name= 'dog'),
                  Specie(name='cat'),
                  Specie(name='bird'),
                  Specie(name='reptile')]
        db.session.add_all(recs)
        db.session.commit()

    id      = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name    = db.Column(db.String(50), nullable=False)

    @classmethod
    def bring_selected_to_top(self, id):
        ordered = []
        selected = Specie.query.get(id)
        ordered.append((selected.id, selected.name))
        
        all= Specie.query.all()
        for specie in all:
                if specie.id != id:
                    ordered.append((specie.id, specie.name))
        return ordered


class Pet(db.Model):
    __tablename__ = 'pet'

    
    
    id          = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name        = db.Column(db.Text, nullable=False)
    specie_id   = db.Column(db.Integer, db.ForeignKey('specie.id'))
    photo_url   = db.Column(db.Text)
    age         = db.Column(db.Integer)
    notes       = db.Column(db.Text)
    available   = db.Column(db.Boolean, nullable=False, default=True)
    specie      = db.relationship('Specie', backref='pets')

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, species: {self.specie_id}, url: {self.photo_url}, age: {self.age}, notes: {self.notes}, available: {self.available}"

    @classmethod
    def get_all_pets(self):
        return Pet.query.all()
    
    def get_pet_info(id):
        return Pet.query.get(id)



    