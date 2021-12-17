import time
from flask import render_template
from app import app, db

from scan.forms import ScanForm
from scan.main_func import *

from scan.models import UserDB


db.create_all()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():  # put application's code here

    form = ScanForm()
    if form.validate_on_submit():
        start_time = time.time()

        if chr(9) in form.text.data:

            ships_common = count_ships([i.split(chr(9)) for i in form.text.data.splitlines()])
            ships_total = dict(sorted(ships_common['ships_total'].items(), key=lambda x: x[1], reverse=True))
            types_total = dict(sorted(ships_common['types_total'].items(), key=lambda x: x[1], reverse=True))
            url = ships_common['url']
            exec_time = round(time.time() - start_time, 3)

            return render_template('ships.html', title='Ships scan result', exec_time=exec_time, ships_total= ships_total, types_total= types_total, url=url)


        else:
            data, raw_data, total_query = check_chars_from_local(form.text.data)
            if not data or 'error' in data:
                return render_template('error.html', title='Error Page')

            ch_aff = aff_new(raw_data)
            common = count_ally(ch_aff)
            total_alliance = dict(sorted(common["alliance"].items(), key=lambda x: x[1], reverse=True))
            total_corp = dict(sorted(common["corporation"].items(), key=lambda x: x[1], reverse=True))
            total_count = common["total"]
            total_corps = common["total_corps"]
            total_chars = common["total_chars"]
            exec_time = round(time.time() - start_time, 3)
            return render_template('scan.html', title='Scan result page',
                                   total_alliance=total_alliance, total_corp=total_corp, total_query=total_query,
                                   total_count=total_count, total_corps=total_corps, total_chars=len(raw_data), exec_time=exec_time)

    return render_template('index.html', title='Scan Page', form=form)


@app.route('/<url>', methods=['GET'])
def scan_url(url):
    start_time = time.time()

    dbScanResult = ShipDB.query.filter(ShipDB.url == url).first()
    ships_common = json.loads(dbScanResult.data)
    ships_total = dict(sorted(ships_common['ships_total'].items(), key=lambda x: x[1], reverse=True))
    types_total = dict(sorted(ships_common['types_total'].items(), key=lambda x: x[1], reverse=True))
    exec_time = round(time.time() - start_time, 3)
    url_name = f"/{ships_common['url']}"


    return render_template('ships_url.html', title='Ships scan result', exec_time=exec_time, ships_total= ships_total, types_total= types_total, url=url_name)
