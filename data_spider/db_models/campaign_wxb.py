#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-17 13:18
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os
import logging
import logging.config
import datetime as dt
from datetime import  datetime
from data_spider.conf import settings 
from data_spider.common.decorator import  mongo_exception

class CampaignWXB(object):

    _conn = settings.mongoConn
    coll = _conn['data_center']['campaign_wxb']


    @classmethod
    def __get_id(cls,campaign,rpt_date):
        return hash(str(rpt_date)+str(campaign))

    @classmethod
    @mongo_exception
    def is_exist(cls,campaign,rpt_date):
        isv = cls.coll.find_one({'_id':cls.__get_id(campaign,rpt_date)})
        if isv is None:
            return False
        else:
            return True

    @classmethod
    @mongo_exception
    def upset_campaign_wxb(cls,obj_dict):
        id = cls.__get_id(obj_dict["campaign"],obj_dict["rpt_date"])
        filter = {'_id':id}
        if obj_dict.has_key('_id'):
            del shop_dict['_id']
        cls.coll.update(filter, {'$set':obj_dict}, upsert=False)

    @classmethod
    @mongo_exception
    def insert_campaign_wxb(cls,obj_dict):
        id = cls.__get_id(obj_dict["campaign"],obj_dict["rpt_date"])
        obj_dict.update({'_id':id})
        cls.coll.save(obj_dict)

    @classmethod
    @mongo_exception
    def upsert_campaign_wxb_list(cls,data_list):
        for data in data_list:
            if cls.is_exist(data["campaign"],data["rpt_date"]):
                cls.upset_campaign_wxb(data)
            else:
                cls.insert_campaign_wxb(data)

