from dotenv.main import load_dotenv
import os
import requests as r
from enum import Enum

dev_username: str = None
dev_password: str = None


class Panels(Enum):
    ADMIN = 'admin'
    FULFILMENT = 'fulfillment'


def argument_adder(*args):
    string = ''
    for arg in args:
        string += str(arg) + '%20'
    return string


def call_dev(panel: Panels, number, prefix):
    import common.data_save as data
    config = data.config_loader()
    address = config['dev_address'][panel.value]
    if panel == Panels.ADMIN:
        response = r.get(address + config[
            panel.value + '_command'] + '/' + config['admin_command']['number_of_users'] + argument_adder(prefix,
                                                                                                          number),
                         auth=(dev_username, dev_password))
        if response.status_code == 200:
            print(response.json()['message'])
            print('starting to assign to locations')
            pass
        else:
            address = address + config['admin_command']['create_user']
            if response.status_code == 404:
                print(response.json()['message'])
                create_specific_user(address, 0, number, prefix)
            else:
                print(response.json()['message'])
                begin = response.json()['valid_number']
                create_specific_user(address, begin - 1, number, prefix)


def create_specific_user(address, begin, end, prefix):
    for i in range(begin, end):
        r.get(address + argument_adder(prefix + str(i) + '@pickup.test', prefix + str(i), '98930' + str('%7d' % i)),
              auth=(dev_username, dev_password))


def set_credentials():
    project_folder = os.path.expanduser('~/PycharmProjects/loadTestForPickup')
    load_dotenv(os.path.join(project_folder, '.env'))
    global dev_username
    global dev_password
    try:
        dev_username = os.environ['dev_username']
        dev_password = os.environ['dev_password']
        print(dev_password, dev_username)
        return True
    except KeyError:
        print('please set environments variables at first')
        return False


def get_credentials():
    print(dev_username, dev_password)


def create_enough_admins():
    number_of_testers = input('how many testers do you want? ')
    prefix = input('whats the prefix of them emails ? ')
    call_dev(Panels.ADMIN, number_of_testers, prefix)
