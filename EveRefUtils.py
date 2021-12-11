import requests
import tarfile
import time
import random
import json
from utils import getFilesInDir, getJsonFromURL, get_list_of_past_dates, call_and_retry

def update_data(nDays, data_dir):
    dates = get_list_of_past_dates(nDays)
    download_km_files_for_dates(dates, data_dir)
    check_eventual_updates_of_files(dates, data_dir)

def check_eventual_updates_of_files(date_list, data_dir):   #to be run after download_km_files_for_dates()
    totals = call_and_retry(getJsonFromURL, 3, [3, 6, 9], 'https://data.everef.net/killmails/totals.json')

    for d in date_list:
        filename = from_date_to_filename(d)
        n_km_server = totals[d.replace('-', '')]
        n_km_local = len(tar_to_json_list(data_dir + filename))
        print(d, n_km_server, n_km_local)
        if n_km_server != n_km_local:
            print(filename + ' needs to be updated...')
            year = d.split('-')[0]
            #download_killmail_file('https://data.everef.net/killmails/' + str(year) + '/' + filename, data_dir)
            call_and_retry(download_killmail_file, 3, [3, 6, 9], 'https://data.everef.net/killmails/' + str(year) + '/' + filename, data_dir)



def download_km_files_for_dates(date_list, data_dir):
    for d in date_list:
        filename = from_date_to_filename(d)

        if filename not in getFilesInDir(data_dir):
            year = d.split('-')[0]
            #download_killmail_file('https://data.everef.net/killmails/' + str(year) + '/' + filename, data_dir)
            call_and_retry(download_killmail_file, 3, [3, 6, 9], 'https://data.everef.net/killmails/' + str(year) + '/' + filename, data_dir)

def from_date_to_filename(date_str):
    '''
    date string YYYY-MM-DD
    '''

    return 'killmails-' + str(date_str) + '.tar.bz2'

def download_killmail_file(url, folderDest):
    print('downloading ' + url + '...')

    filename = url.split('/')[-1:][0]

    r = requests.get(url)
    with open(folderDest + filename, 'wb') as outfile:
        outfile.write(r.content)

    wait_random_time(2, 4)

    try_open_tar(folderDest + filename)

    print('file could be opened')

def try_open_tar(filepath):  #hopefully raises exception if tar file cannot be opened
    tarFile = tarfile.open(filepath)

    tarFile.close()

def wait_random_time(min, max):
    r = random.randint(min, max)
    time.sleep(r)

def tar_to_json_list(filepath):
    '''
    one obj is like this:
    {'attackers': [{'character_id': 2116994446, 'corporation_id': 1000077, 'damage_done': 418, 'final_blow': True, 'security_status': -9.8, 'ship_type_id': 37456, 'weapon_type_id': 2456}], 'killmail_id': 97089202, 'killmail_time': '2021-12-03T00:00:03Z', 'solar_system_id': 30002698, 'victim': {'alliance_id': 99011119, 'character_id': 2119389324, 'corporation_id': 98653975, 'damage_taken': 418, 'items': [], 'position': {'x': 118558541401.56458, 'y': 107336153104.47194, 'z': -126501511174.7286}, 'ship_type_id': 670}, 'killmail_hash': 'ca4aa23be88aed1fe8c5acd092c86bc4c3d17629', 'http_last_modified': '2021-12-03T11:37:14Z'}
    '''
    km_list = []

    tarFile = tarfile.open(filepath)
    members = tarFile.getmembers()

    for m in members:
        member_as_file_object = tarFile.extractfile(m)
        member_as_string = member_as_file_object.read().decode('utf-8')
        member_as_json = json.loads(member_as_string)

        km_list.append(member_as_json)

    tarFile.close()

    return km_list

def extract_ch_ids_from_killmail(km_obj):
    ch_ids = []

    for a in km_obj['attackers']:
        if 'character_id' in a:
            ch_ids.append(a['character_id'])

    if 'character_id' in km_obj['victim']:
        ch_ids.append(km_obj['victim']['character_id'])

    return ch_ids

