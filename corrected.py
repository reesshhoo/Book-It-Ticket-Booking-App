from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_booking.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)

# Define association tables for many-to-many relationship
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Venue(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    admin = db.relationship('User', backref=db.backref('venues', lazy='dynamic'))


class Show(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    date = db.Column(db.Date())
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.id'))
    venue = db.relationship('Venue', backref=db.backref('shows', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Setup Flask-JWT-Extended
jwt = JWTManager(app)


# API Routes
@app.route('/api/user/signup', methods=['POST'])
def user_signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = user_datastore.create_user(email=email, password=password)
    db.session.commit()

    return jsonify({'message': 'User created successfully.'}), 201


@app.route('/api/user/login', methods=['POST'])
def user_login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = user_datastore.get_user(email)

    if user and user_datastore.verify_password(password, user.password):
        access_token = create_access_token(identity=user.email)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid email or password.'}), 401


@app.route('/api/admin/signup', methods=['POST'])
@roles_required('admin')  # Only users with the 'admin' role can access this endpoint
def admin_signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = user_datastore.create_user(email=email, password=password)
    user_datastore.add_role_to_user(user, 'admin')
    db.session.commit()

    return jsonify({'message': 'Admin created successfully.'}), 201


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = user_datastore.get_user(email)

    if user and user_datastore.verify_password(password, user.password) and 'admin' in [role.name for role in user.roles]:
        access_token = create_access_token(identity=user.email)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid email or password.'}), 401


@app.route('/api/user/profile', methods=['GET'])
@jwt_required()  # Requires a valid access token
def user_profile():
    current_user_email = get_jwt_identity()
    user = user_datastore.get_user(current_user_email)
    return jsonify({'email': user.email, 'roles': [role.name for role in user.roles]}), 200


if __name__ == '__main__':
    db.create_all()
    app.run()
