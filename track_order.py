import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# autenticacao twilio
# pegue suas credenciais: http://twil.io/secure
ACCOUNT_SID = ''
AUTH_TOKEN = ''
ACCOUNT_NUMBER = ""
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def search_track_order(code):
    url = "https://www.linkcorreios.com.br/?id="+code
    try:
        r_track = requests.get(url)
        if r_track.status_code != 200:
            return {}
        h_track = r_track.text
        soup = BeautifulSoup(h_track, "html.parser")
        card = soup.find("div", class_="card-header").find_all("li")
        last_status = card[0].find("b").text
        if "destinatÃ¡rio" in last_status:
            last_status = last_status.replace('destinatÃ¡rio', "destinatário")
        track_order_status = {
            "code": code,
            "last_status": last_status,
            "last_update": card[1].text,
            "locate": card[2].text
        }
        return track_order_status
    except requests.exceptions.ConnectionError as err:
        print(err)
        return {}
    except Exception as err:
        print(err)
        return {}


def send_msg(to, result, clt=client):
    try:
        if result:
            msg = f"""
    
    Code: {result['code']}
    Status: {result['last_status']}
    Last Update: {result['last_update']}
    Locate: {result['locate']}
            """
            message = clt.messages.create(
                to=to,
                body=msg,
                from_=ACCOUNT_NUMBER
            )
            return message
        else:
            return
    except TwilioRestException:
        return
