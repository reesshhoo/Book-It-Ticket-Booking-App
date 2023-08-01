from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bookings = db.relationship('Booking', backref='users', lazy=True)
    # venues = db.relationship('Venue', backref='admins', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    venues = db.relationship('Venue', backref='admin', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venues'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    venue_location = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)

class Show(db.Model):
    __tablename__ = 'shows'
    show_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    seats_booked = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, nullable=False)
    show_screen = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)
    bookings = db.relationship('Booking', backref='show', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
    tickets = db.Column(db.Integer, nullable=False)
