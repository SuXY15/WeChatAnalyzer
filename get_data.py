#coding=utf-8
import itchat
import os, sys, time
import json, codecs, requests

message_dict = {
    "test":   "Fucking test!",
    "hello":  "Hello!",
    "bye":    "Bye~"
}
image_dir = "./images/"
json_name = "./data/friends.json"


# downloading head images
def download_images(frined_list):
    for friend in frined_list:
        image_name = image_dir+friend['UserName']+'.jpg'
        if not os.path.isfile(image_name):
            print("Downloading head image of %s"%friend['NickName'])
            img = itchat.get_head_img(userName=friend["UserName"])
            with open(image_name, 'wb') as file:
                file.write(img)

# save some data
def save_data(frined_list):
    friends_save = []
    for friend in frined_list:
        friends_save.append({
            'NickName':   friend['NickName'],
            'HeadImgUrl': friend['HeadImgUrl'],
            'Sex':        friend['Sex'],
            'Province':   friend['Province'],
            'Signature':  friend['Signature'],
            'UserName':   friend['UserName']
            })
    with codecs.open(json_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(frined_list))#,ensure_ascii=False))

# auto reply
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    name = msg['User']['NickName']
    user = itchat.search_friends(name=name)[0]
    text = msg['Text']

    if text in message_dict.keys():
        user.send(message_dict[text])
    else:
        user.send(u"Sorry, %s, I can't reply this now."%name)

# main
if __name__ == '__main__':
    itchat.auto_login()
    
    print("Loading wechat data...")
    friends_list = itchat.get_friends(update=True)[0:]#获取好友信息

    print("Loaded. Start saving json data...")
    save_data(friends_list)

    print("Saved. Start downlaoding images...")
    download_images(friends_list)

    user = itchat.search_friends(name=u'SEE and SING')[0]
    user.send(u'Hello, this is a message from wechat robot.')
    itchat.run()
