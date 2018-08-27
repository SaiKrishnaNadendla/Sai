import re
import os
import sys
import urlparse
import uuid
import logging
import threading
import time
import mechanize
import cookielib
import yaml
import argparse
import importlib
import generic_initialize_db
import dateutil.parser as dparser #to get date from a string, multiple strings ,today,tomorrow
import traceback
import MySQLdb
#import dryscrape
import urllib2
import smtplib
from email import MIMEMultipart
from email import MIMEText
# User-Agent Rotation Manually
from random import choice
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import sessionmaker
from models import Topic, Post, ThreadLastpage, Binaries,Archive
from sqlalchemy.exc import IntegrityError
from Queue import Queue
from threading import Thread
from dateparser import parse
import ssl
import yaml

ssl._create_default_https_context = ssl._create_unverified_context
YAML_OBJ = None
with open(r'settings.yaml', 'r') as stream:
    try:
        YAML_OBJ = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise

parser = argparse.ArgumentParser()
parser.add_argument("forum", help="Give forum value from setting.py file like Forum_1",
                    type=str)
parser.add_argument("-r", "--rawhtml", help="Store raw html pages",
                    action="store_true")
parser.add_argument("-d", "--debug", help="Used to developers debug mode enable",
                    action="store_true")
args = parser.parse_args()

if args.forum:
    forum = args.forum

#print " Tor_used  " , YAML_OBJ.get(forum).get('Tor_used')
if YAML_OBJ.get(forum).get('Tor_used') :
    import socks
    import socket
    def create_connection(address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

    # patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

if YAML_OBJ.get(forum).get('httpreq') :
    import httplib
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# Initialize browser.
browser = None
if YAML_OBJ.get(forum).get('loginissue') :
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
else :
    browser = mechanize.Browser()
browser.set_handle_robots(False)

#pool of user-agents
desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
# browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
userAgent = choice(desktop_agents)
print "userAgent is ::", userAgent 
browser.addheaders = [('User-Agent', userAgent ),
       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
       ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
       ('Accept-Encoding', 'none'),
       ('Accept-Language', 'en-US,en;q=0.8'),
       ('Connection', 'keep-alive')]
cj = cookielib.CookieJar()
browser.set_cookiejar(cj)
