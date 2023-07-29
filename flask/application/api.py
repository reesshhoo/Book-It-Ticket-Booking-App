from flask_restful import Resource, fields
from .models import *
# import datetime
from flask import request, jsonify
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime


# <---------------------------------------------------Helper Functions------------------------->

def is_screen_available(venue_id, show_screen, date_time):
    print(date_time, type(date_time))
    
    print(date_time)
    overlapping_show = Show.query.filter(
        Show.venue_id == venue_id,
        Show.show_screen== show_screen,
        Show.date_time >= date_time,
        Show.date_time < date_time + timedelta(hours=3)  # Assuming shows are 3 hours long
    ).first()
    return overlapping_show is None
#<--------------------------------------------------- LOGIN/SIGNUP API --------------------------------------------------------->

class Login_api(Resource):
    def post(self):
        form = request.get_json()
        email = form.get('email')
        password = form.get('password')
        role = form.get('role')
        if role=='admin':
            admin = Admin.query.filter_by(email=email).first()
            if admin is not None and check_password_hash(admin.password, password):
                admin_name = admin.name
                access_token = create_access_token(identity=email,expires_delta=timedelta(days=3))
                return {'status': True,'access_token':access_token, 'name':admin_name},200
        else:
            user = User.query.filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                username = user.name
                access_token = create_access_token(identity=email,expires_delta=timedelta(days=3))
                return {'status': True,'access_token':access_token, 'name':username},200
        
        return {'status':False,'msg': 'Username or password is incorrect'}, 400
        
class Register_api(Resource):
    def post(self):
        form= request.get_json()
        email = form.get('email')
        password= form.get('password')
        name = form.get('name')
        role = form.get('role')
        if role=='admin':
            alreadyexists = Admin.query.filter_by(email=email).first()
            if alreadyexists is None:
                hashed_password = generate_password_hash(password)
                new_admin = Admin(email=email, password=hashed_password,name=name)
                db.session.add(new_admin)
                db.session.commit()
                access_token = create_access_token(identity=email,expires_delta=timedelta(days=3))
                return {'status': True,'access_token':access_token},200
        else:
            alreadyexists = User.query.filter_by(email=email).first()
            if alreadyexists is None:
                hashed_password = generate_password_hash(password)
                new_admin = User(email=email, password=hashed_password,name=name)
                db.session.add(new_admin)
                db.session.commit()
                access_token = create_access_token(identity=email,expires_delta=timedelta(days=3))
                return {'status': True,'access_token':access_token},200
        
        return {'status': False, 'msg': 'An account with the same Email already exists'}, 400
        

#<-------------------------------------------ADMIN VENUE API----------------------------------------------------------------->

class Venue_api(Resource):

    @jwt_required()
    def get(self):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin :
            return {'status': False, 'msg' : 'User not found'}, 400
        
        venue = Venue.query.filter_by(admin_id=admin.admin_id).all()
        if len(venue)==0:
            return {'status':False, 'msg':'No venue added yet'}
        else:
            
            venues = []
            # print(screens)
            for v in venue:
                shows = list(Shows_api.get(self, venue_id=v.venue_id))
                try:
                    shows = list(Shows_api.get(self, venue_id=v.venue_id))
                    if isinstance(shows, dict) and shows.get('status') is False:
                        shows = []  # Empty list when the API returns a 400 status code
                except:
                    shows = []
                
                venue_data = {
                    'venue_id': v.venue_id,
                    'name': v.name,
                    'admin_id': v.admin_id,
                    'shows' : shows
                }
                venues.append(venue_data)
            return {"venues": venues}
    
    @jwt_required()
    def post(self):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin :
            return {'status': False, 'msg' : 'User not found'}, 400
        # print("testing post method")
        # return "",200
        form = request.get_json()
        venue_name = form.get('name')
        if venue_name is not None:
            new_venue = Venue(name=venue_name, admin_id=admin.admin_id)
            print()
            db.session.add(new_venue)
            db.session.commit()
            return {'status': True, 'msg':'New Venue added Succesfully', 'venue_id': new_venue.venue_id, 'admin_id': new_venue.admin_id}, 200
        else:
            return {'status': False, 'msg': 'Invalid request'}, 400
        
    @jwt_required()
    def put(self, venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        venue = Venue.query.filter_by(venue_id=venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        form = request.get_json()
        venue_name = form.get('name')
        seating_capacity = form.get('seating_capacity')

        if venue_name is not None:
            venue.name = venue_name
        if seating_capacity is not None:
            venue.seating_capacity = seating_capacity

        db.session.commit()

        return {'status': True, 'msg': 'Venue updated successfully', 'venue_id': venue.venue_id, 'admin_id': venue.admin_id}, 200


    @jwt_required()
    def delete(self, venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        venue = Venue.query.filter_by(venue_id=venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        db.session.delete(venue)
        db.session.commit()

        return {'status': True, 'msg': 'Venue deleted successfully', 'venue_id': venue.venue_id, 'admin_id': venue.admin_id}, 200

#<-----------------------------------------------------SHOW VENUE API------------------------------------------------------------------------------>

class Shows_api(Resource):

    @jwt_required()
    def get(self, venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        venue = Venue.query.filter_by(venue_id=venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        shows = Show.query.filter_by(venue_id=venue_id).all()
        if len(shows) == 0:
            return {'status': False, 'msg': 'No shows available for this venue'}, 400

        shows_data = []
        for show in shows:
            show_data = {
                'show_id': show.show_id,
                'name': show.name,
                'show_datetime': show.date_time,
                'seats_available': show.seats_available,
                'show_screen': show.show_screen,
                'price': show.price
            }
            shows_data.append(show_data)

        return {'shows': shows_data}

    @jwt_required()
    def post(self, venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        venue = Venue.query.filter_by(venue_id=venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        form = request.get_json()
        show_name = form.get('name')
        date_time = form.get('date_time')
        seats_available = form.get('seats_available')
        price = form.get('price')
        show_screen = form.get('show_screen')
        format_data = "%m/%d/%Y %I:%M %p"
        date_time = datetime.strptime(date_time, format_data)

        if is_screen_available(venue_id, show_screen, date_time):
            new_show = Show(name=show_name, date_time=date_time, seats_available=seats_available, price=price, venue_id=venue_id, show_screen=show_screen)
            db.session.add(new_show)
            db.session.commit()
            return {'status': True, 'msg': 'New show added successfully', 'show_id': new_show.show_id}, 200
        else:
            return {'status': False, 'msg': 'Invalid request'}, 400

    @jwt_required()
    def put(self, show_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        show = Show.query.filter_by(show_id=show_id).first()
        if not show:
            return {'status': False, 'msg': 'Show not found'}, 400

        venue = Venue.query.filter_by(venue_id=show.venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        form = request.get_json()
        show_name = form.get('name')
        date_time = form.get('date_time')
        seats_available = form.get('seats_available')
        price = form.get('price')

        if show_name is not None:
            show.name = show_name
        if date_time is not None:
            show.date_time = date_time
        if seats_available is not None:
            show.seats_available = seats_available
        if price is not None:
            show.price = price

        db.session.commit()

        return {'status': True, 'msg': 'Show updated successfully', 'show_id': show.show_id}, 200

    @jwt_required()
    def delete(self, show_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        show = Show.query.filter_by(show_id=show_id).first()
        if not show:
            return {'status': False, 'msg': 'Show not found'}, 400

        venue = Venue.query.filter_by(venue_id=show.venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400

        db.session.delete(show)
        db.session.commit()

        return {'status': True, 'msg': 'Show deleted successfully', 'show_id': show.show_id}, 200
