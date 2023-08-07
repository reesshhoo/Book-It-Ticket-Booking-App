from flask import Flask
import celerytasks
import os
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from application import workers
from application import config
from application.config import LocalDevelopmentConfig
from flask_jwt_extended import JWTManager
from application import celery_tasks
from flask_cors import CORS
from application.models import *
from application.api import *


app = Flask(__name__)
if os.getenv("ENV", "development") == "production":
    raise Exception("Currently no production config is setup.")
else:
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
app.app_context().push()
db.create_all()

CORS(app)
app.app_context().push()
celery=workers.celery
celery.conf.update(
broker_url = app.config["CELERY_BROKER_URL"],
result_backend = app.config["CELERY_RESULT_BACKEND"])   
celery.conf.timezone = "Asia/Kolkata"
celery.Task = workers.ContextTask
app.app_context().push()
cache=Cache(app)
app.app_context().push()
api = Api(app)
app.app_context().push()

jwt=JWTManager(app)
app.app_context().push()

# @app.route('/something')
# def celery():
#     job = celerytasks.just_say_hello.delay()
#     return "done",200


api.add_resource(Login_api, "/api/login")
api.add_resource(Register_api, "/api/register")
api.add_resource(Venue_api,"/api/Venues", "/api/Venues/<venue_id>")
api.add_resource(Shows_api, "/api/Shows/<venue_id>","/api/Shows/edit/<show_id>")
api.add_resource(User_api, "/api/User", "/api/User/<show_id>")
api.add_resource(Booking_api, "/api/UserBookings", "/api/UserBookings/<booking_id>")
api.add_resource(Search, "/api/search/<searchvalue>")
api.add_resource(ExportJob,"/api/ExportJob/<venue_id>")






if __name__=='__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)

