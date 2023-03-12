import requests
import json

SERVER_TOKEN = 'AAAAtWZ-gqg:APA91bGmROXVWr39ey57YJw7fKIBKTdigmf2NRjlZ1_nE7BCCVCZ57KmDNXnzM9v6_AqAN1RYvMAZkF8blbmEvSMfifhpLvdJ3TgkJrGjGsntBQFvwrF23tI_H1y0xcjHE9tHk2-bg0c'
class Firebase:
    def __init__(self):
        pass

    def send(self,registrations_ids, message):
        fields = {
            # 'registration_ids' : registrations_ids,
            'to' : registrations_ids,
            'data' : message,
        }
        return self.send_push_notification(fields)

    def send_push_notification(self,fields):
        # firebase server url to send the curl request
        url = 'https://fcm.googleapis.com/fcm/send'

        # building headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + SERVER_TOKEN,
        }

        # body = {
        #         'notification': {'title': 'Sending push form python script',
        #                             'body': 'New Message'
        #                             },
        #         'to':
        #             deviceToken,
        #         'priority': 'high',
        #         #   'data': dataPayLoad,
        #         }
        # data = {
        #     "registration_ids": "dQDHpqOsS-SSl7Ry8x4C5d:APA91bEVk38hVSWpl3k9iIQCMb732lW_VRo0ji9NU_0cIdW5MbzUZUP-bXsmpCe21LPW2eUeZAUk18bF-twmUJx0RJ3tCvgqg0La7ArCXDP8iWV7AXhzELsEdWFwz19C7KrquLbPrCc9", 
        #     "data": 'nothing'}

        data = json.dumps(fields)
        response = requests.post(url,headers=headers, data=data,)

        # print(response)
        # print(response.status_code)

        return True