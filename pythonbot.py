import json
import requests
import time
import urllib

import config


TOKEN = "400866113:AAGyNu4QY2Z_NG--sbN3L8OoTdTnv-_GC2k"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js
                      
def getUserCount(chat_id):
    url = URL + "getChatMembersCount?chat_id={}".format(chat_id)
    js = get_json_from_url(url)
    user_count = js["result"]
    return(user_count)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def delete_message(message_id, chat_id):
    url = URL + "deleteMessage?message_id={}&chat_id={}".format(message_id, chat_id)
    get_url(url)

    
def main():
    update_ids        = []
    active_user_ids   = []
    active_message_id = []
    active_user_count = 0
    chat_id = -1001215801011
    in_id_list = 0
    last_update_id = None
    updates = get_updates(last_update_id)
    user_count = getUserCount(chat_id)
    while True:
        updates = get_updates(last_update_id)
        user_count = getUserCount(chat_id)
        if len(updates["result"]) > 0:
            for update in updates["result"]:
                try:
                    in_id_list = 0
                    user_id = int(update["message"]["from"]["id"])
                    message_id = int(update["message"]["message_id"])
                    update_id = int(update["update_id"])
                    for users in range(len(active_user_ids)):
                            if(int(user_id) == active_user_ids[users]):
                                in_id_list = 1
                                if(message_id > active_message_id[users]):                            
                                    delete_message(active_message_id[users], chat_id)
                                    active_message_id[users] = message_id
                                    update_ids[users] = int(update["update_id"])
                    if(in_id_list==0):
                        active_user_ids.append(int(user_id))
                        active_message_id.append(int(message_id))
                        update_ids.append(int(update["update_id"]))
                    last_update_id = max(update_ids)
                except KeyError:
                    pass
                    #mostly just for edited messages
                    #todo
        else:
            Time.sleep(.5)


if __name__ == '__main__':
    main()
