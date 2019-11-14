from locust import HttpLocust, TaskSet, task, seq_task, TaskSequence
from common.data_save import *
import sys

sys.path.append(os.getcwd())

data = Data()
config = config_loader()
api_addresses = load_yaml(config['api_file'])
api_addresses = api_addresses['fulfillment']


class ObviousMindSet(TaskSequence):

    def on_start(self):
        self.user_credentials = data.get_one_user()

    @seq_task(1)
    @task(1)
    def login(self):
        response = self.client.post(url=api_addresses['login'], data={'email': self.user_credentials.username,
                                                                      'password': self.user_credentials.password}).json()



class EasyPicker(HttpLocust):
