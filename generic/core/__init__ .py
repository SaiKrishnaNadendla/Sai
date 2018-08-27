from generic import yaml_obj, browser, BeautifulSoup, re, urlparse, dparser, parse, datetime, traceback
from generic import sys , time , hashlib , smtplib , MIMEMultipart , MIMEText 
import pytesseract
#import dryscrape
from PIL import Image, ImageFilter
from StringIO import StringIO
from generic.generic_forum_scraper import forum
from sqlalchemy.orm import sessionmaker
from models import Topic, Post, ThreadLastpage
import os
import base64
import webbrowser

#For reCaptcha using selenium required below modules, and also time, BeautifulSoup required which are imported above
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
