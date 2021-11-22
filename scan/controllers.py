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

        u = UserDB(uid='665335352', name='Saori Shirayuki', alliance='Everto', a_ticker='EVR', a_id='665335352',
                 corporation='VERTO', c_ticker='VVV', c_id='1983708877')
        db.session.add(u)
        db.session.commit()

        data = get_chars_from_local(form.text.data)
        if not data:
            return render_template('error.html', title='Error Page')
        else:
            char_affil = requests.post('https://esi.evetech.net/latest/characters/affiliation/', headers=headers,
                                   params=params, data=data).json()
            # input [UID,UID,UID], return list of dicts
            total_alliance = dict(sorted(count_ally(char_affil)["alliance"].items(), key=lambda x: x[1], reverse=True))
            total_corp = dict(sorted(count_ally(char_affil)["corporation"].items(), key=lambda x: x[1], reverse=True))
            return render_template('scan.html', title='Scan result page',
                                   total_alliance=total_alliance, total_corp=total_corp)

    return render_template('index.html', title='Scan Page', form=form)
