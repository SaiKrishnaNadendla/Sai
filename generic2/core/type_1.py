from generic.core import *
from generic.models import Post
# User-Agent Rotation Manually
from random import choice

# User agent pool/ We need to select each user-Agent at the time of request
desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
emailcount = 0
if YAML_OBJ.get(forum).get('Captcha').get('type'):
    if YAML_OBJ.get(forum).get('Jsload').get('tor_phantom'):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

        binary = FirefoxBinary(r"/tmp/mozilla_ityug0/tor-browser_en-US/Browser/firefox")
        # profile = FirefoxProfile(r"/home/vidyayug/Downloads/tor-browser_en-US/Browser/TorBrowser/Data/Browser/profile.default")
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)

        captchaBrowser = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)
    else:
        captchaBrowser = webdriver.Firefox()
    cj = cookielib.LWPCookieJar()
if YAML_OBJ.get(forum).get('Jsload').get('required') and not YAML_OBJ.get(forum).get('Jsload').get('tor_phantom'):
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',
                                 service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
if YAML_OBJ.get(forum).get('Jsload').get('required') and YAML_OBJ.get(forum).get('Jsload').get('tor_phantom'):
    driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',
                                 service_args=['--proxy=127.0.0.1:9050', '--proxy-type=socks5',
                                               '--ignore-ssl-errors=true', '--ssl-protocol=any'])
cookie_dict = {}


def user_authentication(url):
    """ User Authentication """
    l_meta = YAML_OBJ.get(forum).get('Meta').get('Login')
    l_det = YAML_OBJ.get(forum).get('Login')
    if not l_det.get('phantom'):
        # The site we will navigate into, handling it's session
        # response = browser.open(url)
        # browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
        userAgent = choice(desktop_agents)
        browser.addheaders = [('User-Agent', userAgent),
                              ('Accept', '*/*'),
                              ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                              ('Accept-Encoding', 'none'),
                              ('Connection', 'keep-alive')]
        response = None
        try:
            response = browser.open(url)
        except Exception as e:
            pass
        browser.addheaders = [('User-Agent', userAgent),
                              ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                              ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                              ('Accept-Encoding', 'none'),
                              ('Accept-Language', 'en-US,en;q=0.8'),
                              ('Connection', 'keep-alive')]
        try:
            response = browser.open(url)
            print "output is     ", BeautifulSoup(response.read(), 'html.parser')
        except Exception as e:
            logging.exception('exception e as  %s ' % e)
            pass

        # Select the first (index zero) form
        browser.select_form(nr=l_meta.get('f_num'))

        # User credentials
        if YAML_OBJ.get(forum).get('Login').get('required'):
            username = l_det.get('username')
            password = l_det.get('password')

            browser.form[l_meta.get('user')] = username
            browser.form[l_meta.get('pass')] = password

        # Captcha
        if YAML_OBJ.get(forum).get('Captcha').get('required'):
            filepath = '/data/Archives/captcha/'
            timestamp = str(time.time()).split('.')[0]
            imageType = 'png'
            if YAML_OBJ.get(forum).get('Captcha').get('imagetype'):
                imageType = YAML_OBJ.get(forum).get('Captcha').get('imagetype')
            filetimestamp = 'captcha' + timestamp + '.' + imageType
            filename = os.path.join(filepath, filetimestamp)
            c_meta = YAML_OBJ.get(forum).get('Meta').get('Captcha')
            c_det = YAML_OBJ.get(forum).get('Captcha')
            soup1 = BeautifulSoup(response.read(), 'html.parser')
            if YAML_OBJ.get(forum).get('Captcha').get('imagetag'):
                res = soup1.find_all(str(YAML_OBJ.get(forum).get('Captcha').get('imagetag')))[
                    int(YAML_OBJ.get(forum).get('Captcha').get('count'))].get(
                    YAML_OBJ.get(forum).get('Captcha').get('key'))
                if not YAML_OBJ.get(forum).get('Captcha').get('Image_url'):
                    res = res[res.find(",") + 1:]
                    imgdata = base64.decodestring(res)
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    print " take captch image from 52.89.227.115/captcha/%s" % (filetimestamp)
                    webbrowser.open(filename)
                else:
                    print " please access this url in browser  %s " % (
                                YAML_OBJ.get(forum).get('Captcha').get('addUrl') + str(res))
                try:
                    os.system("rsync -apv /data/Archives/captcha/ ityugrsync:/data/Archives/captcha/")
                except Exception  as e3:
                    logging.exception(" exception at file moving  %s " % e3)

                captchaStr = raw_input("Enter captcha Here ::")
                browser.form[c_meta.get('tag')] = str(captchaStr)

        # Login
        try:
            response = browser.submit()
        except Exception as e:
            print e
            if YAML_OBJ.get(forum).get('Login').get('required'):
                username = l_det.get('username')
                password = l_det.get('password')
                browser.add_password('url', username, password)
                response = browser.open(url)
            # print  " is add_password : " , response.read()
        return response.code
    else:
        driver.get(url)
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)
        time.sleep(30)
        element = YAML_OBJ.get(forum).get('Jsload').get('element')
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
        try:
            username = driver.find_element_by_name(l_meta.get('user'))  # l_det.get('username'))
            password = driver.find_element_by_name(l_meta.get('pass'))  # l_det.get('password'))

            # l_det.get('submitbn')
            username1 = l_det.get('username')
            password1 = l_det.get('password')
            username.send_keys(username1)
            password.send_keys(password1)
            password.send_keys(Keys.ENTER)
        except Exception as er1:
            print " exception at submition ", er1
        try:
            time.sleep(10)
            driver.find_element_by_css_selector(str(l_det.get('submitbn'))).click()
            time.sleep(20)
            Web_url = YAML_OBJ.get(forum).get('WEB_URL')
            if YAML_OBJ.get(forum).get('Meta').get('Forum').get('extention'):
                Web_url = Web_url + YAML_OBJ.get(forum).get('Meta').get('Forum').get('extention')

            driver.get(Web_url)
            wait = WebDriverWait(driver, 20)
            time.sleep(20)
            element = YAML_OBJ.get(forum).get('Jsload').get('element')
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
            # print " main code " , driver.page_source
            print " 1 \n "

        except Exception as e:
            print " exc ", e
        # print " if condition " , driver.page_source
        if l_det.get('username') in driver.page_source:
            try:
                print " auth ", (l_det.get('username') in driver.page_source)
                cookie = driver.get_cookies()
                number = 1
                for s_cookie in cookie:
                    cookie_dict1 = {}
                    for k in s_cookie.keys():
                        try:
                            if k == 'name' or k == 'value':
                                cookie_dict1[k] = s_cookie[k]
                        except Exception as e:
                            print " cookie dict exce ", e
                    # print " cookie dict ", cookie_dict
                    cookie_dict[str(number)] = cookie_dict1
                    number = number + 1
                print " cookie dict ", cookie_dict
                return 200
            except Exception as e:
                print " cookie work ", e
        else:
            return 0


def user_captcha_mechanize(url):
    """ User Authentication """
    l_meta = YAML_OBJ.get(forum).get('Meta').get('Login')
    l_det = YAML_OBJ.get(forum).get('Login')
    captchaBrowser.get(url)
    # driver.get(url)
    # The site we will navigate into, handling it's session

    if (YAML_OBJ.get(forum).get('Captcha').get('required') and YAML_OBJ.get(forum).get('Login').get('required')):
        try:
            nameVar = l_meta.get('user')
            passVar = l_meta.get('pass')
            nameVal = l_det.get('username')
            passVal = l_det.get('password')
            # submitbtn_var = l_meta.get('submit')
            submitbtn_val = l_det.get('submitbn')
            time.sleep(10)
            print "paass  ::", passVal
            # Hold control while Loading and Enter credentials
            choice = raw_input('Wait until page load. Press any key to continue : ')

            # ... Perform some actions
            wait_time = YAML_OBJ.get(forum).get('Jsload').get('waittime')
            if wait_time:
                wait = WebDriverWait(captchaBrowser, int(wait_time))
            time.sleep(10)
            # wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, submitbtn_val)))

            ### here I'm commenting this code because some the instances browsers unable to find elements
            # username = captchaBrowser.find_element_by_name(nameVar)
            # password = captchaBrowser.find_element_by_name(passVar)
            # username.send_keys(nameVal)
            # time.sleep(5)
            # password.send_keys(passVal)
            # time.sleep(5)
            # drivers = captchaBrowser.find_element_by_class_name(submitbtn_val)
            # print " driver " , captchaBrowser.page_source
            # drivers.click()

            # Waiting to check other page 'Profile'
            if wait_time:
                wait = WebDriverWait(captchaBrowser, int(wait_time))
            # captchaBrowser.get(url)
            # Grab the cookie
            cookie = captchaBrowser.get_cookies()
            # driver.delete_all_cookies()
            if not YAML_OBJ.get(forum).get('Jsload').get('required'):
                for s_cookie in cookie:
                    cj.set_cookie(cookielib.Cookie(version=0, name=s_cookie['name'], value=s_cookie['value'], port='80',
                                                   port_specified=False, domain=s_cookie['domain'],
                                                   domain_specified=True, domain_initial_dot=False,
                                                   path=s_cookie['path'], path_specified=True,
                                                   secure=s_cookie['secure'], expires=s_cookie['expiry'], discard=False,
                                                   comment=None, comment_url=None, rest=None, rfc2109=False))
            else:
                '''for s_cookie in cookie:
                    cookie_dict = {}
                    for k in s_cookie.keys():
                        try:
                            cookie_dict[k] = s_cookie[k]
                        except Exception as e:
                            print " cookie dic", e
                    # print " cookie dic", cookie_dict
                    try:
                        driver.add_cookie(cookie_dict)
                        time.sleep(10)
                    except Exception as e:
                        print " exception as  ", e'''
                cookie = captchaBrowser.get_cookies()
                number = 1
                for s_cookie in cookie:
                    cookie_dict1 = {}
                    for k in s_cookie.keys():
                        try:
                            if k == 'name' or k == 'value':
                                cookie_dict1[k] = s_cookie[k]
                        except Exception as e:
                            print " cookie dict exce ", e
                    # print " cookie dict ", cookie_dict
                    cookie_dict[str(number)] = cookie_dict1
                    number = number + 1
                print " cookie dict ", cookie_dict

            # print "-------------------------------- coockies set ----------------------------------------------"
            # Instantiate a Browser and set the cookies
            print "Now controll has handover to Mechanize!.."
        finally:
            choice = raw_input('Enter your choice Y/N : ')
            time.sleep(10)
            if (choice == 'Y' or choice == 'y'):
                response = 200
            else:
                response = None
        captchaBrowser.quit()
        response = 200
        return response
    else:
        choice = raw_input('Enter your choice Y/N : ')
        time.sleep(10)
        if (choice == 'Y' or choice == 'y'):
            response = 200
        else:
            response = None
        return response


def user_captcha_authentication(url):
    """ User Authentication """
    l_meta = YAML_OBJ.get(forum).get('Meta').get('Login')
    l_det = YAML_OBJ.get(forum).get('Login')
    captchaBrowser.get(url)
    # The site we will navigate into, handling it's session

    if (YAML_OBJ.get(forum).get('Captcha').get('required') and YAML_OBJ.get(forum).get('Login').get('required')):
        try:
            nameVar = l_meta.get('user')
            passVar = l_meta.get('pass')
            nameVal = l_det.get('username')
            passVal = l_det.get('password')
            time.sleep(10)
            # username = captchaBrowser.find_element_by_name(nameVar)
            # password = captchaBrowser.find_element_by_name(passVar)
            # username.send_keys(nameVal)
            # password.send_keys(passVal)

        finally:
            choice = raw_input('Enter your choice Y/N : ')
            time.sleep(10)
            if (choice == 'Y' or choice == 'y'):
                response = 200
            else:
                response = None
        return response
    else:
        choice = raw_input('Enter your choice Y/N : ')
        time.sleep(10)
        if (choice == 'Y' or choice == 'y'):
            response = 200
        else:
            response = None
        return response


def clickbutton(url):
    """ when forum a click operation when forum is first time load """
    l_meta = YAML_OBJ.get(forum).get('Meta').get('Login')
    if YAML_OBJ.get(forum).get('Click_require'):
        soup = BeautifulSoup(browser.open(url).read(), 'html.parser')
        browser.select_form(nr=l_meta.get('f_num'))
        response = browser.submit()
        return response.code


def get_parse_content(url):
    """ Get scrape content by url """
    try:
        js_check = False
        soup = None
        # Captcha
        if YAML_OBJ.get(forum).get('Captcha').get('type') == 3:
            if not YAML_OBJ.get(forum).get('Jsload').get('required'):
                # For selenium + Mechanize browser
                br = mechanize.Browser()
                br.set_cookiejar(cj)
                # br.set_handle_robots(False)
                # br.set_handle_equiv(False)
                br.addheaders = [
                    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'),
                    ('Accept', '*/*'),
                    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                    ('Accept-Encoding', 'none'),
                    ('Connection', 'keep-alive'),
                    ('Upgrade-Insecure-Requests', '1')
                    ]
                try:
                    # print " url " , url
                    page = br.open(url)
                    content = page.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    # print " soup in type 3 res" , soup
                except Exception as e3:
                    print " Exception as ", e3
            else:
                wait_time = YAML_OBJ.get(forum).get('Jsload').get('waittime')
                driver.get(url)
                wait = WebDriverWait(driver, int(wait_time))
                time.sleep(int(wait_time))
                element = YAML_OBJ.get(forum).get('Jsload').get('element')
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
                soup = BeautifulSoup(driver.page_source, 'lxml')
                # print(" soup " , soup)

            return soup
        elif YAML_OBJ.get(forum).get('Captcha').get('type'):
            # For selenium browser
            captchaBrowser.get(url)
            content = captchaBrowser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            return soup
        else:
            if YAML_OBJ.get(forum).get('Jsload'):
                js_check = YAML_OBJ.get(forum).get('Jsload').get('required')
                element = YAML_OBJ.get(forum).get('Jsload').get('element')
                wait_time = 1
            if js_check:
                try:
                    wait_time = YAML_OBJ.get(forum).get('Jsload').get('waittime')
                    # driver = webdriver.PhantomJS()
                    # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
                    driver.get(url)

                    for key, value in sorted(cookie_dict.items()):
                        driver.add_cookie(value)
                    wait = WebDriverWait(driver, int(wait_time))
                    time.sleep(int(wait_time))
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
                    # time.sleep(10)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    driver.delete_all_cookies()
                    # print " soup  " , soup
                    # driver.execute_script('localStorage.clear();')
                    # print soup
                except Exception as e:
                    print " Excep  ", e
            else:
                # Beautiful Soup is a Python library for pulling data out of HTML files
                # print "mechanize "
                if YAML_OBJ.get(forum).get('lxmlparser'):
                    soup = BeautifulSoup(browser.open(url).read(), 'lxml')
                    soup = BeautifulSoup(browser.open(url).read(), 'lxml') if not soup else soup
                else:
                    soup = BeautifulSoup(browser.open(url).read(), 'html.parser')
                    soup = BeautifulSoup(browser.open(url).read(), 'html.parser') if not soup else soup

                # print soup
            # print soup
            return soup

    except Exception as e:
        logging.exception(' error at fetching soup  %s ' % e)
        """forumUrls = YAML_OBJ.get(forum).get('WEB_URL')
        if YAML_OBJ.get(forum).get('Meta').get('Forum').get('extention'):
            forumUrls = YAML_OBJ.get(forum).get('WEB_URL') + YAML_OBJ.get(forum).get('Meta').get('Forum').get('extention')

        global emailcount
        count = emailcount + 1
        if url == forumUrls and count == 1:
            sendEmail(e ,url )  
        return None """


def get_forum_urls(soup):
    r_url = YAML_OBJ.get(forum).get('Meta').get('Forum').get('url')

    if r_url == None:
        raise 'IN YAML File required field is not found'
    if r_url == "\\%s":
        r_url = r_url.strip('\\')
    links = soup.findAll('a', attrs={'href': re.compile(re.escape(r_url).replace('\%s', ".*"))})
    url_list = list()
    for link in links:
        try:
            url = link.get('href')
            url_list.append(url)
        except Exception as e:
            pass
    url_list = ' '.join(str(x.encode('utf-8')) for x in url_list)
    if YAML_OBJ.get(forum).get('needSlash'):
        return re.findall(re.escape(r_url).replace('\%s', '\S*'), str(url_list), re.I)
    else:
        return re.findall(re.escape(r_url).replace('\%s', '\S+'), str(url_list), re.I)


def remove_words(soup, removewords_dic):
    temp = 0
    for key, value in removewords_dic.items():
        temp += 1
    temp = (temp / 2) + 1
    modifiedsoup = soup
    for countValue in range(1, temp):
        modifiedsoup = str(modifiedsoup).replace(str(removewords_dic.get('remove' + str(countValue))),
                                                 str(removewords_dic.get('replace' + str(countValue))))
        soup = modifiedsoup

    return BeautifulSoup(str(modifiedsoup), 'lxml')


def get_resume_thread_page(engine, thread_last_page_details, f_id, t_id, thread_uuid, baseurl, t_url, t_page):
    try:
        # Check for exisiting entry in the DB.
        # If entry is not present then return 1.
        _session = sessionmaker()
        _session.configure(bind=engine)
        session = _session()
        meta_dic = YAML_OBJ.get(forum).get('Meta')
        if thread_last_page_details > 1:
            temp_lastpage = thread_last_page_details.lastpage
            lastpage = temp_lastpage
            while temp_lastpage > 0:
                thread_url = ''
                if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page'):
                    lastpage = posts_records_per_page(lastpage)

                if str(meta_dic.get('Thread').get('page_url')).count('%s') == 3:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, lastpage, t_page))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 2:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, lastpage))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 1:
                    thread_url = t_url + (str(meta_dic.get('Thread').get('page_url')).lstrip('\\') % (lastpage))
                else:
                    page_splitUrl = meta_dic.get('Thread').get('page_url')
                    splitpageArgs = page_splitUrl.split('rem@_!@')
                    # print " splitpageArgs " ,splitpageArgs
                    for argm in range(len(splitpageArgs) - 1, len(splitpageArgs)):
                        splittedThreadUrl = t_url.split(splitpageArgs[len(splitpageArgs) - 1])
                    # print " splittedThreadUrl " , splittedThreadUrl
                    thread_url = None
                    thread_url = str(splittedThreadUrl[0]) + str(splitpageArgs[1]) + str(t_page) + splitpageArgs[2]

                soup = get_parse_content(thread_url)
                if soup:
                    rows = get_post_rows(soup)
                    exists_count = 0
                    for row in rows:
                        post_info = get_post_info(row)
                        if post_info:
                            post_id = post_info['post_id']

                            is_post_details_exist = session.query(
                                Post
                            ).filter_by(third_party_id=post_id,
                                        thread_uuid=thread_uuid).first()
                            if is_post_details_exist:
                                exists_count = exists_count + 1
                                if exists_count > 1:
                                    session.close()
                                    return lastpage

                temp_lastpage = temp_lastpage - 1
                # print "lastpage:",lastpage," thread_uuid:",thread_uuid
            logging.info("found but had to return 1 thread_uuid: %s lastpage:  %s " % (thread_uuid, lastpage))
            session.close()
            return 1
        else:
            logging.info("do not found 1 thread_uuid: %s " % thread_uuid)
            session.close()
            return 1
    except Exception as e:
        logging.exception("exception occurred %s " % e)
        session.close()
        return 1


def get_thread_total_page_count(soup, url):
    '''
        Get given url pages count by pagination
    '''
    try:
        total_pages = 1
        pagenav_dic = YAML_OBJ.get(forum).get('Meta').get('Thread').get('pagenav')
        sub = YAML_OBJ.get(forum).get('Meta').get('Thread').get('pagenav').get('subtag')
        pagenav = None
        if soup:
            pagenav = soup.find(pagenav_dic.get('tag'), {'class': pagenav_dic.get('class')})

        if pagenav:
            if pagenav_dic.get('subtag'):
                pagesList = list()
                rawList = pagenav.find_all(sub)
                for a in rawList:
                    pagesList.append(a.text)
                last = [int(s) for s in pagesList if s.isdigit()]
                # print "last ::",last
                if len(last) > 0:
                    if not pagenav_dic.get('subclass'):
                        total_pages = max(last)
                    else:
                        lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                        # print " lastPage " , lastPage
                        if lastPage:
                            lastPage = lastPage.text.strip()
                        else:
                            lastPage = " 1 "
                        if total_pages:
                            last = [int(s) for s in lastPage.split() if s.isdigit()]
                        if last:
                            total_pages = max(last)
                        else:
                            total_pages = 1

                else:
                    lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                    # print " lastPage " , lastPage
                    if lastPage:
                        lastPage = lastPage.text.strip()
                    else:
                        lastPage = " 1 "
                    if total_pages:
                        last = [int(s) for s in lastPage.split() if s.isdigit()]
                        if last:
                            total_pages = max(last)
                    else:
                        total_pages = 1
            else:
                pagenav = pagenav.find_all('a')
                pageList = list()
                for a in pagenav:
                    pageList.append(a.text)
                if total_pages:
                    last = [int(s) for s in pageList if s.isdigit()]
                    if last:
                        total_pages = max(last)
                else:
                    total_pages = 1
        if YAML_OBJ.get(forum).get('Meta').get('Thread').get('prob_pagenav'):
            prob_pagenav = YAML_OBJ.get(forum).get('Meta').get('Thread').get('prob_pagenav')
            page_url = YAML_OBJ.get(forum).get('Meta').get('Thread').get('prob_pagenav').get('page_url')
            thread_page_urls = soup.findAll('a', attrs={'href': re.compile(re.escape(page_url).replace('\%s', ".*"))})

            pages_list = []
            if len(thread_page_urls) > 0:

                for page_url in thread_page_urls:
                    if page_url.text.isdigit():
                        pages_list.append(page_url.text)

            if len(pages_list) > 0:
                total_pages = int(max(pages_list))
            else:
                total_pages = 1
    except Exception as e:
        total_pages = 1
        logging.exception("+++++ %s +++ %s " % (traceback.print_exception(*sys.exc_info()), url))
    return total_pages


def get_post_total_page_count(soup, url, post_comment_dict):
    '''
        Get given url pages count by pagination
    '''
    try:
        total_pages = 1
        pagenav_dic = post_comment_dict.get('pagenav')
        sub = post_comment_dict.get('pagenav').get('subtag')
        pagenav = None
        if soup:
            pagenav = soup.find(pagenav_dic.get('tag'), {'class': pagenav_dic.get('class')})
        if pagenav:
            if pagenav_dic.get('subtag'):
                pagesList = list()
                rawList = pagenav.find_all(sub)
                for a in rawList:
                    pagesList.append(a.text)
                last = [int(s) for s in pagesList if s.isdigit()]
                if len(last) > 0:
                    if not pagenav_dic.get('subclass'):
                        total_pages = max(last)
                    else:
                        lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                        # print "  lastPage " , lastPage
                        if lastPage:
                            lastPage = lastPage.text.strip()
                        else:
                            lastPage = " 1 "
                        if total_pages:
                            last = [int(s) for s in lastPage.split() if s.isdigit()]
                            if last:
                                total_pages = max(last)
                            else:
                                total_pages = 1
                        else:
                            pagenav = pagenav.find('a').text.strip()
                            if total_pages:
                                last = [int(s) for s in pagenav.split() if s.isdigit()]
                                if last:
                                    total_pages = max(last)
                            else:
                                total_pages = 1

                else:
                    lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                    if lastPage:
                        lastPage = lastPage.text.strip()
                    else:
                        lastPage = " 1 "
                    if total_pages:
                        last = [int(s) for s in lastPage.split() if s.isdigit()]
                        if last:
                            total_pages = max(last)
                        else:
                            total_pages = 1
                    else:
                        pagenav = pagenav.find('a').text.strip()
                        if total_pages:
                            last = [int(s) for s in pagenav.split() if s.isdigit()]
                            if last:
                                total_pages = max(last)
                        else:
                            total_pages = 1
        if post_comment_dict.get('prob_pagenav'):
            prob_pagenav = post_comment_dict.get('prob_pagenav')
            page_url = post_comment_dict.get('prob_pagenav').get('page_url')
            thread_page_urls = soup.findAll('a', attrs={'href': re.compile(re.escape(page_url).replace('\%s', ".*"))})

            pages_list = []
            if len(thread_page_urls) > 0:

                for page_url in thread_page_urls:
                    if page_url.text.isdigit():
                        pages_list.append(page_url.text)
            print pages_list
            if len(pages_list) > 0:
                total_pages = int(max(pages_list))
            else:
                total_pages = 1
            print " total_pages ", total_pages
    except Exception as e:
        total_pages = 1
        logging.exception("+++ %s ++ %s " % (traceback.print_exception(*sys.exc_info()), url))
    return total_pages


def get_thread_rows(soup, f_id):
    tbody_dic = YAML_OBJ.get(forum).get('Meta').get('Thread').get('soup').get('seperator')

    _attrs = {}
    for key, value in tbody_dic.items():
        if value and key != 'tag':
            if '%s' in value:
                if key == 'id':
                    value = value % f_id
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if tbody_dic.get('tag'):
        if YAML_OBJ.get(forum).get('Meta').get('Thread').get('pagenav').get('mainThreadseparateelement'):
            tbody = soup.find_all(tbody_dic.get('tag'), attrs=_attrs)[
                int(YAML_OBJ.get(forum).get('Meta').get('Thread').get('pagenav').get('mainThreadseparateelement'))]
        else:
            tbody = soup.find(tbody_dic.get('tag'), attrs=_attrs)
    else:
        tbody = soup

    tbody_dic = YAML_OBJ.get(forum).get('Meta').get('Thread').get('find').get('seperator')
    _attrs = {}
    for key, value in tbody_dic.items():
        if value and key != 'tag':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    rows = tbody.findAll(tbody_dic.get('tag'), attrs=_attrs) if tbody else []
    return rows


def get_thread_info(row, baseurl):
    thread_name = ''
    thread_id = None
    thread_date = None
    t_dic = YAML_OBJ.get(forum).get('Meta').get('Thread').get('find')
    _attrs = {}
    for key, value in t_dic.get('title').items():
        if value and key != 'tag' and key != 'get':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)

    thread_title = row.find(t_dic.get('title').get('tag'), attrs=_attrs)
    if thread_title:
        if t_dic.get('title').get('get').get('value'):
            thread_name = thread_title.get(t_dic.get('title').get('get').get('value'))
            if thread_name:
                thread_name = thread_name.encode('utf-8')
        else:
            thread_name = thread_title.text.encode('utf-8')

        # Parsing thread url
        thread_url = thread_title.get('href')
        if not thread_url:
            thread = thread_title.find('a')
            if thread:
                thread_url = thread.get('href')
        thread_url = urlparse.urljoin(baseurl, thread_url)
        thread_url = str(thread_url).replace('../', '')

        # Parsing thread id
        if t_dic.get('t_id') and not t_dic.get('t_id').get('tag'):
            thread_id = t_dic.get('t_id').get('get').get('value')
            thread_id = row.get(thread_id)
            if thread_id:
                list_threads = re.findall("([\d]+)", str(thread_id))
                thread_id = max([int(i) for i in list_threads])
        elif t_dic.get('t_id'):
            _attrs = {}
            for key, value in t_dic.get('t_id').items():
                if value and key != 'tag' and key != 'get' and key != 'threadindex' and key != 'third_party_id_index' and key != 'split_string':
                    if isinstance(value, list):
                        _attrs[key] = value
                    else:
                        _attrs[key] = re.compile(value)
            raw_thread_id = row.find(t_dic.get('t_id').get('tag'), attrs=_attrs)
            thread_id = raw_thread_id.get(t_dic.get('t_id').get('get').get('value')) if raw_thread_id else None
            if thread_id:
                list_threads = None
                list_threads1 = None
                list_threads1 = re.findall("([\d]+)", str(thread_id))
                try:
                    if t_dic.get('t_id').get('threadindex'):

                        list_threads = str(thread_id).split(t_dic.get('t_id').get('split_string'))
                        print "list_threads    ", list_threads
                        list_threads = list_threads[int(t_dic.get('t_id').get('threadindex')) - 1]

                    print "list_threads  ", list_threads
                    if t_dic.get('t_id').get('third_party_id_index'):
                        list_threads = re.findall("([\d]+)", str(list_threads))
                        print "thread_id   ",list_threads
                        thread_id = list_threads[int(t_dic.get('t_id').get('third_party_id_index')) - 1]
                        print "thread_id   ", thread_id
                    else:
                        thread_id = max([int(i) for i in list_threads1])
                except Exception as e:
                    thread_id = max([int(i) for i in list_threads1])
                    print e
                print "thread_id   ", thread_id
        else:
            raw_thread_id = thread_title.get('id')
            if raw_thread_id:
                list_threads = re.findall("([\d]+)", str(raw_thread_id))
                thread_id = max([int(i) for i in list_threads])
                if not str(thread_id):
                    list_threads = re.findall("([\d]+)", str(thread_url))
                    thread_id = max([int(i) for i in list_threads])
            elif thread_url:
                list_threads = re.findall("([\d]+)", str(thread_url))
                if list_threads:
                    thread_id = max([int(i) for i in list_threads])
                # thread_id = max(re.findall("([\d]+)", str(thread_url)))
        if not thread_id:
            thread_id = int(hashlib.md5(thread_name + thread_url).hexdigest(), 16)

    else:
        return None
    last_post_date = None
    if t_dic.get('last_post_date'):
        try:
            _attrs = {}
            selectorType = ''
            selector = None
            print " In last_post_date  "
            for key, value in t_dic.get('last_post_date').items():
                print "key  ", key
                print "value  ", value
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else:
                    if value:
                        elementtag = value
            date_post = find_ele(row, elementtag, selectorType, selector, t_dic)
            last_post_date = date_post
            # print " post_date error finding " , last_post_date
            encodedDateText = "SWfDpXI="
            if last_post_date:
                if encodedDateText.decode('base64') in last_post_date:
                    postdateEncoder = str((last_post_date.encode('base64')).replace(encodedDateText, 'WWVzdGVyZGF5'))
                    last_post_date = postdateEncoder.decode('base64')
                # print "BEFORE ::",last_post_date
                if is_date(last_post_date):
                    last_post_date = get_utc(last_post_date)
                    print "is_date--", last_post_date
                    if last_post_date > datetime.utcnow():
                        last_post_date = datetime.utcnow()
                        # print "is_date--",last_post_date
                else:
                    last_post_date = datetime.utcnow()
                    # print "In else",last_post_date
                # print "AFTER :: post date",last_post_date
            else:
                last_post_date = datetime.utcnow()
                # print "Outer else---",last_post_date
        except Exception as date_exe:
            last_post_date = datetime.utcnow()
            print "exception block else---", last_post_date
    else:
        last_post_date = datetime.utcnow()
    print "last_post_date   ", last_post_date

    # parsing date
    if t_dic.get('date'):
        try:
            _attrs = {}
            for key, value in t_dic.get('date').items():
                if value and key != 'tag':
                    if isinstance(value, list):
                        _attrs[key] = value
                    else:
                        _attrs[key] = re.compile(value)
            rawdate = row.find(t_dic.get('date').get('tag'), attrs=_attrs)
            threaddate = rawdate.text.encode('utf-8').strip()
            encodedDateText = "SWfDpXI="
            if is_date(threaddate):
                if encodedDateText.decode('base64') in threaddate:
                    threaddateEncoder = str((threaddate.encode('base64')).replace(encodedDateText, 'WWVzdGVyZGF5'))
                    threaddate = threaddateEncoder.decode('base64')
            else:
                pass
            thread_date = get_utc(threaddate)
            if thread_date:
                if thread_date > datetime.utcnow():
                    thread_date = datetime.utcnow()
            else:
                thread_date = datetime.utcnow()
            # print "AFTER ::",thread_date
        except Exception as date_exe:
            thread_date = datetime.utcnow()
    else:
        thread_date = datetime.utcnow()

    return {'thread_date': thread_date, 'thread_name': thread_name, 'thread_url': thread_url, 'thread_id': thread_id,
            'last_post_date': last_post_date}


def get_post_rows(soup):
    post_dic = YAML_OBJ.get(forum).get('Meta').get('Post').get('soup').get('seperator')

    if YAML_OBJ.get(forum).get('Meta').get('Post').get('soup').get('postmainseparator'):
        _attrs = {}
        post_seperator = YAML_OBJ.get(forum).get('Meta').get('Post').get('soup').get('postmainseparator')
        if post_seperator.get('number'):
            soup = soup.find_all(post_seperator.get('tag'))[int(post_seperator.get('number'))]
        else:
            for key, value in post_seperator.items():
                if value and key != 'tag':
                    _attrs[key] = re.compile(value)
            soup = soup.find(post_seperator.get('tag'), attrs=_attrs)
    _attrs = {}
    for key, value in post_dic.items():
        if value and key != 'tag':
            _attrs[key] = re.compile(value)
    rows = soup.findAll(post_dic.get('tag'), attrs=_attrs)
    return rows


def get_comment_rows(soup):
    post_dic = YAML_OBJ.get(forum).get('Meta').get('Comment').get('soup').get('seperator')

    if YAML_OBJ.get(forum).get('Meta').get('Comment').get('soup').get('postmainseparator'):
        _attrs = {}
        post_seperator = YAML_OBJ.get(forum).get('Meta').get('Comment').get('soup').get('postmainseparator')
        if post_seperator.get('number'):
            soup = soup.find_all(post_seperator.get('tag'))[int(post_seperator.get('number'))]
        else:
            for key, value in post_seperator.items():
                if value and key != 'tag':
                    _attrs[key] = re.compile(value)
            soup = soup.find(post_seperator.get('tag'), attrs=_attrs)
    _attrs = {}
    for key, value in post_dic.items():
        if value and key != 'tag':
            _attrs[key] = re.compile(value)
    rows = soup.findAll(post_dic.get('tag'), attrs=_attrs)
    return rows


def get_post_info(row):
    post_id = None
    member_name = ''
    post_date = None
    post_body = ''
    post_dic = YAML_OBJ.get(forum).get('Meta').get('Post').get('find')
    _attrs = {}
    for key, value in post_dic.get('name').items():
        if value and key != 'tag':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    post_member = row.find(post_dic.get('name').get('tag'), attrs=_attrs)
    if post_member:
        member_name = post_member.text.encode('utf-8').strip()

    # parsing id
    _attrs = {}
    for key, value in post_dic.get('p_id').items():
        if value and key != 'tag' and key != 'get':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if post_dic.get('p_id').get('tag'):
        raw_post = row.find(post_dic.get('p_id').get('tag'), attrs=_attrs)
        if raw_post:
            raw_post = raw_post.get(post_dic.get('p_id').get('get').get('value'))
            if raw_post:
                post_idcontx = re.search("([\d]+)", raw_post)
                if post_idcontx:
                    post_id = re.search("([\d]+)", raw_post).group(1)
            if YAML_OBJ.get(forum).get('Meta').get('Post').get('pagenav').get('postIdAll'):
                post_ids = re.findall("([\d]+)", raw_post)
                post_id = max(post_ids)
    else:
        raw_post = row.get(post_dic.get('p_id').get('get').get('value'))
        if raw_post:
            post_idsArray = re.search("([\d]+)", raw_post)
            if post_idsArray:
                post_id = re.search("([\d]+)", raw_post).group(1)

    # parsing message
    _attrs = {}
    for key, value in post_dic.get('message').items():
        if value and key != 'tag':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    post_message = row.find(post_dic.get('message').get('tag'), attrs=_attrs)
    if post_message:
        post_body = post_message.text.strip().encode('utf-8')
    elementtag = None

    if YAML_OBJ.get(forum).get('textTopost'):
        post_id = int(hashlib.md5(post_body + member_name).hexdigest(), 16)
    if not post_id and post_body != '' and member_name != '':
        post_id = int(hashlib.md5(post_body + member_name).hexdigest(), 16)
    # parsing date
    _attrs = {}
    if post_dic.get('date'):
        try:
            selectorType = ''
            selector = None
            _attrs = {}
            for key, value in post_dic.get('date').items():
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else:
                    if value:
                        elementtag = value
            date_post = find_ele(row, elementtag, selectorType, selector, post_dic)
            post_date = date_post
            encodedDateText = "SWfDpXI="
            if post_date:
                if encodedDateText.decode('base64') in post_date:
                    postdateEncoder = str((post_date.encode('base64')).replace(encodedDateText, 'WWVzdGVyZGF5'))
                    post_date = postdateEncoder.decode('base64')
                if is_date(post_date):
                    post_date = get_utc(post_date)
                    if post_date > datetime.utcnow():
                        post_date = datetime.utcnow()
                else:
                    post_date = datetime.utcnow()
            else:
                post_date = datetime.utcnow()
        except Exception as date_exe:
            post_date = datetime.utcnow()
    else:
        post_date = datetime.utcnow()

    return {'post_date': post_date, 'post_body': post_body, 'member_name': member_name, 'post_id': post_id,
            'post_urls': post_message}


def get_comment_info(row):
    comment_id = None
    member_name = ''
    comment_date = None
    comment_body = ''
    comment_dic = YAML_OBJ.get(forum).get('Meta').get('Comment').get('find')
    _attrs = {}
    for key, value in comment_dic.get('name').items():
        if value and key != 'tag':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    comment_member = row.find(comment_dic.get('name').get('tag'), attrs=_attrs)

    if comment_member:
        member_name = comment_member.text.encode('utf-8').strip()

    # print "  row in post ", row
    # parsing id
    _attrs = {}
    for key, value in comment_dic.get('p_id').items():
        if value and key != 'tag' and key != 'get':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if comment_dic.get('p_id').get('tag'):
        raw_comment = row.find(comment_dic.get('p_id').get('tag'), attrs=_attrs)
        if raw_comment:
            raw_comment = raw_comment.get(comment_dic.get('p_id').get('get').get('value'))
            if raw_comment:
                comment_idcontx = re.search("([\d]+)", raw_comment)
                if comment_idcontx:
                    comment_id = re.search("([\d]+)", raw_comment).group(1)
            if YAML_OBJ.get(forum).get('Meta').get('Post').get('pagenav').get('postIdAll'):
                comment_ids = re.findall("([\d]+)", raw_comment)
                comment_id = max(comment_ids)

    else:
        raw_comment = row.get(comment_dic.get('p_id').get('get').get('value'))
        if raw_comment:
            comment_idsArray = re.search("([\d]+)", raw_comment)
            if comment_idsArray:
                comment_id = re.search("([\d]+)", raw_comment).group(1)

    # parsing message
    _attrs = {}
    for key, value in comment_dic.get('message').items():
        if value and key != 'tag':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    comment_message = row.find(comment_dic.get('message').get('tag'), attrs=_attrs)
    if comment_message:
        comment_body = comment_message.text.strip().encode('utf-8')
    elementtag = None

    if YAML_OBJ.get(forum).get('textTopost'):
        comment_id = int(hashlib.md5(comment_body + member_name).hexdigest(), 16)

    if not comment_id and comment_body != '' and member_name != '':
        comment_id = int(hashlib.md5(comment_body + member_name).hexdigest(), 16)
    # parsing date
    _attrs = {}
    if comment_dic.get('date'):
        try:
            _attrs = {}
            selectorType = ''
            selector = None

            for key, value in comment_dic.get('date').items():
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else:
                    if value:
                        elementtag = value
            date_comment = find_ele(row, elementtag, selectorType, selector, comment_dic)
            comment_date = date_comment
            encodedDateText = "SWfDpXI="
            if comment_date:
                if encodedDateText.decode('base64') in comment_date:
                    commentdateEncoder = str((comment_date.encode('base64')).replace(encodedDateText, 'WWVzdGVyZGF5'))
                    comment_date = commentdateEncoder.decode('base64')
                if is_date(comment_date):
                    comment_date = get_utc(comment_date)
                    if comment_date > datetime.utcnow():
                        comment_date = datetime.utcnow()
                else:
                    comment_date = datetime.utcnow()
            else:
                comment_date = datetime.utcnow()
        except Exception as date_exe:
            comment_date = datetime.utcnow()
    else:
        comment_date = datetime.utcnow()
    return {'comment_date': comment_date, 'comment_body': comment_body, 'member_name': member_name,
            'comment_id': comment_id, 'comment_type': 'comment', 'comment_urls': comment_message}


# TO check provided string has valid date or not
def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def give_reply(reply_msg, row, thread_url, num):
    reply_btn_obj = YAML_OBJ.get(forum).get('Replay_btn')
    _attr = {}
    reply_submit_obj = YAML_OBJ.get(forum).get('reply_submit')
    reply_msg_obj = YAML_OBJ.get(forum).get('Reply_msg')
    post_soup = get_parse_content(thread_url)

    # print "in give_ reply",post_soup
    if reply_submit_obj:
        try:
            for i in range(0, 4):
                try:
                    response_res = browser.open(thread_url)
                    time.sleep(10)
                    browser.select_form(nr=i)
                    print "before entering msg"
                    browser.form[reply_msg_obj.get('identifier')] = reply_msg
                    # 'topic_comment_19516_noscript'
                    # response_res = browser.submit(id='quick_reply_submit')
                    if reply_submit_obj.get('required'):
                        attr = reply_submit_obj.get('attribute')
                        value = reply_submit_obj.get('value')
                        response_res = browser.submit(attr=value)
                        print " reply submitted successfuly ", thread_url
                    else:
                        response_res = browser.submit()
                    # time.sleep(20)
                    break
                except Exception as e:
                    print "form num exception occured ", i, e
            post_soup = get_parse_content(thread_url)
            if YAML_OBJ.get(forum).get('Meta').get('Post').get('soup').get('removewords'):
                list_words = YAML_OBJ.get(forum).get('Meta').get('Post').get('soup').get('removewords')
                post_soup = remove_words(post_soup, list_words)
            post_rows = get_post_rows(post_soup)
            reply_post_row = post_rows[num]
            post_info_obj = get_post_info(reply_post_row)
            reply_post_body = post_info_obj.get('post_body')
            return reply_post_body
        except Exception as err:
            print " reply form submission ", err
    else:
        print "reply soup is empty"
        return None


# To get Required format of given date
def get_utc(givendate):
    try:
        post_dic = YAML_OBJ.get(forum).get('Meta').get('Post').get('find')
        if (post_dic.get('date_setting')):
            post_dic = post_dic.get('date_setting')
        format = None
        prestring = None
        language = None
        if (post_dic.get('required')):
            format = post_dic.get('format')
            prestring = post_dic.get('pre_string')
            language = post_dic.get('language')
            try:
                if (post_dic.get('pre_string')):
                    for val in post_dic.get('pre_string'):
                        givendate = givendate.replace(val, "")
                if (language):
                    parsed_Date = parse(givendate, languages=[language])
                elif (format == 'DMY'):
                    parsed_Date = parse(givendate, settings={'DATE_ORDER': 'DMY'})
                elif (format == 'MDY'):
                    parsed_Date = parse(givendate, settings={'DATE_ORDER': 'MDY'})
                elif (format == 'YMD'):
                    parsed_Date = parse(givendate, settings={'DATE_ORDER': 'YMD'})
                else:
                    parsed_Date = parse(givendate)
            except ValueError:
                return datetime.utcnow()
        else:
            parsed_Date = parse(givendate)
        try:
            if (post_dic.get('string_format')):
                parsed_Date = datetime.strptime(givendate, post_dic.get('string_format'))
                print "after string_format    ", parsed_Date
        except Exception as e:
            parsed_Date = parse(givendate)
        if parsed_Date == None:  # If date string has combination of strings and date
            try:
                parsed_Date = dparser.parse(givendate, fuzzy=True)
            except ValueError:
                parsed_Date = datetime.utcnow()
        return datetime.combine(parsed_Date.date(), parsed_Date.time())
    except ValueError:
        return datetime.utcnow()


def posts_records_per_page(page):
    page_count = page
    try:
        pagenav_dic = YAML_OBJ.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page')
        if pagenav_dic:
            page = int(page)
            page = (page - 1) * pagenav_dic
            page_count = page
        return page_count
    except Exception as e2:
        print " exception in posts_records_per_page ", e2
        return page_count


def thread_records_per_page(page):
    page_count = page
    try:
        pagenav_dic = YAML_OBJ.get(forum).get('Meta').get('Thread').get('pagenav').get('threads_per_page')
        if pagenav_dic:
            page = int(page)
            page = (page - 1) * pagenav_dic
            page_count = page
        return page_count

    except Exception as e2:
        logging.error(" exception in thread_records_per_page %s " % e2)
        return page_count


def find_ele(root, tag, key, selector, date_dic):
    seloperators = selector.split()
    _attrs = {}
    if selector:
        if isinstance(seloperators[0], list):
            _attrs[key] = seloperators[0]
        else:
            _attrs[key] = re.compile(seloperators[0])

        if seloperators[0] != 'False':
            # print " in true "
            root = root.find(tag, _attrs)
        mainTest = root
    else:
        root = root.find(tag, _attrs)
        mainTest = root
    if (date_dic.get('date_setting')):
        date_dic = date_dic.get('date_setting')
    for index in range(1, len(seloperators)):
        if seloperators[index] == '>':
            root = root.next_Sibling
        elif seloperators[index] == '<':
            root = root.previous_sibling
        # elif (seloperators[index].startswith('~'))
        else:
            try:
                print " seloperators[index] ", seloperators[index][1:]
                childoperator = seloperators[index][1:]

                if '.' in childoperator:
                    childtag = childoperator.split('.')[0]
                    childclass = childoperator.split('.')[1]
                    root = root.find(childtag, {"class": childclass})
                elif '#' in childoperator:
                    childtag = childoperator.split('#')[0]
                    childid = childoperator.split('#')[1]
                    root = root.find(childtag, {"id": childid})
                elif '@':
                    childtag = childoperator.split('@')[0]
                    # print " childtag " , childtag
                    nthchildcount = int(childoperator.split('@')[1])
                    # print " nthchildcount " , nthchildcount , root
                    root = root.find_all(childtag)[nthchildcount - 1]
                    print " root find all", root
            except Exception as e:
                print " exception ", e
    try:
        if (date_dic.get('parent_tag_text_num')):
            root = ' '.join(map(str, root(text=True, recursive=False)))
        else:
            if (date_dic.get('tag') != tag):
                root = root.find(date_dic.get('tag'))[date_dic.get('get').get('value')]
            elif (date_dic.get('tag') == tag):
                root = root[date_dic.get('get').get('value')]
            else:
                root = root.text
    except Exception as e:
        root = root.text
    return str(root).encode('utf-8')


def sendEmail(url, error):
    msg = MIMEMultipart()
    msg['From'] = 'sureshborra@vidyayug.com'
    receipients = ['sai.vidyayug@gmail.com']
    msg['To'] = ", ".join(receipients)
    msg['Subject'] = 'Duplicate Entry Thread Urls'
    message = "Hi Team , \n Thread url :  %s \n Thread Id: %s" % (url, error)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('sureshborra@vidyayug.com', 'Vidyayug@123')

    mailserver.sendmail('sureshborra@vidyayug.com', receipients, msg.as_string())

    mailserver.quit()
