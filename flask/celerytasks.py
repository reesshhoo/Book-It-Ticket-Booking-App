from main import workers
from main import app, cache
from mail_config import send_email, generate_report_content, send_monthly_report
import csv
from application.models import *
from celery.schedules import crontab
from datetime import datetime
import os
from jinja2 import Template
import matplotlib.pyplot as plt
from base64 import b64encode
from weasyprint import HTML


celery = workers.celery


# @celery.task()
# def just_say_hello():
#     print("celery works!")
#     print("Hello ")


@celery.task()
@cache.memoize(timeout=15)
def exportVenue(venue_id,admin_mail,admin_name):
    venue = Venue.query.filter_by(venue_id=venue_id).first()
    filepath = 'static/download/'+venue.name+'_Theatre_details.csv'

    # Check if folder is not present then create one
    if not os.path.exists('static/download/'):
        os.mkdir(path='static/download/')
    with open(file=filepath, mode='w') as file:
        csv_obj = csv.writer(file, delimiter=',')
        csv_obj.writerow(['Venue Id', 'Venue Name', 'Show Name',
                          'No.of tickets Sold'])
        shows = Show.query.filter_by(venue_id=venue_id).all()

        for i in shows:
            csv_obj.writerow([i.venue_id, venue.name, i.name,
                                i.seats_booked])
    
    with open(r"download.html") as file:
        msg_template = Template(file.read())

    content = msg_template.render(
        admin_name=admin_name,
    )
    send_email(to=admin_mail,subject="Export Data",msg=content ,attachment=filepath)
    return "success"




@celery.task()
def user_daily_reminders():
        users = User.query.all()
        # print(users)
        # print('hello')
        for user in users:
            bookings = Booking.query.filter_by(user_id=user.user_id).all()
            # print('reached here')
            for booking in bookings:
                booking_show = Show.query.filter_by(show_id=booking.show_id).first()
                # print(booking_show)
                booking_datetime = booking_show.date_time
                # print('checking datetime')
                if booking_datetime > datetime.now():
                    msg = '''
                        Dear {},<br>
				        You have shows coming up.<br>
				        Please, Visit check the recent updates <br>
				        <br>
				        Thank you<br>
				        BookIt Team
                    '''.format(user.name)
                    send_email(user.email,"Daily Reminder",msg)
                    print('sent mail')
                    break

            else:
                msg = '''
                        Dear {},<br>
				        We have some exiciting shows lined up!<br>
				        Please, Visit check the recent updates. <br>
				        <br>
				        Thank you<br>
				        BookIt Team
                    '''.format(user.name)
                send_email(user.email,"Daily Reminder",msg)




@celery.task()
def user_monthly_report():
    users = User.query.all()
    for user in users:
        total_shows_booked = 0
        total_tickets_booked = 0
        bookings = Booking.query.filter_by(user_id=user.user_id).all()
        for booking in bookings:
            booking_show = Show.query.filter_by(show_id=booking.show_id).first()
            print(booking_show)
            booking_datetime = booking_show.date_time
            if booking_datetime.month == datetime.now().month:
                total_shows_booked += 1
                total_tickets_booked += booking.tickets


        send_monthly_report(user.email, 'Monthly Report', user.name, total_shows_booked, total_tickets_booked)
        

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	# sender.add_periodic_task(1.0, user_daily_reminders.s(), name='kuch bhi')
	# sender.add_periodic_task(crontab(minute=28, hour=23), daily_reminders.s(), name='daily_reminders')
	sender.add_periodic_task(crontab(day=1), user_monthly_report.s(), name='monthly_report')
	sender.add_periodic_task(crontab(minute=30, hour=20), user_daily_reminders.s(), name='user_daily_reminders')

	print('changed')
	# sender.add_periodic_task(crontab(minute=00, hour=7), monthly_html_report.s(), name='monthly_html_repost')
	# sender.add_periodic_task(crontab(minute=00, hous=2), monthly_pdf_report.s(), name='monthly_pdf_report')
	# #testing 
	# sender.add_periodic_task(20, monthly_html_report.s(), name='monthly_html_repost')
	# sender.add_periodic_task(20, monthly_pdf_report.s(), name='monthly_pdf_report')