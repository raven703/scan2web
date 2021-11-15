def get_alliance_info(a_id):
    get_alliance1 = app.op['get_alliances_alliance_id'](
        alliance_id=a_id,
        datasource='tranquility',
    )
    return client.request(get_alliance1).data



def get_corporation_info(c_id):
    get_corporation = app.op['get_corporations_corporation_id'](
        corporation_id=c_id,
        datasource='tranquility',
    )
    response=client.request(get_corporation).data
    return response

def get_char_info(c_id):
    get_char = app.op['get_characters_character_id'](
        character_id =c_id,
        datasource='tranquility',
    )
    response=client.request(get_char).data
    return response

def convert_to_tranq_post(data): #convert to Tranq POST string format ex. [ "96667530", "93503913" ]
    result = '['
    for name in data:
        result = result + ' "' + str(name) + '",'
    result = result.strip(',') + ' ]'
    return result


def get_chars_from_local(filename): # возвращает ID перс. из локала, преобразует их в формат ПОСТ запроса
    with open(filename) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    data = convert_to_tranq_post(data)
    data = requests.post('https://esi.evetech.net/latest/universe/ids/', headers=headers, params=params,
                             data=data).json()
    cid_list = []
    for names in data['characters']:
        for cid in names:
            cid_list.append(names[cid])
            break

    return convert_to_tranq_post(cid_list)

def count_ally(char_affil):
    common = {'alliance': {}, 'corporation': {}}   # dict for counting numbers
    with open("alliance_data.json", "r") as f:
        ally_data = json.load(f)  # dict for all alliances {'UID':name}
    with open("corp_data.json", "r") as f:
        corp_data = json.load(f)  #load corp datafile {UID:name}


    for dicts in char_affil:
        for k, v in dicts.items():  #k, for key ally or corp and v for UID value of both
            if k == 'alliance_id':
                v = ally_data.setdefault(str(v), f'{get_alliance_info(v).name} [{get_alliance_info(v).ticker}]')  #check for UID in global dict, return if TRUE, add if False
                common['alliance'].setdefault(v, 0)  #count entries, total {UID: count} ex. {99007629: 2}
                common['alliance'][v] += 1           #count entries
            elif k == 'corporation_id':
                v = corp_data.setdefault(str(v), f'{get_corporation_info(v).name}  [{get_corporation_info(v).ticker}]')
                common['corporation'].setdefault(v, 0)
                common['corporation'][v] += 1

    with open("alliance_data.json", "w") as f:
        json.dump(ally_data, f)
    with open("corp_data.json", "w") as f:
        json.dump(corp_data, f)


    return common