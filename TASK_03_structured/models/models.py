from extensions import db

# Define the association table for the many-to-many relationship
movie_cast = db.Table('movie_cast',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('cast_member_id', db.Integer, db.ForeignKey('cast_member.id'))
)

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    movies = db.relationship('Movies', backref='director')

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    release_date = db.Column(db.String(11))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    cast = db.Column(db.String(225))

    cast_members = db.relationship('CastMember', secondary=movie_cast, back_populates='movies')

class CastMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movies', secondary=movie_cast, back_populates='cast_members')