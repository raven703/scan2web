from esipy import EsiApp
from esipy import EsiClient
import redis
import requests
import json
import datetime
import re
import uuid
import time



from flask_sqlalchemy import SQLAlchemy
from scan.models import UserDB
from scan.models import ShipDB
from app import db

headers = {
    'accept': 'application/json',
    'Accept-Language': 'en',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
}

params = (
    ('datasource', 'tranquility'),
    ('language', 'en'),
)

esi_app = EsiApp(cache_time=300)
app_esi = esi_app.get_latest_swagger

client = EsiClient(
    retry_requests=False,  # set to retry on http 5xx error (default False)
    headers={'User-Agent': 'first test app'},
    raw_body_only=False,  # default False, set to True to never parse response and only return raw JSON string content.
)



def get_alliance_info(a_id):
    get_alliance1 = app_esi.op['get_alliances_alliance_id'](
        alliance_id=a_id,
        datasource='tranquility',
    )

    return client.request(get_alliance1).data


def get_corporation_info(c_id):
    get_corporation = app_esi.op['get_corporations_corporation_id'](
        corporation_id=c_id,
        datasource='tranquility',
    )
    response = client.request(get_corporation).data

    return response


def get_char_info(c_id):
    get_char = app_esi.op['get_characters_character_id'](
        character_id=c_id,
        datasource='tranquility',
    )
    response = client.request(get_char).data
    return response


def convert_to_tranq_post(data: list) -> str:  # convert to Tranq POST string format ex. [ "96667530", "93503913" ]

    result = '['
    for name in data:
        result = f'{result} "{str(name)}",'
    result = f"{result.strip(',')} ]"
    return result


def db_check_user(user):

    year = user.timestamp.year
    month = user.timestamp.month
    day = user.timestamp.day
    past_date = datetime.datetime(year, month, day)
    now = datetime.datetime.utcnow()
    delta = now - past_date
    if delta.days > 7:
        char = get_char_info(user.uid)

        if "error" not in char:
            u = UserDB.query.filter(UserDB.name == user.name).first()
            if 'alliance_id' in char:
                u.a_id = char.alliance_id
            u.c_id = char.corporation_id
            u.timestamp = datetime.datetime.utcnow()
            db.session.commit()
        elif "Character has been deleted" in char.error:

            deleteUser = UserDB.query.filter(UserDB.name == user.name).first()

            if deleteUser is not None:
                db.session.delete(deleteUser)
                db.session.commit()
    return

def chunc(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def check_chars_from_local(data: str):
    # this func gets characters from local scan, check them in DB and if not: ask TRANQ for info and put into DB
    # return 2 style data: raw as list and formatted as TRANQ post request

    r = redis.Redis(host="pserv")
    r.mset({"max": 0})

    raw_data = list(set([i for i in data.strip().replace('\r', '').split('\n') if len(i) > 0]))
    if re.search(r'[^a-zA-Z0-9 \'\-`!]', ''.join(raw_data)):
        return 'error in re', 'error', 'error'

    request_list = []
    cid_list = []
    total_query = {}
    for name in raw_data:
        user = UserDB.query.filter(UserDB.name == name).first()
        if user is None:
            request_list.append(name)
        else:
            db_check_user(user)
            cid_list.append(user.uid)

    total_query['TRANQ_Server'] = len(request_list)
    total_query['Database'] = len(cid_list)


    if len(request_list) > 0:

        request_list = list(chunc(request_list, 25))
        proc_value = 100 // len(request_list)
        counter = 0

        for req_list in request_list:
            r.mset({'current': counter + proc_value})
            data_id = requests.post('https://esi.evetech.net/latest/universe/ids/', headers=headers, params=params,
                                data=convert_to_tranq_post(req_list)).json()

            # get chars ID from server
            if 'characters' in data_id:
                for slovar in data_id['characters']:
                    char_info = get_char_info(slovar['id'])
                    if "error" not in char_info:
                        cid_list.append(slovar['id'])  # list for chars ID
                    if 'alliance_id' in list(char_info):
                        u = UserDB(uid=slovar['id'], name=slovar['name'], a_id=char_info.alliance_id,
                               c_id=char_info.corporation_id)
                        db.session.add(u)
                        db.session.commit()
                    elif "corporation_id" in list(char_info):
                        print(char_info)
                        u = UserDB(uid=slovar['id'], name=slovar['name'], c_id=char_info.corporation_id)
                        db.session.add(u)
                        db.session.commit()
            counter += proc_value
    r.mset({'current': 0})
    r.mset({'max': 100})

    return convert_to_tranq_post(cid_list), cid_list, total_query


def get_chars_from_local(data: str):  # возвращает ID перс. из локала, преобразует их в формат ПОСТ запроса
    #  на входе строка из имён
    raw_data = list(set([i for i in data.replace('\r', '').split('\n') if len(i) > 0]))
    print(f'before conversion: {raw_data}')
    request_data = []
    exist_data = []
    cid_list = []
    data = []
    for name in raw_data:
        user = UserDB.query.filter(UserDB.name == name).first()
        if user is None:
            request_data.append(name)

        else:
            exist_data.append(name)
            print(user.name, user.uid)

    data = convert_to_tranq_post(request_data)  # преобразование в формат пост запроса сервера. передаётся список
    # неизвестных имён
    # запрос у сервера, передаётся список имён, в ответ UID
    if len(request_data) > 0:
        uid_data_req = requests.post('https://esi.evetech.net/latest/universe/ids/', headers=headers, params=params,
                                     data=data).json()
        print(f'total requests from server {len(uid_data_req)}')
    else:
        uid_data_req = []
    # print(f'server answer universe IDs {uid_data}')
    if 'characters' in uid_data_req:
        for slovar in uid_data_req['characters']:
            cid_list.append(slovar['id'])
            u = UserDB(uid=slovar['id'], name=slovar['name'])
            db.session.add(u)
            db.session.commit()

    if len(exist_data) > 0:
        print(f'total requests from DB {len(exist_data)}')
        for name in exist_data:
            user = UserDB.query.filter(UserDB.name == name).first()
            cid_list.append(user.uid)

    if len(cid_list) > 0:
        return convert_to_tranq_post(cid_list)
    else:
        return False


def aff_new(charid: list):
    # this func makes affilation swagger style response  char affilation
    aff_list = []
    for uid in charid:
        char_data = UserDB.query.filter(UserDB.uid == uid).first()

        if char_data is not None:
            if char_data.a_id is None:
                aff_list.append({'character_id': int(uid), 'corporation_id': int(char_data.c_id)})
            else:
                aff_list.append({
                    'alliance_id': int(char_data.a_id),
                    'character_id': int(uid),
                    'corporation_id': int(char_data.c_id)
                })
    return aff_list


def count_ally(char_affil: list):
    # dict for counting numbers
    common2 = {'alliances': {}, 'corporations': {}}
    with open("alliance_data.json", "r") as f:
        ally_data = json.load(f)  # dict for all alliances {'UID':name}
    with open("corp_data.json", "r") as f:
        corp_data = json.load(f)  # load corp datafile {UID:name}
    if 'error' in char_affil:
        return char_affil

    for dicts in char_affil:

        ally_flag = False
        for k, v in dicts.items():  # k, for key ally or corp and v for UID value of both
            if k == 'alliance_id':
                ally_info = get_alliance_info(v) if str(v) not in ally_data else None

                uid, ally_uid = v, v
                v = ally_data.setdefault(str(v),
                                         f'{ally_info.name} [{ally_info.ticker}]' if str(v) not in ally_data else None)
                # check for UID in global dict, return if TRUE, add if False

                name, ticker = find_ticker(v)
                common2['alliances'].setdefault(uid, {'Name': name.strip(), 'Ticker': ticker, 'count': 0})
                common2['alliances'][uid]['count'] += 1


                ally_flag = True

            elif k == 'corporation_id' and ally_flag:
                corp_info = get_corporation_info(v) if str(v) not in corp_data else None
                uid = v

                v = corp_data.setdefault(str(v),
                                         f'{corp_info.name}  [{corp_info.ticker}]' if str(v) not in corp_data else None)
                name, ticker = find_ticker(v)

                common2['corporations'].setdefault(uid, {'Name': name.strip(), 'Ticker': ticker, 'count': 0, 'ally_uid': ally_uid})
                common2['corporations'][uid]['count'] += 1


            elif k == 'corporation_id':


                uid = v
                noa = 000000
                common2['alliances'].setdefault(noa, {'Name': 'No alliance', 'Ticker': 'NoA', 'count': 0})
                common2['alliances'][noa]['count'] += 1
                v = corp_data.setdefault(str(v),
                                         f'{get_corporation_info(v).name}  [{get_corporation_info(v).ticker}]' if str(
                                             v) not in corp_data else None)
                name, ticker = find_ticker(v)
                common2['corporations'].setdefault(uid, {'Name': name.strip(), 'Ticker': ticker, 'count': 0, 'ally_uid': noa})
                common2['corporations'][uid]['count'] += 1


    # res = len(common['alliance'])
    # if 'No alliance' in common['alliance']:
    #     res -= 1

    common2['total'] = len(common2['alliances'])
    common2['total_corps'] = len(common2['corporations'])
    common2['total_chars'] = len(char_affil)


    with open("alliance_data.json", "w") as f:
        json.dump(ally_data, f)
    with open("corp_data.json", "w") as f:
        json.dump(corp_data, f)

    url = uuid.uuid4().hex
    common2['url'] = url
    u = ShipDB(data=json.dumps(common2), url=url)
    db.session.add(u)
    db.session.commit()

    return common2


def count_ships(result: list) -> dict:
    ships_common = {'ships_total': {}, 'ships_useful': {},'types_total': {}, 'url': {}}
    with open('data.json', 'r', encoding='utf-8') as file:
        ships = json.load(file)
    print("result is", result)
    for scan_line in result:
        if scan_line[0].isdigit():
            uid = scan_line[0]
            ship_name = scan_line[1]
            ship_type = scan_line[2]
            ships_common['ships_total'].setdefault(ship_type, [0, uid])
            ships_common['ships_total'][ship_type][0] += 1
            for key in ships.keys():

                if scan_line[2] in ships[key]:
                    ships_common['types_total'].setdefault(key, 0)
                    ships_common['types_total'][key] += 1
                    ships_common['ships_useful'].setdefault(ship_type, [0, uid])
                    ships_common['ships_useful'][ship_type][0] += 1
                    break

    url = uuid.uuid4().hex
    ships_common['url'] = url
    u = ShipDB(data=json.dumps(ships_common), url=url)
    db.session.add(u)
    db.session.commit()

    print(ships_common)

    return ships_common


def find_ticker(string):
    ticker = re.findall(r'([[a-zA-Z\d_.<>-]+])', string)
    name = re.sub(r'\[.+\]', '', string)
    if len(ticker) == 0:
        ticker = '[NOTICKER]'
    return name, "".join(ticker)
