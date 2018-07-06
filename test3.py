#!/usr/bin/python
# coding=utf-8
#

import velocloud;
from velocloud.rest import ApiException
import urllib3

urllib3.disable_warnings()
velocloud.configuration.verify_ssl = False
client = velocloud.ApiClient(host="172.18.6.250")
api = velocloud.AllApi(client) 


def check_velocloud_api():

    urllib3.disable_warnings()
    velocloud.configuration.verify_ssl = False
    client = velocloud.ApiClient(host="172.18.6.250")
    client.authenticate('super@velocloud.net', 'vcadm!n', operator=True)
    api = velocloud.AllApi(client)
 
    try:
        response = api.systemPropertyGetSystemProperties({"group" : "vco"})
    except:
        return False

    return response


def wait_for_api(sleep_time=24):
    status_poll_count = 0
    while status_poll_count < 30:
        api_status = check_velocloud_api()
        if api_status:
            return True
        else:
            status_poll_count += 1
            time.sleep(sleep_time)

        if status_poll_count == 30:
            return False


wait_for_api()


