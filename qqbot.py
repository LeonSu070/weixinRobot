#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json
import hashlib
import collections


class QQWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.qqbot_key = ""
        self.qqbot_appid = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('qqconf.ini')
            self.qqbot_key = cf.get('main', 'key')
            self.qqbot_appid = cf.get('main', 'appid')
        except Exception:
            pass
        print 'qqbot_key:', self.qqbot_key

    def qqbot_auto_reply(self, uid, msg):
        if self.qqbot_key:
            url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
            user_id = uid.replace('@', '')[:30]
            params = {
                'app_id': self.qqbot_appid,
                'session': user_id,
                'question': msg.encode('utf8'),
                'time_stamp': str(int(time.time())),
                'nonce_str': str(random.randint(1, 9999999999)),
            }

            params['sign'] = self.get_req_sign(params)
            r = requests.post(url, data=params)
            respond = json.loads(r.text)
            result = respond['data']['answer']
            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def get_req_sign(self, params):
        params = sorted(params.items())
        str = urllib.urlencode(params)
        str += '&app_key=' + self.qqbot_key
        m = hashlib.md5()
        m.update(str)
        sign = m.hexdigest().upper()
        return sign

    def auto_switch(self, msg):
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            msg_data = msg['content']['desc']
            to_use_id = msg['user']['id']
        else:
            msg_data = msg['content']['data']
            to_use_id = msg['to_user_id']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', to_use_id)
        else:
            print msg_data
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', to_use_id)

    def handle_msg_all(self, msg):
        if self.DEBUG:
            print("bot.py, handle_msg_all, line 69", msg)
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(self.qqbot_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(msg['user']['id'], self.my_account['UserName'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    #if detail['type'] == 'at':
                    for k in my_names:
                        #if my_names[k] and my_names[k] == detail['value']:
                        if my_names[k]:
                            i = detail['value'].find(my_names[k])
                            if i >= 0:
                                is_at_me = True
                                break
                if self.DEBUG:
                    print("bot.py, handle_msg_all, line 69", is_at_me)
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        self.auto_switch(msg)
                        if self.robot_switch:
                            reply += self.qqbot_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])


def main():
    bot = QQWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()

