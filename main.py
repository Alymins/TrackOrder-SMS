from flask import Flask, render_template, url_for, request, redirect
from track_order import send_msg, search_track_order
from tracks_code_db import save_track_code, send_msg_every_day
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(send_msg_every_day, 'interval', hours=1)
scheduler.start()

app = Flask("Track Order - SMS")


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/enviado")
def search():
    code = request.args.get("code")
    phone_number = request.args.get("phone")
    ok = request.args.get("ok")
    if not code or not phone_number or not ok:
        return redirect(url_for("main"))
    try:
        assert phone_number.startswith("+")
    except Exception:
        return redirect(url_for('main'))
    result = search_track_order(code)
    print(result)
    if "entregue ao destinatário" not in result['last_status']:
        save_track_code((phone_number, code, result["last_update"]))
    else:
        pass
    msg = send_msg(to=phone_number, result=result)
    return render_template("send.html", msg=msg)


app.run()
send_msg_every_day()
