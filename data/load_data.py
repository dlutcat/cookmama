#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torndb
import yaml

db = torndb.Connection(
    host='192.168.0.186:34891', database='cookmama',
    user='wjun', password='UmkVpysZnsOh9hucwG22')

def load_db():
    stream = file('data.yaml', 'r') 
    o = yaml.load(stream)

    for item in o['items']:
        sql = "insert into item (name, img, description) values ('%s', '%s', '%s')" \
                    % (item['name'], item['img'], item['desc']) 
        db.execute(sql)

    for shop in o['shops']:
        db.execute("insert into shop (name, description, tel1, tel2, tel3) values ('%s', '%s', '%s', '%s', '%s')" \
                    % (shop['name'], shop['desc'], shop['tel1'], shop['tel2'], shop['tel3']))

if __name__ == '__main__':
    load_db()
