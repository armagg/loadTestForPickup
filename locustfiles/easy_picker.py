import os
import sys

from locust import HttpLocust, task, seq_task, TaskSequence

sys.path.append(os.getcwd())
from common.data_save import *

data = Data()
config = config_loader()
api_addresses = load_yaml(config['api_file'])
api_addresses = api_addresses['fulfillment']
debug_mode = config['debug_mode']


class ObviousMindSet(TaskSequence):
    token: str

    def on_start(self):
        if debug_mode:
            print('on start...')
        user_credentials = data.get_one_user()
        self.login(user_credentials)
        self.first_pick()

    def login(self, user_credentials):
        if debug_mode:
            print('login...')
        response = self.client.post(url=api_addresses['login'], data={'email': user_credentials.username,
                                                                      'password': user_credentials.password})
        json_response = response.json()

        if response.status_code != 200:
            response.failure()
        self.token = json_response['token']

    def first_pick(self):
        if debug_mode:
            print('first pick')
        self.header = {'X-Auth-Key': self.token}
        response = self.client.post(url=api_addresses['get_first_step'], headers=self.header)
        response_json = response.json()
        if response.status_code != 200:
            response.failure()
        else:
            self.next_pickup_list_id = response_json['pickupListId']

    @seq_task(1)
    @task(1)
    def get_serial(self):
        if debug_mode:
            print('getting serial')
        response = self.client.post(url=api_addresses['get_serial'], headers=self.header,
                                    data={'pickupListId': self.next_pickup_list_id})
        print(response.json())
        if response.status_code != 200:
            response.failure()
        else:
            self.serial = response.json()['serial']

    @seq_task(2)
    @task(1)
    def add_serial(self):
        if debug_mode:
            print('add serial')
        response = self.client.post(url=api_addresses['register_item'], headers=self.header,
                                    data={'action': 'add', 'serial': self.serial})
        print(response.json())
        print('ghabl: ' + str(self.next_pickup_list_id))
        response = self.client.post(url=api_addresses['confirm'], headers=self.header)
        self.next_pickup_list_id = response.json()['pickupListId']
        print('bad: ' + str(self.next_pickup_list_id) + ' javab e server ' + str(response.json()['pickupListId']))


class EasyPicker(HttpLocust):
    task_set = ObviousMindSet
    min_wait = 5000
    max_wait = 5000
