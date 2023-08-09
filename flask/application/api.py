from flask_restful import Resource, fields
from .models import *
# import datetime
from flask import request, jsonify
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime 
import celerytasks


# <---------------------------------------------------Helper Functions--------------------------------------------------->

def is_screen_available(venue_id, show_screen, date_time):
    print(date_time, type(date_time))
    
    print(date_time)
    if date_time > (datetime.now()):
        
        show = Show.query.filter_by(venue_id = venue_id,show_screen= show_screen).first()
        if show is not None:
            if date_time > (show.date_time + timedelta(hours=3)):
                overlapping_show = None
            else:
                overlapping_show = show
            print('its ok')
            return overlapping_show is None
        else:
            return True
    else: 
        return False

def convert_to_datetime(date_time):
    format_data = "%Y-%m-%dT%H:%M"
    converted_date_time = datetime.strptime(date_time, format_data)
    return converted_date_time

def convert_datetime_to_str(date_time):
    def get_day_suffix(day):
        if 11 <= day <= 13:
            return 'th'
        else:
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    formatted_date = date_time.strftime("%d{} %B, %Y, %I:%M %p").format(get_day_suffix(date_time.day))
    return formatted_date

def convert_tags_into_array(show_tags):
    tags_list = show_tags.split(',')
    tags_list = [tag.strip() for tag in tags_list]  # Remove leading and trailing spaces
    return tags_list




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
                shows = Shows_api.get(self, venue_id=v.venue_id)
                if shows==None:
                    shows = []
                venue_data = {
                    'venue_id': v.venue_id,
                    'name': v.name,
                    'venue_location':v.venue_location,
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
        form = request.get_json()
        venue_name = form.get('name')
        venue_location = form.get('venue_location')
        if venue_name is not None:
            new_venue = Venue(name=venue_name, admin_id=admin.admin_id, venue_location=venue_location)
            print()
            db.session.add(new_venue)
            db.session.commit()
            print(new_venue.venue_location)
            return {'status': True, 'msg':'New Venue added Succesfully', 'venue_id': new_venue.venue_id, 'admin_id': new_venue.admin_id, 'venue_location':new_venue.venue_location}, 200
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
        venue_location = form.get('venue_location')

        if venue_name is not None:
            venue.name = venue_name
        if venue_location is not None:
            venue.venue_location = venue_location

        db.session.commit()

        return {'status': True, 'msg': 'Venue updated successfully', 'venue_id': venue.venue_id, 'admin_id': venue.admin_id, 'venue_location':venue.venue_location}, 200


    @jwt_required()
    def delete(self, venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin:
            return {'status': False, 'msg': 'User not found'}, 400

        venue = Venue.query.filter_by(venue_id=venue_id, admin_id=admin.admin_id).first()
        if not venue:
            return {'status': False, 'msg': 'Venue not found'}, 400
        
        shows = Show.query.filter_by(venue_id=venue_id).all()
        for show in shows:
            booking = Booking.query.filter_by(show_id=show.show_id).all()
            for b in booking:
                db.session.delete(booking)
            db.session.delete(show)

        db.session.delete(venue)
        db.session.commit()

        return {'status': True, 'msg': 'Venue deleted successfully', 'venue_id': venue.venue_id, 'admin_id': venue.admin_id}, 200

#<-----------------------------------------------------ADMIN SHOW VENUE API------------------------------------------------------------------------------>

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
            # raise DataError(status_code=400)
            return None

        shows_data = []
        for show in shows:
            if show.date_time < datetime.now():
                past_show = True
            else:
                past_show = False
            show_data = {
                'show_id': show.show_id,
                'name': show.name,
                'show_datetime': convert_datetime_to_str(show.date_time),
                'seats_booked': show.seats_booked,
                'seats_available': show.seats_available,
                'show_screen': show.show_screen,
                'imagefile': show.image,
                'past_show': past_show,
                'price': show.price,
                'tags': convert_tags_into_array(show.tags)
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
        date_time = form.get('show_datetime')
        seats_available = form.get('show_seats')
        price = form.get('price')
        show_screen = form.get('show_screen')
        tags = form.get('tags')
        image = form.get('imagefile')
        date_time = convert_to_datetime(date_time)

        if is_screen_available(venue_id, show_screen, date_time):
            new_show = Show(name=show_name, date_time=date_time, seats_available=seats_available, price=price, venue_id=venue_id, show_screen=show_screen, image=image,tags=tags)
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
        show_screen = form.get('show_screen')
        date_time = form.get('date_time')
        seats_available = form.get('seats_available')
        price = form.get('price')
        tags = form.get('tags')
        image = form.get('imagefile')
        date_time = convert_to_datetime(date_time)
        if show_name is not None:
            show.name = show_name
        if date_time is not None:
            show.date_time = date_time
        if show_screen is not None:
            show.show_screen = show_screen
        if seats_available is not None:
            show.seats_available = seats_available
        if price is not None:
            show.price = price
        if image is not None:
            show.image = image
        if tags is not None:
            show.tags = tags

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

        booking = Booking.query.filter_by(show_id=show.show_id).all()
        for b in booking:
            db.session.delete(b)

        db.session.delete(show)
        db.session.commit()

        return {'status': True, 'msg': 'Show deleted successfully', 'show_id': show.show_id}, 200


#<-----------------------------------------------------USER VENUE&SHOW VENUE API------------------------------------------------------------------------------>
class User_api(Resource):

    @jwt_required()
    def get(self):
        # print("Reaching here")
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return {'status': False, 'msg': 'User not found'}, 400

        venues = Venue.query.all()
        if not venues:
            return {'status': False, 'msg': 'No venue added yet'},200

        data = []
        for v in venues:  # Use 'v' instead of 'venue'
            shows = Show.query.filter_by(venue_id=v.venue_id).all() 
            shows_data = []
            for show in shows:
                if show.date_time > datetime.now():
                    show_data = {
                        'show_id': show.show_id,
                        'name': show.name,
                        'show_datetime': convert_datetime_to_str(show.date_time),
                        'seats_booked': show.seats_booked,
                        'seats_available': show.seats_available,
                        'show_screen': show.show_screen,
                        'tags': convert_tags_into_array(show.tags),
                        'imagefile': show.image,
                        'price': show.price
                    }
                    shows_data.append(show_data)

            venue_data = {
                'venue_id': v.venue_id,  # Use 'v.venue_id' instead of 'venue.venue_id'
                'name': v.name,  # Use 'v.name' instead of 'venue.name'
                'venue_location': v.venue_location,  # Use 'v.venue_location' instead of 'venue.venue_location'
                'admin_id': v.admin_id,  # Use 'v.admin_id' instead of 'venue.admin_id'
                'shows': shows_data
            }
            data.append(venue_data)

        return {"venues": data},200
    
    @jwt_required()
    def put(self,show_id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return {'status': False, 'msg': 'User not found'}, 400

        s = Show.query.filter_by(show_id=show_id).first()
        if s is None:
                {'status': False, 'msg': 'Show not found'}, 400
        form =request.get_json()
        tickets = form.get('tickets')
        if tickets is not None and tickets > 0:
            if (s.seats_available >= tickets):
                s.seats_booked = s.seats_booked + tickets
                if (s.seats_booked >= s.seats_available) == False:
                    db.session.commit()
                else:
                    return {'status': False, 'msg': 'Not enough seats available'}, 400
                new_booking = Booking(user_id=user.user_id, show_id=s.show_id,tickets=tickets)
                db.session.add(new_booking)
                db.session.commit()
                return {'status': True, 'msg': 'Booking successful'}, 200
            else:
                return {'status': False, 'msg': 'Invalid no. of seats'}, 400
        
        else:
            return {'status': False, 'msg': 'Invalid number of tickets'}, 400

#<-----------------------------------------------------BOOKING API------------------------------------------------------------------------------>

class Booking_api(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return {'status': False, 'msg': 'User not found'}, 400
        booking = Booking.query.filter_by(user_id=user.user_id).all()
        data = []

        for b in booking:
            shows = Show.query.filter_by(show_id=b.show_id).all() 
            shows_data = {}
            for show in shows:
                if show.date_time > datetime.now():
                    past_show = True
                else:
                    past_show = False
                show_data = {
                    'show_id': show.show_id,
                    'name': show.name,
                    'show_datetime': convert_datetime_to_str(show.date_time),
                    'seats_booked': show.seats_booked,
                    'seats_available': show.seats_available,
                    'show_screen': show.show_screen,
                    'imagefile': show.image,
                    'price': show.price,
                    'past_show': past_show,
                    'tickets': b.tickets
                }
                shows_data = show_data
                # shows_data = show_data

            booking_data = {
                'booking_id': b.booking_id,  # Use 'v.venue_id' instead of 'venue.venue_id'
                'user_id': b.user_id,  # Use 'v.name' instead of 'venue.name'
                'show_id': b.show_id,  # Use 'v.venue_location' instead of 'venue.venue_location'
                'tickets': b.tickets,  # Use 'v.admin_id' instead of 'venue.admin_id'
                'shows': shows_data
            }
            data.append(booking_data)

        return {"bookings": data},200


    @jwt_required()
    def delete(self,booking_id):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return {'status': False, 'msg': 'User not found'}, 400
        booking = Booking.query.filter_by(booking_id=booking_id).first()
        show = Show.query.filter_by(show_id=booking.show_id).first()
        show.seats_booked = show.seats_booked - booking.tickets
        db.session.delete(booking)
        db.session.commit()

        return {'status': True, 'msg': 'Booking Cancelled successfully'}, 200       


#<-----------------------------------------------------SEARCHING API------------------------------------------------------------------------------> 

class Search(Resource):
    @jwt_required()
    def get(self, searchvalue):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if not user:
            return {'status': False, 'msg': 'User not found'}, 400
        
        venue = Venue.query.all()
        sshows = Show.query.all()
        data = []
        for v in venue:
            if (searchvalue in v.name.lower()) or (searchvalue in v.venue_location.lower()):
                shows = Show.query.filter_by(venue_id=v.venue_id).all() 
                shows_data = []
                for show in shows:
                    if show.date_time > datetime.now():
                        show_data = {
                            'show_id': show.show_id,
                            'name': show.name,
                            'show_datetime': convert_datetime_to_str(show.date_time),
                            'seats_booked': show.seats_booked,
                            'seats_available': show.seats_available,
                            'show_screen': show.show_screen,
                            'tags': convert_tags_into_array(show.tags),
                            'imagefile': show.image,
                            'price': show.price
                        }
                        shows_data.append(show_data)

                venue_data = {
                    'venue_id': v.venue_id,  # Use 'v.venue_id' instead of 'venue.venue_id'
                    'name': v.name,  # Use 'v.name' instead of 'venue.name'
                    'venue_location': v.venue_location,  # Use 'v.venue_location' instead of 'venue.venue_location'
                    'admin_id': v.admin_id,  # Use 'v.admin_id' instead of 'venue.admin_id'
                    'shows': shows_data
                }
                data.append(venue_data)

        if len(data)>0:
            return {"venues": data},200
            
        other_data = []
        for s in sshows:
            ven = Venue.query.filter_by(venue_id=s.venue_id).first()
            if (searchvalue in s.name) or (searchvalue in convert_tags_into_array(s.tags)):
                shows_data = []
                if s.date_time > datetime.now():
                    show_data = {
                        'show_id': s.show_id,
                        'name': s.name,
                        'show_datetime': convert_datetime_to_str(s.date_time),
                        'seats_booked': s.seats_booked,
                        'seats_available': s.seats_available,
                        'show_screen': s.show_screen,
                        'tags': convert_tags_into_array(s.tags),
                        'imagefile': s.image,
                        'price': s.price
                    }
                    shows_data.append(show_data)

                    venue_data = {
                        'venue_id': ven.venue_id,  # Use 'v.venue_id' instead of 'venue.venue_id'
                        'name': ven.name,  # Use 'v.name' instead of 'venue.name'
                        'venue_location': ven.venue_location,  # Use 'v.venue_location' instead of 'venue.venue_location'
                        'admin_id': ven.admin_id,  # Use 'v.admin_id' instead of 'venue.admin_id'
                        'shows': shows_data
                    }
                    other_data.append(venue_data)
        
        if len(other_data)>0:
            return {"venues": other_data},200
        
        return {'msg': 'No Results Found'},400


class ExportJob(Resource):
    @jwt_required()
    def get(self,venue_id):
        current_admin = get_jwt_identity()
        admin = Admin.query.filter_by(email=current_admin).first()
        if not admin :
            return {'status': False, 'msg' : 'User not found'}, 400
        
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        celerytasks.exportVenue.delay(venue_id=venue_id, admin_mail=admin.email, admin_name=admin.name)

        return jsonify('Task submitted')

