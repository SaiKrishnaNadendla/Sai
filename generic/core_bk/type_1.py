from generic.core import *
# User-Agent Rotation Manually
from random import choice
#User agent pool/ We need to select each user-Agent at the time of request
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
emailcount = 0
if yaml_obj.get(forum).get('Captcha').get('type'):
    captchaBrowser = webdriver.Firefox()
if yaml_obj.get(forum).get('Jsload').get('required') :
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
def user_authentication(url):
  """ User Authentication """
  l_meta = yaml_obj.get(forum).get('Meta').get('Login')
  l_det = yaml_obj.get(forum).get('Login')
  print "url is    ",url
  if not l_det.get('phantom') :
    # The site we will navigate into, handling it's session
    #response = browser.open(url)
    #browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
    userAgent = choice(desktop_agents)
    browser.addheaders = [('User-Agent', userAgent),
       ('Accept', '*/*'),
       ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
       ('Accept-Encoding', 'none'),
       ('Connection', 'keep-alive')]
    response = None
    try :
        response = browser.open(url)
        #print "output is     ",BeautifulSoup(response.read() , 'html.parser')
    except Exception as e :
        print e       
        pass
    browser.addheaders = [('User-Agent', userAgent),
       ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
       ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
       ('Accept-Encoding', 'none'),
       ('Accept-Language', 'en-US,en;q=0.8'),
       ('Connection', 'keep-alive')]
    try :
        response = browser.open(url)
        #print "output is     ",BeautifulSoup(response.read() , 'html.parser')
    except Exception as e :
        print 'exception e as' , e
        pass
    
    # Select the first (index zero) form
    browser.select_form(nr=l_meta.get('f_num'))

    # User credentials
    if yaml_obj.get(forum).get('Login').get('required'):
        browser.form[l_meta.get('user')] = l_det.get('username')
        browser.form[l_meta.get('pass')] = l_det.get('password')

    # Captcha
    if yaml_obj.get(forum).get('Captcha').get('required'):
        filepath = '/data/Archives/captcha/'
        timestamp = str(time.time()).split('.')[0]
        imageType = 'png'
        if yaml_obj.get(forum).get('Captcha').get('imagetype'):
            imageType = yaml_obj.get(forum).get('Captcha').get('imagetype')  
        filetimestamp = 'captcha'+timestamp+'.'+imageType
        filename = os.path.join(filepath , filetimestamp)
        c_meta = yaml_obj.get(forum).get('Meta').get('Captcha')
        c_det = yaml_obj.get(forum).get('Captcha')
        soup1 = BeautifulSoup(response.read(), 'html.parser')
        if yaml_obj.get(forum).get('Captcha').get('imagetag'):
            res = soup1.find_all(str(yaml_obj.get(forum).get('Captcha').get('imagetag')))[int(yaml_obj.get(forum).get('Captcha').get('count'))].get( yaml_obj.get(forum).get('Captcha').get('key'))       
            print " res " , res 
            res = res[res.find(",")+1:] 
            imgdata = base64.decodestring(res)
            with open(filename, 'wb') as f:        
                f.write(imgdata)        
            webbrowser.open(filename)
            '''try :
                os.system("rsync -apv /data/Archives/captcha/ ityugrsync:/data/Archives/captcha/")
            except Exception  as e3 :
                print " exception at file moving " , e3 '''
            print " take captch image from /data/Archives/captcha/%s" %(filetimestamp)
            captchaStr = raw_input("Enter captcha Here ::")
            browser.form[c_meta.get('tag')] = str(captchaStr)

    # Login
    response = browser.submit()
    return response.code
  else :
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        time.sleep(20)
        element = yaml_obj.get(forum).get('Jsload').get('element')
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
        #print " soup " , driver.page_source
        #l_meta.get('user')   l_meta.get('pass')   
        username = driver.find_element_by_name(l_meta.get('user'))   # l_det.get('username'))
        password = driver.find_element_by_name(l_meta.get('pass'))   # l_det.get('password'))
        #l_det.get('submitbn')
        username.send_keys(l_det.get('username'))
        password.send_keys(l_det.get('password')) 
        
        drivers = driver.find_element_by_class_name(l_det.get('submitbn'))
        #print " driver " , driver.page_source
        drivers.click()
        print " result " , l_det.get('username') in driver.page_source
        #print " driver " , driver.page_source
        if l_det.get('username') in driver.page_source : 
            return 200 
        else :
            return 0

def user_captcha_authentication(url):
    """ User Authentication """
    l_meta = yaml_obj.get(forum).get('Meta').get('Login')
    l_det = yaml_obj.get(forum).get('Login')
    captchaBrowser.get(url)
    # The site we will navigate into, handling it's session

    if (yaml_obj.get(forum).get('Captcha').get('required') and yaml_obj.get(forum).get('Login').get('required')):        
        try:            
            nameVar = l_meta.get('user')
            passVar = l_meta.get('pass')
            nameVal = l_det.get('username')
            passVal = l_det.get('password')
            time.sleep(10)           
            username = captchaBrowser.find_element_by_name(nameVar) # username = captchaBrowser.find_element_by_name("username")
            password = captchaBrowser.find_element_by_name(passVar) # password = captchaBrowser.find_element_by_name("password")
            username.send_keys(nameVal)# username.send_keys("jhoneypep")
            password.send_keys(passVal)# password.send_keys("Jhoney@1234") 
            
        finally:           
            choice = raw_input('Enter your choice Y/N : ')
            time.sleep(10)
            if(choice == 'Y' or choice == 'y'):
                response = 200
            else:
                response = None
        return response
    else:       
        choice = raw_input('Enter your choice Y/N : ')
        time.sleep(10)
        if(choice == 'Y' or choice == 'y'):
            response = 200
        else:
            response = None
        return response	
	
	
def clickbutton(url):
    """ when forum a click operation when forum is first time load """
    l_meta = yaml_obj.get(forum).get('Meta').get('Login')
    if yaml_obj.get(forum).get('Click_require') :
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
        if yaml_obj.get(forum).get('Captcha').get('type'):
            #For selenium browser
            captchaBrowser.get(url)
            content = captchaBrowser.page_source
            soup = BeautifulSoup(content,'html.parser')
            return soup
        else:    
            if yaml_obj.get(forum).get('Jsload') :
                js_check = yaml_obj.get(forum).get('Jsload').get('required')
                element = yaml_obj.get(forum).get('Jsload').get('element')
                wait_time = 1
            if js_check:
                try :
                    wait_time = yaml_obj.get(forum).get('Jsload').get('waittime')
                    #driver = webdriver.PhantomJS()
                    #driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
                    driver.get(url)
                    wait = WebDriverWait(driver, int(wait_time))
                    time.sleep(int(wait_time))
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, element)))
                    #time.sleep(10)
                    soup = BeautifulSoup(driver.page_source , 'lxml')
                    #print " soup  " , soup
                    driver.delete_all_cookies()
                    #driver.execute_script('localStorage.clear();')
                    #print soup
                except Exception as e :
                    print " Excep  ", e
            else:
                # Beautiful Soup is a Python library for pulling data out of HTML files
                #print "mechanize "
                if yaml_obj.get(forum).get('lxmlparser'):
                    soup = BeautifulSoup(browser.open(url).read(), 'lxml')
                    soup = BeautifulSoup(browser.open(url).read(), 'lxml') if not soup else soup
                else :
                    soup = BeautifulSoup(browser.open(url).read(), 'html.parser')   
                    soup = BeautifulSoup(browser.open(url).read(), 'html.parser') if not soup else soup
            print "open the url       ", url    
            #print "get the url       ", browser.geturl()    
                #print soup
            #print soup  
            return soup

    except Exception as e:
        print ' error at fetching soup  ',e
        forumUrls = yaml_obj.get(forum).get('WEB_URL')
        if yaml_obj.get(forum).get('Meta').get('Forum').get('extention'):
            forumUrls = yaml_obj.get(forum).get('WEB_URL') + yaml_obj.get(forum).get('Meta').get('Forum').get('extention')

        global emailcount
        count = emailcount + 1
        if url == forumUrls and count == 1:
            #sendEmail(e ,url ) 
            pass
        return None


def get_forum_urls (soup):
    r_url = yaml_obj.get(forum).get('Meta').get('Forum').get('url')

    if r_url == None:
        raise 'IN YAML File required field is not found'
    if r_url == "\\%s":
        r_url = r_url.strip('\\')
    links = soup.findAll('a', attrs={'href': re.compile(re.escape(r_url).replace('\%s',".*"))})
    url_list = list()
    for link in links:
        try:
            url = link.get('href')
            url_list.append(url)
        except:
            pass
    url_list = ' '.join (str(x.encode('utf-8')) for x in url_list)
    #return re.findall (re.escape(r_url).replace('\%s', '\S+'), str(url_list), re.I)
    if yaml_obj.get(forum).get('needSlash') :
        return re.findall (re.escape(r_url).replace('\%s', '\S*'), str(url_list), re.I)
    else :
        #print " @@@@@@@ else   @@@@@@@@@@  "
        return re.findall (re.escape(r_url).replace('\%s', '\S+'), str(url_list), re.I)

#Removing any unusual HTML content from 'soup'
def remove_words(soup, removewords_dic):
    temp = 0
    for key,value in removewords_dic.items():
        temp += 1
    temp = (temp/2)+1
    modifiedsoup = soup
    #print "before remove soup " ,soup
    for countValue in range(1,temp) :
        modifiedsoup = str(modifiedsoup).replace(str(removewords_dic.get('remove'+str(countValue))),str(removewords_dic.get('replace'+str(countValue))))
        soup = modifiedsoup

    return BeautifulSoup(str(modifiedsoup), 'lxml')


def get_resume_thread_page (engine,thread_last_page_details, f_id,t_id, thread_uuid, baseurl, t_url,t_page):
    try:
          # Check for exisiting entry in the DB.
          # If entry is not present then return 1.
        print "thread_uuid     ",thread_uuid
        _session = sessionmaker()
        _session.configure(bind=engine)
        session = _session()
        meta_dic = yaml_obj.get(forum).get('Meta')
        if thread_last_page_details >1:
            temp_lastpage = thread_last_page_details.lastpage
            #print "temp_lastpage    ",temp_lastpage
            lastpage = temp_lastpage
            while temp_lastpage>0:
                thread_url=''
                #print "before lastpage   ",lastpage
                if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page'):
                    lastpage = posts_records_per_page(lastpage)
                print "after lastpage   ",lastpage

                if str(meta_dic.get('Thread').get('page_url')).count ('%s') == 3:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, lastpage , t_page))
                elif str(meta_dic.get('Thread').get('page_url')).count ('%s') == 2:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, lastpage))
                elif str(meta_dic.get('Thread').get('page_url')).count ('%s') == 1:
                    thread_url =  t_url + (str(meta_dic.get('Thread').get('page_url')).lstrip('\\') % (lastpage))
                else :
                    page_splitUrl = meta_dic.get('Thread').get('page_url')
                    splitpageArgs = page_splitUrl.split('rem@_!@')
                    #print " splitpageArgs " ,splitpageArgs
                    for argm in range (len(splitpageArgs)-1,len(splitpageArgs)) :
                        splittedThreadUrl = t_url.split(splitpageArgs[len(splitpageArgs)-1])
                    #print " splittedThreadUrl " , splittedThreadUrl
                    thread_url  =None
                    thread_url = str(splittedThreadUrl[0])+str(splitpageArgs[1])+str(t_page)+splitpageArgs[2]

                print "before parse_content   ",lastpage
                soup = get_parse_content(thread_url)

                print "after parse_content   ",lastpage
                if soup:
                    rows = get_post_rows(soup)
                    exists_count=0
                    for row in rows:
                        post_info = get_post_info (row)
                        if post_info:
                            post_id = post_info['post_id']
                            #print "checking post_id:",post_id,"page no:", lastpage
                            #if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page'):
                            #    lastpage = (int(lastpage)/yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page'))+1

                            is_post_details_exist = session.query(
                                          Post
                            ).filter_by(third_party_id=post_id,
                            thread_uuid=thread_uuid).first()
                            if is_post_details_exist:
                                exists_count = exists_count+1
                                if exists_count >1:
                                    #print "found and returning thread_uuid:", thread_uuid, "lastpage:",lastpage
                                    session.close()
                                    print "lasr page is    ", lastpage
                                    return lastpage

                temp_lastpage = temp_lastpage-1
                #print "lastpage:",lastpage," thread_uuid:",thread_uuid
            print "found but had to return 1 thread_uuid:", thread_uuid, "lastpage:",lastpage
            session.close()
            print  "after session close    "
            return 1
        else:
            print "do not found 1 thread_uuid:", thread_uuid
            session.close()
            return 1
    except Exception as e:
        print "exception occurred",e
        session.close()
        return 1


def get_thread_total_page_count (soup, url):
    '''
        Get given url pages count by pagination
    '''
    try:
        total_pages = 1
        pagenav_dic = yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav')
        sub = yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('subtag')
        pagenav = None
        if soup :
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
                    if not pagenav_dic.get('subclass') :  
                        total_pages = max(last)
                    else :
                          lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                          #print " lastPage " , lastPage
                          if lastPage :
                              lastPage = lastPage.text.strip()
                          else :
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
                    if lastPage :
                        lastPage = lastPage.text.strip()
                    else :
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
                    print "findind a  ",pageList
                #print "findind a  ",pagenav
                #print "findind a  pageList ",pageList
                if total_pages:
                    last = [int(s) for s in pageList if s.isdigit()]
                    #print "lasr					",last
                    if last:
                        total_pages = max(last)
                else:
                    total_pages = 1
    except Exception as e:
        total_pages = 1
        print "+++++++++++++++++++++++++++++++++", traceback.print_exception(*sys.exc_info()), "+++++++++++++++++++++++++++++++"
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", url
    return total_pages


def get_post_total_page_count (soup, url):
    '''
        Get given url pages count by pagination
    '''
    try:
            total_pages = 1
            pagenav_dic = yaml_obj.get(forum).get('Meta').get('Post').get('pagenav')
            sub = yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('subtag')
            pagenav = None
            if soup :
                #print "   soup  at getting pagination  " , soup
                pagenav = soup.find(pagenav_dic.get('tag'), {'class': pagenav_dic.get('class') })
                #print " pagenav  " ,pagenav
            if pagenav:
                if pagenav_dic.get('subtag'):
                    pagesList = list()
                    rawList = pagenav.find_all(sub)
                    for a in rawList:
                        pagesList.append(a.text)
                    last = [int(s) for s in pagesList if s.isdigit()]
                    if len(last) > 0:
                        if not pagenav_dic.get('subclass') :
                            total_pages = max(last)
                        else : 
                            lastPage = pagenav.find(pagenav_dic.get('subtag'), {'class': pagenav_dic.get('subclass')})
                            #print "  lastPage " , lastPage
                            if lastPage :
                                lastPage = lastPage.text.strip()
                            else :
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
                        if lastPage :
                            lastPage = lastPage.text.strip()
                        else :
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
    except Exception as e:
        total_pages = 1
        print "+++++++++++++++++++++++++++++++++", traceback.print_exception(*sys.exc_info()), "+++++++++++++++++++++++++++++++"
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", url
    return total_pages

def get_thread_rows (soup, f_id):
    tbody_dic = yaml_obj.get(forum).get('Meta').get('Thread').get('soup').get('seperator')

    _attrs = {}
    for key,value in tbody_dic.items():
        if value and key != 'tag':
            if '%s' in value:
                if key == 'id':
                    value = value % f_id
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if tbody_dic.get('tag'):
        if yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('mainThreadseparateelement') :
            print  " rows length  " , (yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('mainThreadseparateelement'))
            tbody = soup.find_all(tbody_dic.get('tag'), attrs=_attrs)[int(yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('mainThreadseparateelement'))] 
        else :
            tbody = soup.find(tbody_dic.get('tag'), attrs=_attrs)
    else:
        tbody = soup

    tbody_dic = yaml_obj.get(forum).get('Meta').get('Thread').get('find').get('seperator')
    _attrs = {}
    for key,value in tbody_dic.items():
        if value and key != 'tag':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    rows = tbody.findAll(tbody_dic.get('tag'), attrs=_attrs) if tbody else []
    return rows

def get_thread_info (row, baseurl):
    thread_name = ''
    thread_id = None
    thread_date = None
    t_dic = yaml_obj.get(forum).get('Meta').get('Thread').get('find')
    #print " row  " , row
    # parsing thread name
    _attrs = {}
    for key,value in t_dic.get('title').items():
        if value and key != 'tag' and key != 'get':
            if isinstance(value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)

    thread_title = row.find(t_dic.get('title').get('tag'), attrs=_attrs)
    if thread_title:
        if t_dic.get('title').get('get').get('value'):
            thread_name = thread_title.get(t_dic.get('title').get('get').get('value'))
            if thread_name :
                thread_name = thread_name.encode('utf-8')
        else:
            thread_name = thread_title.text.encode('utf-8')

        # Parsing thread url
        thread_url = thread_title.get('href')
        if not thread_url :
            thread =  thread_title.find('a')
            if thread :
                thread_url = thread.get('href')
        thread_url = urlparse.urljoin(baseurl, thread_url)
        thread_url = str(thread_url).replace('../','')

        # Parsing thread id
        if t_dic.get('t_id') and not t_dic.get('t_id').get('tag'):        
            thread_id = t_dic.get('t_id').get('get').get('value')
            thread_id = row.get(thread_id)
            if thread_id :
                list_threads =  re.findall("([\d]+)",str(thread_id))
                thread_id =max([int(i) for i in list_threads])
            print "thread_id ::",thread_id
        elif t_dic.get('t_id'):
            _attrs = {}
            for key,value in t_dic.get('t_id').items():
                if value and key != 'tag' and key != 'get':
                    if isinstance(value, list):
                        _attrs[key] = value
                    else:
                        _attrs[key] = re.compile(value)
            raw_thread_id = row.find(t_dic.get('t_id').get('tag'), attrs=_attrs)
            thread_id = raw_thread_id.get(t_dic.get('t_id').get('get').get('value')) if raw_thread_id else None
            if thread_id :
                list_threads =  re.findall("([\d]+)",str(thread_id))
                thread_id =max([int(i) for i in list_threads])
        else:
            raw_thread_id = thread_title.get('id')
            if raw_thread_id:
                list_threads =  re.findall("([\d]+)", str(raw_thread_id))
                thread_id =max([int(i) for i in list_threads])
                if not str(thread_id) :
                   list_threads =  re.findall("([\d]+)", str(thread_url))
                   thread_id =max([int(i) for i in list_threads])
            elif thread_url:
                list_threads =  re.findall("([\d]+)", str(thread_url))
                if list_threads:
                    thread_id =max([int(i) for i in list_threads])
                #thread_id = max(re.findall("([\d]+)", str(thread_url)))
        if not thread_id :
            thread_id = int(hashlib.md5(thread_name+thread_url).hexdigest(), 16)

        #print " thread_id  " , thread_id
        # commented by suresh due to the following condition gives none when thread id not present in url
        #if str(thread_id) not in str(thread_url):
        #    print " thread none  "
        #    return None
    else:
        return None
    last_post_date=None
    datetype = 'Thread'
    if t_dic.get('last_post_date') :
        try:
            _attrs = {}
            selectorType = ''
            selector = None
            print " In last_post_date  "
            for key,value in t_dic.get('last_post_date').items():
                print "key  ",key
                print "value  ",value
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else :
                     if value :
                        elementtag = value
            print "selector  ",selector
            date_post = find_ele(row, elementtag  ,selectorType , selector, t_dic)
            last_post_date = date_post
            #print " post_date error finding " , last_post_date
            encodedDateText = "SWfDpXI="
            if last_post_date:
                if encodedDateText.decode('base64') in last_post_date :
                    postdateEncoder = str((last_post_date.encode('base64')).replace(encodedDateText,'WWVzdGVyZGF5'))
                    last_post_date= postdateEncoder.decode('base64')
                #print "BEFORE ::",last_post_date
                if is_date(last_post_date):
                    last_post_date = get_utc(last_post_date)
                    print "is_date--",last_post_date
                    if last_post_date > datetime.utcnow():
                        last_post_date = datetime.utcnow()
                        #print "is_date--",last_post_date
                else:
                    last_post_date = datetime.utcnow()
                    #print "In else",last_post_date
                #print "AFTER :: post date",last_post_date
            else:
                last_post_date = datetime.utcnow()
                #print "Outer else---",last_post_date
        except Exception as date_exe:
            last_post_date = datetime.utcnow()
            print "exception block else---",last_post_date
    else :
        last_post_date = datetime.utcnow()
        print "post_date   ",last_post_date
    # parsing date
    if t_dic.get('date') :
        try:
            _attrs = {}
            for key, value in t_dic.get('date').items():
                if value and key != 'tag':
                    if isinstance (value, list):
                        _attrs[key] = value
                    else:
                        _attrs[key] = re.compile(value)
            rawdate = row.find(t_dic.get('date').get('tag'), attrs=_attrs)
            threaddate = rawdate.text.encode('utf-8').strip()
            encodedDateText = "SWfDpXI="
            if is_date(threaddate):
                if encodedDateText.decode('base64') in threaddate :
                    threaddateEncoder = str((threaddate.encode('base64')).replace(encodedDateText,'WWVzdGVyZGF5'))
                    threaddate= threaddateEncoder.decode('base64')
            else:
                pass
            thread_date = get_utc(threaddate)
            if thread_date:
                if thread_date > datetime.utcnow():
                    thread_date = datetime.utcnow()
            else:
                thread_date = datetime.utcnow()
            #print "AFTER ::",thread_date
        except Exception as date_exe:
            thread_date = datetime.utcnow()
    else:
        thread_date = datetime.utcnow()

    print "thread_url    ", thread_url

    return {'thread_date' : thread_date, 'thread_name' : thread_name, 'thread_url': thread_url, 'thread_id': thread_id, 'last_post_date': last_post_date}


def get_post_rows (soup):
    post_dic = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('seperator')
    
    if  yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmainseparator'):
        _attrs = {}
        post_seperator = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmainseparator')
        if post_seperator.get('number'):
             soup = soup.find_all(post_seperator.get('tag'))[int(post_seperator.get('number'))]
        else :
            for key,value in post_seperator.items():
                if value and key != 'tag':
                    _attrs[key] = re.compile(value)
            #print "  post_seperator.get('tag') " , post_seperator.get('tag') 
            soup = soup.find(post_seperator.get('tag'), attrs=_attrs)
    #print " ***** soup after replace removewords *****" , soup
    _attrs = {}
    for key,value in post_dic.items():
        if value and key != 'tag':
            _attrs[key] = re.compile(value)
    rows = soup.findAll(post_dic.get('tag'), attrs=_attrs)
    # print " No of rows " , len(rows)
    return rows

def get_comment_rows(soup):
    post_dic = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('seperator')
    
    if  yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmainseparator'):
        _attrs = {}
        post_seperator = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmainseparator')
        if post_seperator.get('number'):
             soup = soup.find_all(post_seperator.get('tag'))[int(post_seperator.get('number'))]
        else :
            for key,value in post_seperator.items():
                if value and key != 'tag':
                    _attrs[key] = re.compile(value)
            #print "  post_seperator.get('tag') " , post_seperator.get('tag') 
            soup = soup.find(post_seperator.get('tag'), attrs=_attrs)
    #print " ***** soup after replace removewords *****" , soup
    _attrs = {}
    for key,value in post_dic.items():
        if value and key != 'tag':
            _attrs[key] = re.compile(value)
    rows = soup.findAll(post_dic.get('tag'), attrs=_attrs)
    # print " No of rows " , len(rows)
    return rows

def get_post_info (row):
    post_id = None
    member_name = ''
    post_date = None
    post_body = ''
    post_dic = yaml_obj.get(forum).get('Meta').get('Post').get('find')
    _attrs = {}
    for key,value in post_dic.get('name').items():
        if value and key != 'tag':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    post_member = row.find(post_dic.get('name').get('tag'), attrs=_attrs)
    if post_member :
        member_name = post_member.text.encode('utf-8').strip()

    #print "  row ", row
    # parsing id
    _attrs = {}
    for key,value in post_dic.get('p_id').items():
        if value and key != 'tag' and key != 'get':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if post_dic.get('p_id').get('tag'):
        raw_post = row.find (post_dic.get('p_id').get('tag'), attrs=_attrs)
        if raw_post :
            raw_post = raw_post.get(post_dic.get('p_id').get('get').get('value'))
            #print "raw_post      ",raw_post
            if raw_post :
                post_idcontx = re.search ("([\d]+)", raw_post) 
                if  post_idcontx :
                    post_id = re.search ("([\d]+)", raw_post).group(1)
            if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('postIdAll') :
                post_ids = re.findall("([\d]+)", raw_post) 
                post_id = max(post_ids)
           
            #print  "  post_id  " , post_id
    else:
        raw_post = row.get(post_dic.get('p_id').get('get').get('value'))
        if raw_post :
            post_idsArray = re.search ("([\d]+)", raw_post)
            if post_idsArray :
               post_id = re.search ("([\d]+)", raw_post).group(1)

    # parsing message
    _attrs = {}
    for key,value in post_dic.get('message').items():
        if value and key != 'tag':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    post_message = row.find(post_dic.get('message').get('tag') , attrs=_attrs)
    if post_message:
        post_body = post_message.text.strip().encode('utf-8')
    elementtag = None

    if yaml_obj.get(forum).get('textTopost') :
          post_id = int(hashlib.md5(post_body+member_name).hexdigest(), 16)
    if not post_id and post_body!='' and member_name!='' :
          post_id = int(hashlib.md5(post_body+member_name).hexdigest(), 16)
    # parsing date
    _attrs = {}
    if post_dic.get('date') :
        try:
            selectorType = ''
            selector = None
            _attrs = {}
            for key,value in post_dic.get('date').items():
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else :
                    if value : 
                        elementtag = value
            datetype = 'Post'
            date_post = find_ele(row, elementtag  ,selectorType , selector, post_dic)
            post_date = date_post
            #print " post_date error finding " , post_date
            encodedDateText = "SWfDpXI="
            if post_date:
                if encodedDateText.decode('base64') in post_date :
                    postdateEncoder = str((post_date.encode('base64')).replace(encodedDateText,'WWVzdGVyZGF5'))
                    post_date= postdateEncoder.decode('base64')
                #print "BEFORE ::",post_date
                if is_date(post_date):
                    post_date = get_utc(post_date)
                    if post_date > datetime.utcnow():
                        post_date = datetime.utcnow()
                else:
                    post_date = datetime.utcnow()
                #print "AFTER :: post date",post_date
            else:
                post_date = datetime.utcnow()
        except Exception as date_exe:
            post_date = datetime.utcnow()
            print "Exception in ",sys.exc_traceback.tb_lineno
    else :
        post_date = datetime.utcnow()

    return {'post_date' : post_date, 'post_body' : post_body, 'member_name': member_name, 'post_id': post_id, 'post_urls' : post_message}

def get_comment_info(row):
    comment_id = None
    member_name = ''
    comment_date = None
    comment_body = ''
    comment_dic = yaml_obj.get(forum).get('Meta').get('Comment').get('find')
    _attrs = {}
    for key,value in comment_dic.get('name').items():
        if value and key != 'tag':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    comment_member = row.find(comment_dic.get('name').get('tag'), attrs=_attrs)
    #print "comment_member---",comment_member
    if comment_member :
        member_name = comment_member.text.encode('utf-8').strip()

    #print "  row in post ", row
    # parsing id
    _attrs = {}
    for key,value in comment_dic.get('p_id').items():
        if value and key != 'tag' and key != 'get':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    if comment_dic.get('p_id').get('tag'):
        raw_comment = row.find (comment_dic.get('p_id').get('tag'), attrs=_attrs)
        if raw_comment :
            raw_comment = raw_comment.get(comment_dic.get('p_id').get('get').get('value'))
            if raw_comment :
                comment_idcontx = re.search ("([\d]+)", raw_comment) 
                if  comment_idcontx :
                    comment_id = re.search ("([\d]+)", raw_comment).group(1)
            if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('postIdAll') :
                comment_ids = re.findall("([\d]+)", raw_comment) 
                comment_id = max(comment_ids)
           
            #print  "  comment_id  " , comment_id
    else:
        raw_comment = row.get(comment_dic.get('p_id').get('get').get('value'))
        if raw_comment :
            comment_idsArray = re.search ("([\d]+)", raw_comment)
            if comment_idsArray :
               comment_id = re.search ("([\d]+)", raw_comment).group(1)

    # parsing message
    _attrs = {}
    for key,value in comment_dic.get('message').items():
        if value and key != 'tag':
            if isinstance (value, list):
                _attrs[key] = value
            else:
                _attrs[key] = re.compile(value)
    comment_message = row.find(comment_dic.get('message').get('tag') , attrs=_attrs)
    if comment_message:
        comment_body = comment_message.text.strip().encode('utf-8')
    elementtag = None

    if yaml_obj.get(forum).get('textTopost') :
          comment_id = int(hashlib.md5(comment_body+member_name).hexdigest(), 16)

    if not comment_id and comment_body!='' and member_name!='' :
          comment_id = int(hashlib.md5(comment_body+member_name).hexdigest(), 16)
    # parsing date
    _attrs = {}
    if comment_dic.get('date') :
        try:
            _attrs = {}
            selectorType = ''
            selector = None
            
            for key,value in comment_dic.get('date').items():
                if value and key != 'tag':
                    selector = value
                    selectorType = key
                else : 
                     if value : 
                        elementtag = value
            datetype = 'Comment'
            date_comment = find_ele(row, elementtag  ,selectorType , selector, comment_dic)
            comment_date = date_comment
            #print " comment_date error finding " , comment_date
            encodedDateText = "SWfDpXI="
            if comment_date:
                if encodedDateText.decode('base64') in comment_date :
                    commentdateEncoder = str((comment_date.encode('base64')).replace(encodedDateText,'WWVzdGVyZGF5'))
                    comment_date= commentdateEncoder.decode('base64')
                #print "BEFORE ::",comment_date
                if is_date(comment_date):
                    comment_date = get_utc(comment_date)
                    #print "is_date--",comment_date
                    if comment_date > datetime.utcnow():
                        comment_date = datetime.utcnow()
                        #print "is_date--",comment_date
                else:
                    comment_date = datetime.utcnow()
                    #print "In else",comment_date
                #print "AFTER :: comment date",comment_date
            else:
                comment_date = datetime.utcnow()
                #print "Outer else---",comment_date
        except Exception as date_exe:
            comment_date = datetime.utcnow()
            #print "exception block else---",comment_date    
    else :
        comment_date = datetime.utcnow()
        #print "comment_date   ",comment_date
    return {'comment_date' : comment_date, 'comment_body' : comment_body, 'member_name': member_name, 'comment_id': comment_id, 'comment_type': 'comment', 'comment_urls' : comment_message}

#TO check provided string has valid date or not
def is_date(date_string):
    try:
        parse(date_string)
        #print "     string   ", date_string
        return True
    except Exception as e:
        #print " in is_date exception  ",e
        return False

#To get Required format of given date
def get_utc(givendate):
    try:
        post_dic = yaml_obj.get(forum).get('Meta').get('Post').get('find')
        if(post_dic.get('date_setting')):
            post_dic=post_dic.get('date_setting')
        format = None
        datemode = None
        order = None
        prestring = None
        poststring = None
        timezone = None
        parsed_Date = None
        #print "before string_format    ", post_dic.get('string_format')
        if(post_dic.get('required')):
            datemode = post_dic.get('type')
            format = post_dic.get('format')
            #order = post_dic.get('order')
            prestring = post_dic.get('pre_string')
            poststring = post_dic.get('post_string')
            language = post_dic.get('language')
            timezone = post_dic.get('tz')
            try:
                if(post_dic.get('pre_string')):
                    for val in post_dic.get('pre_string'):
                        givendate = givendate.replace(val,"")
                if(language):
                    parsed_Date = parse(givendate, languages=[language])
                elif(format == 'DMY'):
                    parsed_Date = parse(givendate, settings={'DATE_ORDER': 'DMY'})
                elif(format == 'MDY'):
                    parsed_Date = parse(givendate, settings={'DATE_ORDER': 'MDY'})
                else:
                    parsed_Date = parse(givendate)
            except ValueError:
                return datetime.utcnow()
        else:
            parsed_Date = parse(givendate)
        try: 
            if(post_dic.get('string_format')):
                parsed_Date = datetime.strptime(givendate,post_dic.get('string_format'))
        except Exception as e:
            parsed_Date = parse(givendate)
        if parsed_Date == None: # If date string has combination of strings and date
            try:
                parsed_Date = dparser.parse(givendate, fuzzy=True)
            except ValueError:
                parsed_Date = datetime.utcnow()
        #print "-----final parsed_Date after------", datetime.combine(parsed_Date.date(),parsed_Date.time())
        return datetime.combine(parsed_Date.date(),parsed_Date.time())
    except ValueError:
        return datetime.utcnow()

def posts_records_per_page(page):
    page_count = page
    try :
        pagenav_dic = yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page')
        if pagenav_dic:
            page = int(page)
            page = (page - 1) * pagenav_dic
            page_count = page
        return page_count
    except Exception as e2 :
        print " exception in posts_records_per_page ", e2
        return page_count

def thread_records_per_page(page):
    page_count = page
    try :
        pagenav_dic = yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('threads_per_page')
        if pagenav_dic:
            page = int(page)
            page = (page - 1) * pagenav_dic
            page_count = page
        return page_count

    except Exception as e2 :
        print " exception in thread_records_per_page ", e2
        return page_count

def find_ele(root, tag , key ,selector,date_info):
    #print "datetype     ",datetype
    #print "in find_ele  ",tag,"key",key
    seloperators=selector.split()
    _attrs = {}
    #print " root            is          ", root
    if selector :
        if isinstance (seloperators[0], list):		
             _attrs[key] = seloperators[0]		
        else:		
             _attrs[key] = re.compile(seloperators[0])		
    		
        if seloperators[0] != 'False' :		
            #print " in true "		
            root = root.find(tag , _attrs)
        mainTest = root
    else :
        root = root.find(tag , _attrs)
        mainTest = root
    print " original root here     ", root
    if(date_info.get('date_setting')):
        date_info = date_info.get('date_setting')
    for index in range(1,len(seloperators)):
        if seloperators[index] == '>':
            root = root.next_Sibling
        elif seloperators[index] == '<':
            root = root.previous_sibling
        #elif (seloperators[index].startswith('~'))
        else:
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
                nthchildcount = int(childoperator.split('@')[1])
                root = root.find_all(childtag)[nthchildcount-1]
    #print " original root here2     ", root
    try:
        if (date_info.get('parent_tag_text_num')):
            print "from data type",datetype
            print " test here     ", ' '.join(map(str,root(text=True, recursive=False)))
            root = ' '.join(map(str,root(text=True, recursive=False)))
        else:
            attr_tag = None
            if(date_info.get('tag')):
                attr_tag = date_info.get('tag')
                index = int(attr_tag.split('@')[1])
                attr_tag = attr_tag.split('@')[0]
                if(index == 0):
                    #print "inside of find attr     "
                    root = root[date_info.get('get').get('value')]
                elif(index == 1):
                    root = root.find(attr_tag)[date_info.get('get').get('value')]
            else:
                root=root.text

    except Exception as e:
        #print "exception here    ",e
        root=root.text
    ##print "final root here  ", root
    #print " final root here     ", root
    return str(root).encode('utf-8')


def sendEmail(error , url) :
    msg = MIMEMultipart()
    msg['From'] = 'sureshborra@vidyayug.com'
    receipients = ['chaitanya.cheekate@vidyayug.com','shekark@vidyayug.com','sureshborra@vidyayug.com','anupam822@gmail.com']
    msg['To'] = ", ".join(receipients)
    msg['Subject'] = 'Forum is Down'
    message = "Hi Team , \n Forum url :  %s \n Error Description: %s"%(url , error)
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('sureshborra@vidyayug.com', 'Vidyayug@123')
    
    mailserver.sendmail('sureshborra@vidyayug.com',receipients,msg.as_string())
    
    mailserver.quit()

