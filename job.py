import datetime
import json
import time

file_path = 'keyStoreFile-1.json'
job_frequency = 5  # in seconds


def key_cleanup():

    with open(file_path) as json_file:
        json_data = json.load(json_file)

    for obj in json_data['keys']:
        if obj['keyExpired'] == 'Y':
            continue
        expire_date = datetime.datetime.strptime(
            obj['keyCreatedTime'], '%m-%d-%y-%H%M') + datetime.timedelta(0, int(obj['TimeToLive']))

        if expire_date < datetime.datetime.now():
            obj['keyExpired'] = 'Y'

    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def main():
    while True:
        key_cleanup()
        time.sleep(job_frequency)


main()
