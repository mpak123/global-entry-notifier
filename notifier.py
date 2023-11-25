#!/usr/bin/env python

from math import log
import requests
import time
import sys
from datetime import datetime, timedelta
import yagmail
import logging

# API URL
APPOINTMENTS_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={}&minimum=1"

EMAIL_TEMPLATE = """
<p>Good news! New Global Entry appointment(s) available on the following date:</p>
%s
"""

# List of Global Entry locations
# Insert your location IDs here
LOCATION_IDS = {
    'Newark': 5444,
    'Nashville': 10260
}

# How often to run this check in seconds
TIME_WAIT = 60

# Number of days into the future to look for appointments
DAYS_OUT = 60

# Dates
now = datetime.now()
future_date = now + timedelta(days=DAYS_OUT)

def notify_send_email(date):
    recipient = "Insert recipient email address here"

    try:
        yagmail.SMTP(recipient, oauth2_file="~/credentials.json").send(dfrecipient, 'Global Entry Appointment Available!', EMAIL_TEMPLATE % date)
    except Exception:
        logging.exception('Failed to send succcess e-mail.')
        log(e)

def check_appointments(city, id):
    url = APPOINTMENTS_URL.format(id)
    appointments = requests.get(url).json()
    return appointments

def appointment_in_timeframe(now, future_date, appointment_date):
    if now <= appt_datetime <= future_date:
        return True
    else:
        return False


try:
    while True:
        for city, id in LOCATION_IDS.items():
            try:
                appointments = check_appointments(city, id)
            except Exception as e:
                print("Could not retrieve appointments from API.")
                appointments = []
            if appointments:
                appt_datetime = datetime.strptime(appointments[0]['startTimestamp'], '%Y-%m-%dT%H:%M')
                if appointment_in_timeframe(now, future_date, appt_datetime):
                    message = "{}: Found an appointment at {}!".format(city, appointments[0]['startTimestamp'])
                    notify_send_email(message)
                else:
                    print("{}: No appointments during the next {} days.".format(city, DAYS_OUT))
            else:
                print("{}: No appointments during the next {} days.".format(city, DAYS_OUT))
            time.sleep(1)
        time.sleep(TIME_WAIT)
except KeyboardInterrupt:
    sys.exit(0)
