import requests
import sys, os
from locust import HttpLocust, TaskSet, task, seq_task, TaskSequence

sys.path.append(os.getcwd())
from common.data_save import *
import sys

data = LoadData()
config = config_loader()
api_addresses = load_yaml(config['api_file'])
api_addresses = api_addresses['fulfillment']


class ObviousMindSet(TaskSequence):
    token: str

    def on_start(self):
        user_credentials = data.get_one_user()
        self.login(user_credentials)

    def login(self, user_credentials):
        response = self.client.post(url=api_addresses['login'], data={'email': user_credentials.username,
                                                                      'password': user_credentials.password})
        json_response = response.json()

        if response.status_code != 200:
            response.failure()
        self.token = json_response['token']

    @seq_task(1)
    def first_pick(self):
        self.header = {'X-Auth-Key': self.token}
        response = self.client.post(url=api_addresses['get_first_step'], header=self.header)


class EasyPicker(HttpLocust):
    task_set = ObviousMindSet
    min_wait = 1000
    max_wait = 3000
