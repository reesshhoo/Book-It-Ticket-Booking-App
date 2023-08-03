from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from application.models import *
from application.api import *


app = Flask(__name__)
CORS(app)
# Initialising the DB using SQLAlchemy, pushing content to the app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.config['SECRET_KEY'] = '#1010100'
db.init_app(app)
app.app_context().push()
db.create_all()

jwt=JWTManager(app)
app.app_context().push()

api.add_resource(Login_api, "/api/login")
api.add_resource(Register_api, "/api/register")
api.add_resource(Venue_api,"/api/Venues", "/api/Venues/<venue_id>")
api.add_resource(Shows_api, "/api/Shows/<venue_id>","/api/Shows/edit/<show_id>")
api.add_resource(User_api, "/api/User", "/api/User/<show_id>")

# @app.route('/api/Usershows', methods=["GET"])
# @jwt_required()
# def shows():
#     current_user = get_jwt_identity()
#     user = User.query.filter_by(email=current_user).first()
#     if not user:
#         return {'status': False, 'msg': 'User not found'}, 400

#     venues = Venue.query.all()
#     if not venues:
#         return {'status': False, 'msg': 'No venue added yet'},200

#     data = []
#     for v in venues:  # Use 'v' instead of 'venue'
#         shows = Show.query.filter_by(venue_id=v.venue_id).all() 
#         shows_data = []
#         for show in shows:
#             show_data = {
#                 'show_id': show.show_id,
#                 'name': show.name,
#                 'show_datetime': convert_datetime_to_str(show.date_time),
#                 'seats_booked': show.seats_booked,
#                 'seats_available': show.seats_available,
#                 'show_screen': show.show_screen,
#                 'imagefile': show.image,
#                 'price': show.price
#             }
#             shows_data.append(show_data)

#         venue_data = {
#             'venue_id': v.venue_id,  # Use 'v.venue_id' instead of 'venue.venue_id'
#             'name': v.name,  # Use 'v.name' instead of 'venue.name'
#             'venue_location': v.venue_location,  # Use 'v.venue_location' instead of 'venue.venue_location'
#             'admin_id': v.admin_id,  # Use 'v.admin_id' instead of 'venue.admin_id'
#             'shows': shows_data
#         }
#         data.append(venue_data)

#     return {"venues": data}

# @app.route('/api/Usershows/booking/<show_id>', methods=["PUT"])
# @jwt_required()
# def booking(show_id):
#     current_user = get_jwt_identity()
#     user = User.query.filter_by(email=current_user).first()
#     if not user:
#         return {'status': False, 'msg': 'User not found'}, 400

#     s = Show.query.filter_by(show_id=show_id).first()
#     if s is None:
#             {'status': False, 'msg': 'Show not found'}, 400
#     form =request.get_json()
#     tickets = form.get('tickets')
#     if tickets is not None and tickets > 0:
#         if (s.seats_available >= tickets):
#             s.seats_available = s.seats_available - tickets
#             s.seats_booked = s.seats_booked + tickets
#             # db.session.commit()
#             new_booking = Booking(user_id=user.user_id, show_id=s.show_id,tickets=tickets)
#             db.session.add(new_booking)
#             db.session.commit()
#             return {'status': True, 'msg': 'Booking successful'}, 200
#         else:
#             return {'status': False, 'msg': 'Not enough seats available'}, 400
    
#     else:
#         return {'status': False, 'msg': 'Invalid number of tickets'}, 400






if __name__=='__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)

