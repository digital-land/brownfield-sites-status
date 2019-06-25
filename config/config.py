# -*- coding: utf-8 -*-
import json
import os


class Config(object):
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.getenv('SECRET_KEY')
    STATUS_API = os.getenv('STATUS_API', 'https://vuhjywgzu1.execute-api.eu-west-2.amazonaws.com/dev/status')


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
