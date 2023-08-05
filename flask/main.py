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
api.add_resource(Booking_api, "/api/UserBookings", "/api/UserBookings/<booking_id>")
api.add_resource(Search, "/api/search/<searchvalue>")






if __name__=='__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)

