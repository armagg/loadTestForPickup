import common.data as data
from dotenv.main import load_dotenv
import os
import requests as r
from enum import Enum

dev_username: str = ''
dev_password: str = ''
config = data.config_loader()


class Panels(Enum):
    ADMIN = 'admin'
    FULFILMENT = 'fulfillment'


def argument_adder(*args):
    string = '%20'
    for arg in args:
        string += str(arg) + '%20'
    return string[:-3]


def call_dev(number, prefix):
    address = config['dev_addresses'][Panels.ADMIN.value]

    response = r.get(address + config[
        Panels.ADMIN.value + '_command'] + '/' + config['admin_command']['number_of_users'] +
                     argument_adder(prefix, number),
                     auth=(dev_username, dev_password))
    if response.status_code == 200:
        print(response.json()['message'])
        print('starting to assign to locations')

    else:
        if response.status_code == 404:
            print(response.json()['message'])
            create_user(0, number, prefix)
        else:
            print(response.json()['message'])
            begin = response.json()['valid_number']
            create_user(begin - 1, number, prefix)


def create_user(begin, end, prefix):
    from common.data import Data
    data = Data()
    address = config['dev_addresses'][Panels.ADMIN.value]
    address = address + config['admin_command']['create_user']
    for i in range(begin, end):
        username = prefix + str(i) + '@pickup.test'
        password = prefix + str(i)
        phone = '98930' + str(i)
        data.add_one_user(username, password)
        r.get(
            address + argument_adder(username, password, phone),
            auth=(dev_username, dev_password))
    data.save_data_added()
    data.end()


def create_privileges_for_prefix(prefix):
    address = config['dev_addresses'][Panels.FULFILMENT.value] + config[Panels.FULFILMENT.value + '_command'][
        'create_privileges']
    response = r.get(url=address + argument_adder(prefix), auth=(dev_username, dev_password))
    if response.status_code == 200:
        return True
    return False


def set_credentials():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(root_dir)
    load_dotenv(os.path.join(project_folder, '.env'))
    global dev_username
    global dev_password
    try:
        dev_username = os.environ['dev_username']
        dev_password = os.environ['dev_password']
        return True
    except KeyError:
        print('please set environments variables at first')
        return False


def get_credentials():
    return dev_username, dev_password


def prepare_warehouse_for_pickup():
    import time
    set_credentials()
    number_of_testers = int(input('how many testers do you want? '))
    prefix = input('whats the prefix of them emails ? ')
    create_user(0, number_of_testers, prefix)
    print('waiting for syncing with admin')
    time.sleep(20)
    if create_privileges_for_prefix(prefix):
        print('privileges created')
        time.sleep(5)
        print('now you are ready to pick')
    else:
        print('some bad thing occurred!! :(')
        exit(0)
