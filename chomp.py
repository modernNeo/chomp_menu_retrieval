import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen

from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

url = "https://www.chompveganeatery.com/meal-prep-service"

months = ['jan ', 'feb ', 'marc ', 'apr ', 'may ', 'june ', 'july ', 'aug ', 'sept ', 'oct ', 'nov ', 'dec ']


def send_email(subject: str = None, body: str = None):
    from_person_name = 'CHOMP'
    from_person_email = os.environ['FROM_EMAIL']
    password = f"{os.environ['BESTBUY_STEELBOOKS_PASSWORD']}"
    to_person_email = os.environ['TO_EMAIL']

    print("Setting up MIMEMultipart object")
    msg = MIMEMultipart()
    msg['From'] = from_person_name + " <" + from_person_email + ">"
    msg['To'] = " <" + to_person_email + ">"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    print("Connecting to smtp.gmail.com:587")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    print("Logging into your gmail")
    server.login(from_person_email, password)
    print("Sending email...")
    server.send_message(from_addr=from_person_email, to_addrs=to_person_email, msg=msg)
    server.close()


def get_entries(menu_data, start_printing):
    all_entries = []
    if type(menu_data) is dict:
        for (key, value) in menu_data.items():
            entry, new_start_printing = get_entries(value, start_printing)
            if not start_printing and new_start_printing:
                start_printing = new_start_printing
            if len(entry) > 0:
                all_entries.extend(entry)
        return all_entries, start_printing
    elif type(menu_data) is list:
        for index, entry in enumerate(menu_data):
            entry, new_start_printing = get_entries(entry, start_printing)
            if not start_printing and new_start_printing:
                start_printing = new_start_printing
            if len(entry) > 0:
                all_entries.extend(entry)
        return all_entries, start_printing
    elif type(menu_data) is bool or type(menu_data) is int or menu_data is None:
        return [], start_printing

    for month in months:
        try:
            if month in menu_data.lower():
                start_printing = True
                break
        except Exception:
            pass
    if start_printing:
        return menu_data, start_printing
    else:
        return [], start_printing


# f = open("/home/jace/siteData")
# json_file = json.load(f)
def poll_chomp_menu():
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script"]):
        if "BOOTSTRAP_STATE_" in script.next:
            send_email(
                "CHOMP_MENU",
                body="".join(
                    get_entries(
                        json.loads(script.contents[0].strip().replace("window.__BOOTSTRAP_STATE__ = ", "")[:-1]),
                        False
                    )[0]
                ).replace("\n", "<br>")
            )


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(poll_chomp_menu, 'cron', day_of_week='mon', hour='1')
    scheduler.start()
