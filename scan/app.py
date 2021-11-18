from flask import Flask, render_template

from scan.forms import ScanForm
from scan.main_func import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():  # put application's code here

    form = ScanForm()
    if form.validate_on_submit():
        data = get_chars_from_local(form.text.data)
        char_affil = requests.post('https://esi.evetech.net/latest/characters/affiliation/', headers=headers,
                                   params=params, data=data).json()
        total_alliance = count_ally(char_affil)["alliance"]
        total_corp = count_ally(char_affil)["corporation"]
        return render_template('scan.html', title='Scan result page', total_alliance=total_alliance, total_corp=total_corp)

    return render_template('index.html', title='Scan Page', form=form)


if __name__ == '__main__':
    app.run()
