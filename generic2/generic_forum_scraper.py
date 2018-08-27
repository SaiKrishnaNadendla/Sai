# appending the path to find core libraries
import sys
import os
import yaml

# Below line is required only in production. So please comment below line in dev mode.
# os.chdir('/home/ityug/scraper/generic')
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)
#os.chdir('..')
initializeYaml_obj = None
with open(r'instance_settings.yaml', 'r') as stream:
    try:
        initializeYaml_obj = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise

reload(sys)
sys.setdefaultencoding('utf-8')
os.chdir(current_path)
sys.path.append(os.path.dirname(os.path.realpath(__name__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__name__))))

# import all required modules
from generic import *
from generic import YAML_OBJ as yaml_obj
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

# import required type module from core directory
t_module = importlib.import_module('core.' + yaml_obj[forum]['TYPE'])

# initialize db
# during development uncomment below lines
# if not args.debug:
#    generic_initialize_db.initialize_db (forum, args.rawhtml)

PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))
LOG_PATH = os.path.join(PROJECT_ROOT, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
DB_URL = 'mysql://' + initializeYaml_obj.get('DB_USERNAME') + ':' + initializeYaml_obj.get(
    'DB_PASSWORD') + '@' + initializeYaml_obj.get('HOST') + '/' + initializeYaml_obj.get('DB_NAME') + '?charset=utf8'
baseurl = yaml_obj[forum]['WEB_URL']
loginUrl = yaml_obj[forum]['LOGIN_URL']

# Define Queue
q = Queue(2 * yaml_obj[forum]['NUM_THREADS'])
threadLock = threading.Lock()

# Log file info
logfilename = LOG_PATH + '/' + yaml_obj[forum]['PROJECT'] + '_' + datetime.now().strftime("%Y_%m_%d") + '.log'
logging.basicConfig(
    name=yaml_obj[forum]['PROJECT'],
    level=logging.DEBUG,
    format=' %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=logfilename
)

engine = create_engine(DB_URL)
_session = sessionmaker()
# print " memory  ",sys.getsizeof(_session)
_session.configure(bind=engine)
failed_thread_list = list()
failed_post_list = list()


def parse_forum():
    """ List all forum urls """
    try:
        if yaml_obj.get(forum).get('Meta').get('Forum').get('extention'):
            soup = t_module.get_parse_content(baseurl + yaml_obj.get(forum).get('Meta').get('Forum').get('extention'))
            soup = t_module.get_parse_content(baseurl + yaml_obj.get(forum).get('Meta').get('Forum').get('extention'))
        else:
            soup = t_module.get_parse_content(baseurl)
            soup = t_module.get_parse_content(baseurl)
        # print 'soup ' , soup
        forum_urls = t_module.get_forum_urls(soup)
        logging.debug('%s' % forum_urls)
        if yaml_obj.get(forum).get('subforums'):
            if yaml_obj.get(forum).get('subforums').get('type') == 'include':
                forum_urls = yaml_obj.get(forum).get('subforums').get('values')
            elif yaml_obj.get(forum).get('subforums').get('type') == 'exclude':
                removeUrls = yaml_obj.get(forum).get('subforums').get('values')
                print "  removeUrls ", removeUrls
                ### converts to set to remove duplicates
                forum_set_urls = set(removeUrls)
                set_forum_urls = set(forum_urls) - (forum_set_urls)
                forum_urls = list(set_forum_urls)
            print('forum_urls after  %s' % forum_urls)
        print forum_urls
        forum_urls = list(set(forum_urls))
        for forum_url in forum_urls:
            # print 'baseurlinforumsurl  ' , yaml_obj.get(forum).get('baseurlinforumsurl')
            if not yaml_obj.get(forum).get('baseurlinforumsurl'):
                forum_url = urlparse.urljoin(baseurl, forum_url)
            if not args.debug:
                # parse_thread(forum_url)
                q.put(forum_url)

    except Exception as e:
        if yaml_obj.get(forum).get('Meta').get('Forum').get('extention'):
            logging.exception('*************** Main Url exception :\t %s  ' % (
                        baseurl + yaml_obj.get(forum).get('Meta').get('Forum').get('extention')))
        else:
            logging.exception('*************** Main Url exception :\t %s ' % str(baseurl))
        logging.exception(' %s ' % traceback.print_exception(*sys.exc_info()))


def parse_thread(f_url):
    """
        List all threads by forum url and
        store thread information
    """
    forum_url = None
    check_text = 'NoDuplicate'
    try:

        soup = t_module.get_parse_content(f_url)
        print "soup   ", soup
        forum_url = f_url
        r_url = yaml_obj.get(forum).get('Meta').get('Forum').get('url')
        # f_id = int(re.search(re.escape(r_url).replace('\%s', '([\d]+)'), f_url, re.I).group(1))
        f_id = re.search(re.escape(r_url).replace('\%s', '(\S+)'), f_url, re.I).group(1)
        if yaml_obj.get(forum).get('Meta').get('Thread').get('soup').get('removewords'):
            list_words = yaml_obj.get(forum).get('Meta').get('Thread').get('soup').get('removewords')
            soup = t_module.remove_words(soup, list_words)

        if soup:
            forum_uuid = yaml_obj[forum]['FORUM_UUID']
            # Get all thread list pages by pagination
            temp_pages = t_module.get_thread_total_page_count(soup, f_url)
            total_pages = temp_pages
            logging.info("total Forum Pages : %s   url  %s" % (total_pages, f_url))
            print "total Forum Pages : ", total_pages
            page = 1
            temp_page = 1
            # for page in range(1, total_pages + 1):
            while temp_page < total_pages + 1:
                page = temp_page
                # Initial Session
                # If page count not increment sequentially then give in threads_per_page
                if yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav').get('threads_per_page'):
                    page = t_module.thread_records_per_page(page)

                if str(yaml_obj.get(forum).get('Meta').get('Forum').get('page_url')).count('%s') == 2:
                    if page != 1:
                        forum_url = baseurl + (
                                    str(yaml_obj.get(forum).get('Meta').get('Forum').get('page_url')) % (f_id, page))
                else:
                    forum_url = f_url + (
                                str(yaml_obj.get(forum).get('Meta').get('Forum').get('page_url')).lstrip('\\') % (page))

                # checking Pagination again because sometimes limited pagination visible in current page, then update max pages
                if yaml_obj.get(forum).get('Meta').get('Thread').get('pagenav'):
                    current_page_max = t_module.get_thread_total_page_count(soup, forum_url)
                    if current_page_max > total_pages:
                        # print "Pagination Updated From :%s To :%s "%(temp_pages,current_page_max)
                        total_pages = current_page_max
                logging.info('------------------->Forum URL: %s ' % forum_url)
                soup = t_module.get_parse_content(forum_url)
                if yaml_obj.get(forum).get('Meta').get('Thread').get('soup').get('removewords'):
                    list_words = yaml_obj.get(forum).get('Meta').get('Thread').get('soup').get('removewords')
                    soup = t_module.remove_words(soup, list_words)

                # print "soup",soup
                if not soup:
                    failed_thread_list.append(forum_url)
                    temp_page = temp_page + 1
                    continue
                rows = t_module.get_thread_rows(soup, f_id)
                logging.debug(" thread rows :: %s " % len(rows))
                print "  thread rows :: ", len(rows)
                for row in rows:
                    # thread_info = t_module.get_thread_info (row, baseurl)
                    if yaml_obj.get(forum).get("includethreadurl"):
                        thread_info = t_module.get_thread_info(row, f_url)
                    else:
                        thread_info = t_module.get_thread_info(row, baseurl)

                    if thread_info:
                        thread_date = thread_info['thread_date']
                        thread_name = thread_info['thread_name']
                        thread_url = thread_info['thread_url']
                        thread_id = thread_info['thread_id']
                        last_post_date = thread_info['last_post_date']
                    else:
                        # temp_page = temp_page+1
                        continue
                    # create session
                    session = _session()
                    skipThread = False
                    # Check for exisiting entry in the DB.
                    # If entry is not present then add it to DB
                    if yaml_obj.get(forum).get('newdomain'):
                        old_domainUrl = str(thread_url).replace(yaml_obj.get(forum).get('WEB_URL'),
                                                                yaml_obj.get(forum).get('oldDomainUrl'))
                        is_thread_exists_witholddomain = session.query(
                            Topic
                        ).filter_by(url=old_domainUrl, third_party_id=thread_id).first()
                        if is_thread_exists_witholddomain:
                            thread_uuid1 = is_thread_exists_witholddomain.uuid
                            is_new_post_exist = session.query(func.max(Post.created_at)).filter_by(
                                thread_uuid=thread_uuid1).one()
                            print ('  THread Name   ', str(thread_name))
                            print('---------> is_new_post_exist[0]', str(is_new_post_exist[0]))
                            print('---------> Thread last_post_date', str(last_post_date))
                            if is_new_post_exist[0] == last_post_date:
                                print "Both dates equal  "
                                skipThread = True
                            if not skipThread:
                                print "****************Thread related post's not exists****************"
                                if not args.debug:
                                    parse_post(thread_url, thread_id, f_id, thread_uuid1, page, check_text)
                            continue
                    # Check for exisiting entry in the DB.
                    # If entry is not present then add it to DB.
                    is_thread_details_exist = session.query(
                        Topic
                    ).filter_by(url=thread_url, third_party_id=thread_id).first()
                    store_thread_url = thread_url
                    if yaml_obj.get(forum).get('remove_string') and not is_thread_details_exist:
                        store_thread_url = thread_url.split(str(yaml_obj.get(forum).get('remove_string')))[0]
                    logging.debug(" is_thread_details_exist %s " % is_thread_details_exist)
                    # print('---------> Forum URL', str(forum_url))
                    if yaml_obj.get(forum).get('searchurlonly') and not is_thread_details_exist:
                        trim_thread_url = store_thread_url.replace('http://', '').replace('https://', '')
                        is_thread_details_exist = session.query(Topic).filter(
                            (Topic.url == 'http://' + trim_thread_url) | (
                                        Topic.url == 'https://' + trim_thread_url)).first()
                        if not is_thread_details_exist and yaml_obj.get(forum).get('update_url'):
                            is_thread_details_exist = session.query(Topic).filter(
                                Topic.url.like(str(store_thread_url) + '%')).first()
                            if is_thread_details_exist:
                                is_thread_details_exist.url = thread_url
                        if is_thread_details_exist and yaml_obj.get(forum).get('update_third_party_id'):
                            is_thread_details_exist.third_party_id = thread_id
                        try:
                            # Commit the changes.
                            session.commit()
                        except IntegrityError as ie:
                            session.rollback()
                            session.close()
                            logging.exception(" Exception during update threads insertion %s " % ie)
                            continue
                    if yaml_obj.get(forum).get('thirdpartyidonly') and not is_thread_details_exist:
                        is_thread_details_exist1 = session.query(Topic).filter_by(third_party_id=thread_id,
                                                                                  forum_uuid=forum_uuid).first()
                        if is_thread_details_exist1:
                            t_module.sendEmail(thread_url, thread_id)

                    if not is_thread_details_exist:
                        thread_uuid = str(uuid.uuid4())
                        logging.info('--------->Thread Name \t %s ' % str(thread_name))
                        print "--------->Thread Name \t ", thread_name

                        # Add data to database
                        topic = Topic(uuid=thread_uuid, forum_uuid=forum_uuid,
                                      third_party_id=thread_id, name=thread_name,
                                      created_at=thread_date, url=thread_url)

                        # Save object to the database.
                        #session.add(topic)
                        #session.flush()
                        try:
                            session.add(topic)
                            session.flush()
                            # Commit the changes.
                            session.commit()
                        except IntegrityError as ie:
                            # session.rollback()
                            # session closing here
                            check_text = 'Duplicate'
                            session = _session()
                            print "in duplicate error raised"
                            is_thread_details_exist1 = session.query(Topic).filter_by(third_party_id=thread_id,
                                                                                      forum_uuid=forum_uuid).first()
                            thread_uuid = is_thread_details_exist1.uuid
                            if not args.debug:
                                parse_post(thread_url, thread_id, f_id, thread_uuid, page, check_text)
                            logging.exception(" Exception during threads insertion %s " % ie)
                            session.close()
                            continue
                    else:
                        thread_uuid = is_thread_details_exist.uuid
                        is_new_post_exist = session.query(func.max(Post.created_at)).filter_by(
                            thread_uuid=thread_uuid).one()
                        print ('  THread Name   ', str(thread_name))
                        print('---------> is_new_post_exist[0]', str(is_new_post_exist[0]))
                        print('---------> Thread last_post_date', str(last_post_date))
                        if is_new_post_exist[0] == last_post_date:
                            print "Both dates equal  "
                            skipThread = True

                    # Session Close
                    session.close()

                    # Get all Threads by each forum
                    if not skipThread:
                        print "****************Thread related post's not exists****************"
                        if not args.debug:
                            parse_post(thread_url, thread_id, f_id, thread_uuid, page, check_text)
                    else:
                        print " this threads has no latest posts  forum_url : ", forum_url, '  thread_name : ', thread_name
                temp_page = temp_page + 1
        else:
            failed_thread_list.append(forum_url)
            logging.debug("** %s ***" % forum_url)
    except Exception as e:
        logging.exception('*** Forum URL exception :\t %s ' % str(forum_url))
        failed_thread_list.append(forum_url)
        logging.exception(' %s ' % traceback.print_exception(*sys.exc_info()))


def parse_post(t_url, t_id, f_id, thread_uuid, t_page, check_text):
    """ List all posts by thread url and
        store post information
    """
    try:
        logging.info('---Thread URL: %s ' % t_url)
        thread_url = t_url
        if yaml_obj.get(forum).get('Login').get('phantom'):
            soup = t_module.get_parse_content(t_url)
        soup = t_module.get_parse_content(t_url)
        meta_dic = yaml_obj.get(forum).get('Meta')
        if yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('removewords'):
            list_words = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('removewords')
            soup = t_module.remove_words(soup, list_words)

        if soup:
            # Get all thread list pages by pagination
            post_dic = meta_dic.get('Post')
            total_pages = t_module.get_post_total_page_count(soup, t_url, post_dic)
            session = _session()
            # resume thread pagination logic
            # get thread's last page visit
            last_page_details_exist = session.query(
                ThreadLastpage
            ).filter_by(thread_uuid=thread_uuid).first()
            # session.close()
            sequence_num = 0
            # Get the sequence number if already exists
            getPostMax_Sequence = session.query(
                func.max(Post.sequence_number)
            ).filter_by(thread_uuid=thread_uuid, type='post').first()
            if getPostMax_Sequence[0] is None:
                sequence_num = 0
            else:
                sequence_num = getPostMax_Sequence[0] + 1
            # calculate start page of thread
            session.close()
            start_page = 1
            if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav'):
                start_page = t_module.get_resume_thread_page(engine, last_page_details_exist, f_id, t_id, thread_uuid,
                                                             baseurl, t_url, t_page)
            logging.info("  total_post_pages %s " % total_pages)
            if start_page == 0:
                start_page = 1
            is_url_exist = None
            for page in range(start_page, total_pages + 1):

                # create session
                session = _session()
                # if last page details exists update the page no
                if last_page_details_exist:
                    last_page_details_exist = session.query(
                        ThreadLastpage
                    ).filter_by(thread_uuid=thread_uuid).first()
                    last_page_details_exist.lastpage = page
                    last_page_details_exist.updated_at = datetime.now()
                    session.commit()

                else:
                    # if last page details not exists add new record
                    current_date = datetime.now()
                    last_page_details_exist = ThreadLastpage(thread_uuid=thread_uuid,
                                                             lastpage=page,
                                                             updated_at=current_date)
                    session.add(last_page_details_exist)
                    session.commit()

                try:
                    session.close()
                except Exception as e:
                    logging.exception(" exception closing session %s " % e)
                # Form a Thred URL
                temp = page
                if yaml_obj.get(forum).get('Meta').get('Post').get('pagenav').get('posts_per_page'):
                    page = t_module.posts_records_per_page(page)
                # count related changed for url like http://www.hk-pub.com/forum/thread-1611360-2-7.html (threadId-postPageNumber-threadPageNumber)
                # previous it used for swehack it url pattern changed to count 2
                if str(meta_dic.get('Thread').get('page_url')).count('%s') == 3:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, page, t_page))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 2:
                    if temp != 1:
                        thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, page))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 1:
                    if temp != 1:
                        thread_url = t_url + (str(meta_dic.get('Thread').get('page_url')).lstrip('\\') % (page))
                else:
                    if temp != 1:
                        page_splitUrl = meta_dic.get('Thread').get('page_url')
                        splitpageArgs = page_splitUrl.split('rem@_!@')
                        # print "   t_url in rem@  " ,  t_url
                        for argm in range(len(splitpageArgs) - 1, len(splitpageArgs)):
                            splittedThreadUrl = t_url.split(splitpageArgs[len(splitpageArgs) - 1])

                        thread_url = None
                        thread_url = str(splittedThreadUrl[0]) + str(splitpageArgs[1]) + str(page) + splitpageArgs[2]
                if yaml_obj.get(forum).get('code_replace'):
                    if '/p1' in thread_url:
                        thread_url = thread_url.replace('/p1/', '/')
                    if '#latest' in thread_url:
                        thread_url = thread_url.replace('#latest', '/p1')
                    if 'goto=newpost&' in thread_url:
                        thread_url = thread_url.replace('goto=newpost&', '')
                logging.debug("thread_url %s " % thread_url);
                soup = t_module.get_parse_content(thread_url)
                # print " soup " , soup
                if not soup:
                    failed_post_list.append(thread_url)
                    continue
                if yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('removewords'):
                    list_words = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('removewords')
                    soup = t_module.remove_words(soup, list_words)

                rows = t_module.get_post_rows(soup)
                logging.info(" post_rows length %s  " % len(rows))
                count = 0

                rowcount = len(rows)
                if yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmerge'):
                    merge_dict = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmerge')
                    rowseleminate = int(str(merge_dict.get('count')).split(',')[0])
                    rowcount = (len(rows) - rowseleminate) / int(str(merge_dict.get('count')).split(',')[1])
                for num in range(rowcount):
                    # print " num in for loop " ,num
                    if yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmerge'):
                        merge_dict = yaml_obj.get(forum).get('Meta').get('Post').get('soup').get('postmerge')
                        mergeCount = int(str(merge_dict.get('count')).split(',')[1])
                        rowseleminate = int(str(merge_dict.get('count')).split(',')[0])
                        temp = ""
                        for i in range(mergeCount):
                            temp = temp + str(rows[(num * mergeCount) + (rowseleminate) + i])
                            # print "row values ==  " , (num*mergeCount)+(rowseleminate)+i
                        row = BeautifulSoup(temp, 'html.parser')
                    else:
                        row = rows[num]
                    post_info = t_module.get_post_info(row)
                    # print " post_info  ",   post_info
                    if post_info:
                        post_date = post_info['post_date']
                        post_body = post_info['post_body']
                        member_name = post_info['member_name']
                        post_id = post_info['post_id']
                        post_bodyUrls = post_info['post_urls']

                        if post_body != '' and post_id != None and member_name != '':
                            session = _session()

                            is_post_details_exist = session.query(
                                Post
                            ).filter_by(third_party_id=post_id,
                                        thread_uuid=thread_uuid).first()
                            if yaml_obj.get(forum).get('Replace_url') and check_text == 'Duplicate':
                                print "in replace_url   "
                                if is_post_details_exist:
                                    if is_post_details_exist.member_name == member_name:
                                        print "in replace_url   ", is_post_details_exist.member_name
                                        is_url_exist = session.query(Topic).filter_by(uuid=thread_uuid).first()
                                        is_url_exist.url = t_url
                                        try:
                                            session.commit()
                                        except IntegrityError:
                                            session.rollback()
                                            continue
                                        break
                                else:
                                    continue
                            postId = 0
                            skip_reply = True
                            if yaml_obj.get(forum).get('Replay'):
                                reply_obj = yaml_obj.get(forum).get('Replay')
                                if reply_obj.get('required'):
                                    reply_obj = yaml_obj.get(forum).get('Replay')
                                    for key_word in reply_obj.get('keyword'):
                                        print "check ", str(post_body).find(key_word) >= 0
                                        if str(post_body).find(key_word) >= 0:
                                            skip_reply = False
                                            break
                                        else:
                                            skip_reply = True
                            if not skip_reply:
                                reply_msgs = reply_obj.get('reply_messages')
                                choice_reply_msg = choice(reply_msgs)
                                reply_post_body = t_module.give_reply(choice_reply_msg, row, thread_url, num)
                                # print " reply_post_body ", reply_post_body
                                if reply_post_body:
                                    post_body = reply_post_body
                            # logging.debug(" is_post_details_exist %s " % is_post_details_exist)
                            print " is_post_details_exist %s ", is_post_details_exist
                            if not is_post_details_exist and check_text == 'NoDuplicate':
                                post_uuid = str(uuid.uuid4())
                                logging.info('******** Member Name: \t  %s ' % str(member_name))
                                print " ******** Member Name: \t  %s ", str(member_name)
                                # logging.info('******** Post Body: \t %s '  % str(post_body))
                                print " ******** Post Body: \t ", str(post_body)
                                logging.info('******** Posted Date\t %s ' % str(post_date))
                                print " ******** Posted Date\t ", str(post_date)

                                timezone = yaml_obj.get(forum).get('time_zone')
                                # Add data to database

                                post = Post(uuid=post_uuid, thread_uuid=thread_uuid,
                                            third_party_id=post_id,
                                            member_name=member_name, body=post_body, type='post', parent_uuid=None,
                                            created_at=post_date, timezone=timezone, sequence_number=sequence_num)
                                # post_list.append(post)
                                session.add(post)
                                session.flush()
                                postId = post.pid
                                try:
                                    session.commit()
                                except IntegrityError:
                                    session.rollback()
                                    continue
                                if not yaml_obj.get(forum).get('Meta').get('Thread').get('find').get('date'):
                                    # Check for exisiting date in the DB.
                                    # If date today or None is present then update it to DB.
                                    is_thread_details_exist = session.query(
                                        Topic
                                    ).filter_by(url=t_url).first()

                                    if is_thread_details_exist:
                                        db = MySQLdb.connect(initializeYaml_obj.get('HOST'),
                                                             initializeYaml_obj.get('DB_USERNAME'),
                                                             initializeYaml_obj.get('DB_PASSWORD'))
                                        # prepare a cursor object using cursor() method
                                        cursor1 = db.cursor()
                                        cursor1.execute("use " + initializeYaml_obj.get('DB_NAME'))

                                        cursor1.execute("select min(created_at) from posts where thread_uuid= '%s'" % (
                                            is_thread_details_exist.uuid))
                                        min_postDate = cursor1.fetchone()
                                        if min_postDate:
                                            postDate = min_postDate[0]
                                            postDate = str(postDate)
                                        db.close()
                                        count = 1

                                        if postDate < str(is_thread_details_exist.created_at):
                                            is_thread_details_exist.created_at = postDate
                                try:
                                    #storeUrls(post_bodyUrls, postId, post_uuid, thread_uuid)
                                    pass
                                except Exception as e:
                                    print " Exception in store Urls ", e
                                sequence_num = sequence_num + 1
                            else:
                                post_uuid = is_post_details_exist.uuid
                                body = is_post_details_exist.body
                                if body == '':
                                    is_post_details_exist.body = post_body

                            session.close()
                            if yaml_obj.get(forum).get('Meta').get('Comment'):
                                parse_comments(t_url, t_id, f_id, thread_uuid, t_page, post_uuid, row)
                                # storeUrls(post_bodyUrls,postId)
                        else:
                            pass
                    else:
                        # print " post_info  " , post_info
                        continue
                if is_url_exist != None and yaml_obj.get(forum).get('Replace_url'):
                    break
        else:
            failed_post_list.append(thread_url)
            logging.debug("*** Thread Page Not Found ** %s " % thread_url)
    except Exception as e:
        logging.exception('************** Thread url exception :\t %s ' % str(thread_url))
        failed_post_list.append(thread_url)
        logging.exception(' %s ' % traceback.print_exception(*sys.exc_info()))


def parse_comments(t_url, t_id, f_id, thread_uuid, t_page, post_uuid, postrow):
    """ List all posts by thread url and
        store post information
    """
    try:
        thread_url = t_url
        soup = t_module.get_parse_content(t_url)
        meta_dic = yaml_obj.get(forum).get('Meta')
        if yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('removewords'):
            list_words = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('removewords')
            soup = t_module.remove_words(soup, list_words)
        if soup:
            # Get all thread list pages by pagination
            comment_dict = meta_dic.get('Comment')
            total_pages = t_module.get_post_total_page_count(soup, t_url, comment_dict)
            logging.debug(" comment_pages @@@@  :::   %s " % total_pages)
            session = _session()

            # calculate start page of thread
            start_page = 1

            for page in range(1, total_pages + 1):

                # Form a Thred URL
                temp = page

                if yaml_obj.get(forum).get('Meta').get('Comment').get('pagenav').get('posts_per_page'):
                    page = t_module.posts_records_per_page(page)
                if str(meta_dic.get('Thread').get('page_url')).count('%s') == 3:
                    thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, page, t_page))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 2:
                    if temp != 1:
                        thread_url = baseurl + (str(meta_dic.get('Thread').get('page_url')) % (t_id, page))
                elif str(meta_dic.get('Thread').get('page_url')).count('%s') == 1:
                    if temp != 1:
                        thread_url = t_url + (str(meta_dic.get('Thread').get('page_url')).lstrip('\\') % (page))
                else:
                    if temp != 1:
                        page_splitUrl = meta_dic.get('Thread').get('page_url')
                        splitpageArgs = page_splitUrl.split('rem@_!@')
                        for argm in range(len(splitpageArgs) - 1, len(splitpageArgs)):
                            splittedThreadUrl = t_url.split(splitpageArgs[len(splitpageArgs) - 1])

                        thread_url = None
                        thread_url = str(splittedThreadUrl[0]) + str(splitpageArgs[1]) + str(page) + splitpageArgs[2]
                if yaml_obj.get(forum).get('code_replace'):
                    if '#latest' in thread_url:
                        thread_url = thread_url.replace('#latest', '/p1')
                    if '/p1/' in thread_url:
                        thread_url = thread_url.replace('/p1/', '/')
                logging.info(" COmment url %s " % thread_url)
                soup = t_module.get_parse_content(thread_url)
                if not soup:
                    failed_post_list.append(thread_url)
                    continue
                if yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('removewords'):
                    list_words = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('removewords')
                    soup = t_module.remove_words(soup, list_words)

                if not yaml_obj.get(forum).get('souprequired'):
                    rows = t_module.get_comment_rows(soup)
                else:
                    rows = t_module.get_comment_rows(postrow)

                count = 0

                rowcount = len(rows)
                if yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmerge'):
                    merge_dict = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmerge')
                    rowseleminate = int(str(merge_dict.get('count')).split(',')[0])
                    rowcount = (len(rows) - rowseleminate) / int(str(merge_dict.get('count')).split(',')[1])
                getCommentMax_Sequence = session.query(
                    func.max(Post.sequence_number)
                ).filter_by(parent_uuid=post_uuid, type='comment').first()
                sequence_num = 0
                if getCommentMax_Sequence[0] is None:
                    sequence_num = 0
                else:
                    sequence_num = getCommentMax_Sequence[0] + 1
                for num in range(rowcount):
                    # print " num in for loop " ,num
                    if yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmerge'):
                        merge_dict = yaml_obj.get(forum).get('Meta').get('Comment').get('soup').get('postmerge')
                        mergeCount = int(str(merge_dict.get('count')).split(',')[1])
                        rowseleminate = int(str(merge_dict.get('count')).split(',')[0])
                        temp = ""
                        for i in range(mergeCount):
                            temp = temp + str(rows[(num * mergeCount) + (rowseleminate) + i])
                        row = BeautifulSoup(temp, 'html.parser')
                    else:
                        row = rows[num]
                    comment_info = t_module.get_comment_info(row)
                    if comment_info:
                        comment_date = comment_info['comment_date']
                        comment_body = comment_info['comment_body']

                        member_name = comment_info['member_name']

                        comment_id = comment_info['comment_id']
                        comment_bodyUrls = comment_info['comment_urls']
                        timezone = yaml_obj[forum]['time_zone']

                        if comment_body != '' and comment_id != None and member_name != '':

                            is_Comment_details_exist = session.query(
                                Post
                            ).filter_by(third_party_id=comment_id,
                                        thread_uuid=thread_uuid, parent_uuid=post_uuid).first()

                            logging.debug(" is_Comment_details_exist %s " % is_Comment_details_exist)
                            if not is_Comment_details_exist:
                                comment_uuid = str(uuid.uuid4())
                                # logging.info('******** Thread UUID: \t %s ' % str(thread_uuid))
                                logging.info('******** comment member Name: \t   %s ' % str(member_name))
                                # logging.info('******** comment_uuid : \t  %s ' % str(comment_uuid))
                                logging.info('******** Post Body: \t  %s ' % str(comment_body))
                                logging.info('******** commented Date\t  %s ' % str(comment_date))

                                # Add data to database
                                comment = Post(uuid=comment_uuid, thread_uuid=thread_uuid,
                                               third_party_id=comment_id,
                                               member_name=member_name,
                                               body=comment_body, type='comment', parent_uuid=post_uuid,
                                               created_at=comment_date, timezone=timezone, sequence_number=sequence_num)

                                # post_list.append(post)
                                try:
                                    session.add(comment)
                                    session.flush()
                                except IntegrityError as e:
                                    print "in comments exception"
                                    if yaml_obj.get(forum).get('updatecomments'):
                                        session = _session()
                                        is_Comment_details_exist1 = session.query(
                                            Post
                                        ).filter_by(third_party_id=comment_id,
                                                    thread_uuid=thread_uuid).first()
                                        is_Comment_details_exist1.type = 'comment'
                                        is_Comment_details_exist1.parent_uuid = post_uuid
                                        session.commit()
                                        session.close()
                                except Exception as e2:
                                    print "Exception as  ", e2

                                try:
                                    session.commit()
                                except IntegrityError:
                                    session.rollback()
                                    session.close()
                                    continue
                                commentId = comment.pid
                                try:
                                    storeUrls(comment_bodyUrls, commentId, comment_uuid, thread_uuid)
                                except Exception as e:
                                    print " Exception during storeUrl comment section ", e
                                sequence_num = sequence_num + 1
                            else:
                                is_Comment_details_exist.third_party_id = comment_id

                            session.close()
                        else:
                            pass
                    else:
                        continue
        else:
            failed_post_list.append(thread_url)
            logging.error("**** Thread url not Found *****  %s " % thread_url)
    except Exception as e:
        logging.exception('************** Thread url exception :\t  %s ' % str(thread_url))
        failed_post_list.append(thread_url)
        logging.exception('  %s ' % traceback.print_exception(*sys.exc_info()))


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


def storeUrls(post_body1, postId, post_uuid, thread_uuid):
    forum_name = yaml_obj[forum]['PROJECT']
    if post_body1:
        doc_urls = post_body1.find_all('a')
        # print " doc_urls "  , doc_urls
        for doc_url in doc_urls:
            doc_url = doc_url.get('href')
            isValid = re.search(
                r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
                doc_url)
            if not isValid:
                doc_url = baseurl + doc_url

            numOfSep = doc_url.count("?", 0, len(doc_url))
            isValidUrl = doc_url.split("?", 1)
            if numOfSep >= 1:
                isValidUrl1 = re.search(
                    r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
                    isValidUrl[1])
                if isValidUrl1:
                    doc_url = isValidUrl[1]
            fileName = None
            # print " doc_url after done " , doc_url
            if re.search(r'' + baseurl + '', doc_url):
                pass
            else:
                def getFileName(url, openUrl):
                    try:
                        if 'Content-Disposition' in openUrl.info():
                            # If the response has Content-Disposition, try to get filename from it
                            cd = dict(map(
                                lambda x: x.strip().split('=') if '=' in x else (x.strip(), ''),
                                openUrl.info()['Content-Disposition'].split(';')))
                            if 'filename' in cd:
                                filename = cd['filename'].strip("\"'")
                            if filename: return filename
                        # if no filename was found above, parse it out of the final URL.
                        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])
                    except Exception as e:
                        pass

                r = None
                session = None
                try:
                    _session = sessionmaker()
                    _session.configure(bind=engine)

                    # create session
                    session = _session()

                    is_Url_details_exist = session.query(
                        Binaries
                    ).filter_by(post_id=postId,
                                url=doc_url).first()
                    status = 'success'

                    if not is_Url_details_exist:
                        # binaries_list = list()
                        hdr = {
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko)                                    Chrome/23.0.1271.64 Safari/537.11',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive'}
                        g = urllib2.Request(doc_url, headers=hdr)

                        f2 = None
                        matchedOrNot = True

                        try:
                            f2 = urllib2.urlopen(g)
                            contentType = f2.info().getheaders("Content-Type")[0]
                            matchedOrNot = re.search("html", contentType)
                        except urllib2.HTTPError, e:
                            status = 'failure  Due to %s ' % (str(e))
                        except urllib2.URLError, e:
                            status = 'failure  Due to %s ' % (str(e))
                        except Exception as e:
                            print " excecption termination download content ", e
                            status = 'failure  Due to %s ' % (str(e))
                        finally:
                            pass

                        try:
                            if f2:
                                r = f2
                            else:
                                r = urllib2.urlopen(g)
                        except Exception as e:
                            status = 'failure  Due to %s ' % (str(e))

                        fileName = fileName or getFileName(doc_url, r)
                        # print " fileName   " ,fileName
                        if not fileName:
                            fileNameget = str(doc_url).rsplit('/')
                            if len(fileNameget) < 2:
                                fileName = str(fileNameget[0])
                            else:
                                if fileNameget[len(fileNameget) - 1]:
                                    if not matchedOrNot:
                                        fileName = str(fileNameget[len(fileNameget) - 1]) + '.txt'
                                    else:
                                        fileName = str(fileNameget[len(fileNameget) - 1]) + '.html'
                                else:
                                    if not matchedOrNot:
                                        fileName = str(fileNameget[len(fileNameget) - 2]) + '.txt'
                                    else:
                                        fileName = str(fileNameget[len(fileNameget) - 2]) + '.html'

                        splitfileName = str(fileName).rsplit('.', 1)
                        timestamp = str(time.time()).split('.')[0]
                        if splitfileName:
                            if splitfileName[1]:
                                if str(splitfileName[1]) != 'com':
                                    fileName = str(forum_name) + "_" + str(thread_uuid) + "_" + str(
                                        splitfileName[0]) + timestamp + '.' + splitfileName[1]
                                else:
                                    fileName = str(forum_name) + "_" + str(thread_uuid) + "_" + tr(
                                        splitfileName[0]) + timestamp + '.txt'
                            else:
                                fileName = str(forum_name) + "_" + str(thread_uuid) + "_" + str(
                                    splitfileName[0]) + timestamp + '.txt'

                        fullpath = '/data/Archives/all'
                        if not os.path.exists(fullpath):
                            # os.mkdir(fullpath)
                            subFolder = fullpath.strip().split('/')
                            count = 0
                            subPath = ''
                            for i in range(0, len(subFolder)):
                                if subFolder[i] != "":
                                    subfolderpath = str(subFolder[i])
                                    subPath = (subPath + '/' + subfolderpath).strip()
                                    if os.path.exists(subPath):
                                        pass
                                    else:
                                        try:
                                            os.mkdir(subPath)
                                        except Exception as e:
                                            logging.error("error while creating folder ")

                        fullpath = os.path.join(fullpath, fileName)
                        filesize = 0
                        if status == 'success':
                            with open(fullpath, 'w') as f:
                                # shutil.copyfile(r,f)
                                if r:
                                    f.write(r.read())
                                    status = 'success'
                                else:
                                    status = 'failure'

                            filesize = os.path.getsize(fullpath)
                            if int(filesize) == 0:
                                status = 'failure'
                                try:
                                    os.remove(fullpath)
                                except Exception as e:
                                    print e

                            if status == 'failure':
                                try:
                                    os.remove(fullpath)
                                except Exception as e:
                                    print e
                        else:
                            status = 'failure'
                        if status == 'failure':
                            filesize = 0
                        binaryUUid = str(uuid.uuid4())
                        binaries = Binaries(binary_uuId=binaryUUid, post_id=postId, url=doc_url,
                                            fileName=fileName,
                                            status=status, createdDate=datetime.utcnow(), post_uuid=post_uuid,
                                            file_size=filesize)
                        # binaries_list.append(binaries)
                        session.add(binaries)
                        session.flush()
                        session.commit()
                        session.close()
                        logging.info(" binary saved successfully  %s " % fileName)
                    else:
                        session.close()
                except urllib2.HTTPError, e:
                    if session:
                        session.close()
                    logging.exception(" error  %s " % e.code)
                except urllib2.URLError, e:
                    if session:
                        session.close()
                    logging.exception("error %s " % e.args)
                except Exception as e:
                    if session:
                        session.close()
                    logging.exception(" exception in store url %s " % e)
                finally:
                    if r:
                        r.close()


def dowork(q):
    while True:
        try:
            url = q.get()
            logging.info('******************* current url:\t %s ' % url)
            parse_thread(url)
            q.task_done()
        except Exception as e:
            logging.info('******************* ERROR Dowork ************')
            logging.info('****  ERROR Dowork  **** url: %s ' % url)
            logging.info('**** Exception:\t %s ' % str(traceback.print_exception(*sys.exc_info())))
            q.task_done()


if __name__ == '__main__':

    try:
        starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logging.info('******** start time:\t  %s ' % starttime)
        # If required then, User Authentication
        if yaml_obj.get(forum).get('Click_require'):
            auth_status_code = t_module.clickbutton(loginUrl)
            # Check for user authentication success.
            if not auth_status_code == 200:
                logging.error('***** login failure !****** ')
                sys.exit()
            else:
                logging.info('form submitted')

        if yaml_obj.get(forum).get('Login').get('required'):
            if not yaml_obj.get(forum).get('Captcha').get('required'):
                # Simple Login without captcha
                auth_status_code = t_module.user_authentication(loginUrl)
            if yaml_obj.get(forum).get('Captcha').get('required'):
                if not yaml_obj.get(forum).get('Captcha').get('type'):
                    # Simple Login with simple captcha
                    auth_status_code = t_module.user_authentication(loginUrl)
                if yaml_obj.get(forum).get('Captcha').get('type'):
                    captcha_type = yaml_obj.get(forum).get('Captcha').get('type')
                    captcha_type = int(raw_input('Enter Captcha Type as a number 1 or 2 or 3'))
                    if (captcha_type == 1):
                        # Login with captcha other than simple captcha
                        auth_status_code = t_module.user_captcha_authentication(loginUrl)
                    elif (captcha_type == 2):
                        # Only captcha other than Login like only reCaptcha
                        auth_status_code = t_module.user_captcha_authentication(loginUrl)
                    elif (captcha_type == 3):
                        # Only captcha other than Login like only reCaptcha
                        auth_status_code = t_module.user_captcha_mechanize(loginUrl)
                    else:
                        print ("Please Provide valid input for Captcha - > type : 1 or 2 or 3")
            if not auth_status_code == 200:
                logging.error('***** login failure !****** ')
                sys.exit()
            else:
                print 'Authentication Success.'
                logging.info('************** Sucessfully Login! ******** ')
        elif not yaml_obj.get(forum).get('Login').get('required') and yaml_obj.get(forum).get('Captcha').get(
                'required'):
            if yaml_obj.get(forum).get('Captcha').get('type'):
                captcha_type = yaml_obj.get(forum).get('Captcha').get('type')
                captcha_type = int(raw_input('Enter Captcha Type as a number 1 or 2 or 3'))
                if (captcha_type == 2):
                    auth_status_code = t_module.user_captcha_authentication(loginUrl)
                elif (captcha_type == 3):
                    auth_status_code = t_module.user_captcha_mechanize(loginUrl)
                else:
                    logging.error("Please Provide valid input for Captcha - > type : 1 or 2 or 3")
                if not auth_status_code == 200:
                    logging.error('***** login failure !****** ')
                    sys.exit()
                else:
                    logging.info('************** Sucessfully Login! ******** ')
            else:
                auth_status_code = t_module.user_authentication(loginUrl)
                if not auth_status_code == 200:
                    logging.error('Authentication Failed.')
                    sys.exit()
                else:
                    logging.info('Authentication Success.')
        logging.info("Initializing Threads")
        for i in range(1, yaml_obj[forum]['NUM_THREADS']):
            worker = Thread(target=dowork, args=(q,))
            worker.setDaemon(True)
            # print " threading.active_count() " , threading.active_count()
            worker.start()

        # Start scraping the forum
        print "Start Forum Scraping:\t "
        logging.info("Start Forum Scraping")
        if not args.debug:
            parse_forum()

        q.join()
        time.sleep(1)
        logging.info('************** Sucessfully completed! ******** ')

        endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Failed Threads")
        logging.info(failed_thread_list)

        logging.info("Failed Posts:")
        logging.info(failed_post_list)
        print "******** end time:\t ", endtime
        logging.info('******** end time:\t %s' % endtime)
        sys.exit()
    except KeyboardInterrupt:
        # quit
        logging.info("Failed Threads")
        logging.info(failed_thread_list)
        print "-----------------------------------------------------------"
        logging.info("Failed Posts")
        logging.info(failed_post_list)
        sys.exit()
