import os, time
import csv

from flask import render_template, redirect, url_for, Response
from app import app

from scan.forms import ScanForm
from scan.main_func import *
from datetime import datetime

r = redis.Redis(host="pserv")

db.create_all()


@app.route('/progress')
def progress():
    def generate():
        while True:
            esi_query = '{' + f'"max":{r.get("max").decode("utf8")}, "current":{r.get("current").decode("utf8")}' + '}\n\n'
            #yield 'data: ' + '{' + f'"max":{r.get("max").decode("utf8")}, "current":{r.get("current").decode("utf8")}' + '}\n\n'
            yield 'data:' + esi_query
            time.sleep(0.9)

    return Response(generate(), mimetype='text/event-stream')




# @app.route('/index2')
# def index2():
#     with open('addbase.csv') as file:
#         data = csv.DictReader(file, delimiter=";")
#         for row in list(data):
#             u = InvTypes(typeid=row["TYPEID"], groupid=row["GROUPID"], typename=row["TYPENAME"])
#             db.session.add(u)
#             db.session.commit()
#     return render_template('index2.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    r.mset({'max': 0})
    r.mset({'current': 0})
    form = ScanForm()
    if form.validate_on_submit():

        if chr(9) in form.text.data:

            ships_common = count_ships([i.replace("\xa0", "").replace("-", "").split(chr(9)) for i in form.text.data.splitlines()])

            url = ships_common['url']
            return redirect(f'/{url}')


        else:
            data, raw_data, total_query = check_chars_from_local(form.text.data)
            if not data or 'error' in data:
                return redirect(url_for('index'))

            ch_aff = aff_new(raw_data)
            common = count_ally(ch_aff)
            url = common['url']
            return redirect(f'/{url}')

    return render_template('index.html', title='Hello!', form=form)


@app.route('/<url>', methods=['GET', 'POST'])
def scan_url(url):
    start_time = time.time()

    dbScanResult = ShipDB.query.filter(ShipDB.url == url).first()
    if dbScanResult is None:
        return redirect(url_for('index'))

    data = json.loads(dbScanResult.data)
    timestamp = dbScanResult.timestamp
    dt_now = datetime.utcnow()
    scan_time = timestamp.strftime("%H:%M ET")
    scan_date = timestamp.strftime("%d.%m.%Y")
    time_delta = str(dt_now - timestamp)[:-7]
    current_time = dt_now.strftime("%H:%M ET")
    current_date = dt_now.strftime("%d.%m.%Y")

    if 'corporations' not in data:
        ships_common = data
        ships_total = dict(sorted(ships_common['ships_useful'].items(), key=lambda x: x[1][0], reverse=True))
        types_total = dict(sorted(ships_common['types_total'].items(), key=lambda x: x[1][0], reverse=True))
        print(ships_common)
        print(ships_total)

        types_num = len(ships_total)

        ships_num = sum([i[0] for i in ships_total.values()])
        url_name = f"/{ships_common['url']}"
        exec_time = round(time.time() - start_time, 3)
        return render_template('shipDb.html', title=f"{ships_num} ships in system", exec_time=exec_time, ships_total= ships_total, types_total= types_total, url=url_name,
                               current_time = current_time, scan_time = scan_time,
                               scan_date = scan_date, time_delta = time_delta,
                               types_num = types_num,
                               ships_num = ships_num,
                               ships_common=ships_common)
    else:

        total_alliance = dict(sorted(data['alliances'].items(), key=lambda x: x[1].get('count'), reverse=True))
        total_corp = dict(sorted(data['corporations'].items(), key=lambda x: x[1].get('count'), reverse=True))
        total_count = data["total"]  # total alliances
        total_corps = data["total_corps"]
        total_chars = data["total_chars"]
        total_query = data["total"]
        url_name = f"/{data['url']}"

        dt = datetime.utcnow()

        exec_time = round(time.time() - start_time, 3)
        return render_template('scanDb.html', title=f"{total_chars} pilots in local",
                               total_alliance=total_alliance, total_corp=total_corp, total_query=total_query,
                               total_count=total_count, total_corps=total_corps, total_chars=total_chars,
                               exec_time=exec_time, url=url_name, current_date=current_date, current_time = current_time, scan_time = scan_time,
                               scan_date = scan_date, time_delta = time_delta)


