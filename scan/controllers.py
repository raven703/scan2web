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
        data, raw_data, total_query = check_chars_from_local(form.text.data)
        if not data or 'error' in data:
            return render_template('error.html', title='Error Page')

        else:

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
