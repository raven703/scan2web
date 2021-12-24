import time
from flask import render_template, redirect, url_for
from app import app

from scan.forms import ScanForm
from scan.main_func import *



db.create_all()
@app.route('/index2', methods=['GET'])
def index2():
    return render_template('index2.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    form = ScanForm()
    if form.validate_on_submit():
        start_time = time.time()

        if chr(9) in form.text.data:

            ships_common = count_ships([i.split(chr(9)) for i in form.text.data.splitlines()])
            # ships_total = dict(sorted(ships_common['ships_total'].items(), key=lambda x: x[1], reverse=True))
            # types_total = dict(sorted(ships_common['types_total'].items(), key=lambda x: x[1], reverse=True))
            url = ships_common['url']
            # exec_time = round(time.time() - start_time, 3)
            return redirect(f'/{url}')

            # return render_template('ships.html', title='Ships scan result', exec_time=exec_time, ships_total= ships_total, types_total= types_total, url=url)


        else:
            data, raw_data, total_query = check_chars_from_local(form.text.data)
            if not data or 'error' in data:
                # print(data)
                return redirect(url_for('index'))

            ch_aff = aff_new(raw_data)
            common, common2 = count_ally(ch_aff)
            # total_alliance = dict(sorted(common["alliance"].items(), key=lambda x: x[1], reverse=True))
            # total_corp = dict(sorted(common["corporation"].items(), key=lambda x: x[1], reverse=True))
            # total_count = common["total"]
            # total_corps = common["total_corps"]
            # total_chars = common["total_chars"]
            # exec_time = round(time.time() - start_time, 3)
            # return render_template('scan.html', title='Scan result page',
            #                        total_alliance=total_alliance, total_corp=total_corp, total_query=total_query,
            #                        total_count=total_count, total_corps=total_corps, total_chars=len(raw_data), exec_time=exec_time, url=url)

            url = common2['url']
            print(common2)
            return redirect(f'/{url}')

    return render_template('index.html', title='Scan Page', form=form)


@app.route('/<url>', methods=['GET', 'POST'])
def scan_url(url):
    start_time = time.time()

    dbScanResult = ShipDB.query.filter(ShipDB.url == url).first()
    if dbScanResult is None:
        return redirect(url_for('index'))

    data = json.loads(dbScanResult.data)
    if 'corporation' not in data:
        ships_common = data
        ships_total = dict(sorted(ships_common['ships_total'].items(), key=lambda x: x[1], reverse=True))
        types_total = dict(sorted(ships_common['types_total'].items(), key=lambda x: x[1], reverse=True))
        url_name = f"/{ships_common['url']}"
        exec_time = round(time.time() - start_time, 3)
        return render_template('ships_url.html', title='Ships scan result', exec_time=exec_time, ships_total= ships_total, types_total= types_total, url=url_name)
    else:

        common = data
        total_alliance = dict(sorted(common["alliances"].keys().items(), key=lambda x: x[1], reverse=True))
        total_corp = dict(sorted(common["corporation"].items(), key=lambda x: x[1], reverse=True))
        total_count = common["total"]
        total_corps = common["total_corps"]
        total_chars = common["total_chars"]
        total_query = common["total"]
        url_name = f"/{common['url']}"

        exec_time = round(time.time() - start_time, 3)
        return render_template('scanDb.html', title='Scan result page',
                               total_alliance=total_alliance, total_corp=total_corp, total_query=total_query,
                               total_count=total_count, total_corps=total_corps, total_chars=total_chars,
                               exec_time=exec_time, url=url_name)


