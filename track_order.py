import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from time import sleep


# autenticacao twilio
# pegue suas credenciais: http://twil.io/secure
account_sid = 'ACa3e0745640b287f1229ff9132124d33e'
auth_token = 'd6ab5d840239b346cc16aa2e6d3df488'
account_number = "+16106162702"
client = Client(account_sid, auth_token)


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
                from_=account_number
            )
            return message
        else:
            return
    except TwilioRestException:
        return
