import os
import sys
from typing import Dict

from locust import HttpLocust, task, seq_task, TaskSequence

sys.path.append(os.getcwd())

from common.data import *
from common.commands_call import prepare_warehouse_for_pickup

config = config_loader()
api_addresses = load_yaml(config['api_file'])
api_addresses = api_addresses['fulfillment']
debug_mode = config['debug_mode']
prepare_warehouse_for_pickup()

data = Data()


def create_new_orders():
    pass


class ObviousMindSet(TaskSequence):
    serial: list
    next_pickup_list_id: object
    header: Dict[str, str]
    does_it_end: bool
    token: str

    def on_start(self):
        if debug_mode:
            print('on start...')
        user_credentials = data.get_one_user()
        self.does_it_end = False
        self.login(user_credentials)
        self.first_pick()

    def login(self, user_credentials):

        if debug_mode:
            print('login...')
        response = self.client.post(url=api_addresses['login'], data={'email': user_credentials.username,
                                                                      'password': user_credentials.password})
        json_response = response.json()

        self.token = json_response['token']

    def first_pick(self):
        if debug_mode:
            print('first pick')
        self.header = {'X-Auth-Key': self.token}
        response = self.client.post(url=api_addresses['get_first_step'], headers=self.header)
        response_json = response.json()
        print(response.json())
        if response.status_code != 200:
            response.failure()
        else:
            self.next_pickup_list_id = response_json['pickupListId']

    @seq_task(1)
    @task(1)
    def get_serial(self):
        if self.does_it_end:
            pass
        if debug_mode:
            print('getting serial')
        response = self.client.post(url=api_addresses['get_serial'], headers=self.header,
                                    data={'pickupListId': self.next_pickup_list_id})
        if response.status_code != 200:
            if response.status_code == 422:
                create_new_orders()
        else:
            self.serial = response.json()['serial']

    @seq_task(2)
    @task(1)
    def add_serial(self):
        if self.does_it_end:
            pass
        if debug_mode:
            print('add serial')
        for i in self.serial:
            response = self.client.post(url=api_addresses['register_item'], headers=self.header,
                                        data={'action': 'add', 'serial': i})
            if 'remainingCount' in response.json() and response.json()['remainingCount'] == 0:
                break

        response = self.client.post(url=api_addresses['confirm'], headers=self.header)
        try:
            self.next_pickup_list_id = response.json()['pickupListId']
        except KeyError:
            self.does_it_end = True


class EasyPicker(HttpLocust):
    task_set = ObviousMindSet
    min_wait = 5000
    max_wait = 5000
