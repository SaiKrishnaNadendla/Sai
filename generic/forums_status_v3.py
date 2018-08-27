#!/usr/bin/python
# -*- coding: utf-8 -*-

#Same solution By selenium + PhanthomJS
import sys , time 
import urlparse
import io, json
import csv

#For reCaptcha using selenium required below modules, and also time, BeautifulSoup required which are imported above
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#old list of forums
arrlen = ["http://33cb5x4tdiab2jhe.onion/","http://jg7mqus5l6mc6ghk.onion/","http://bcelks5fdtdrnhmh.onion/","http://privatelwioxytnr.onion/","http://t7ajl4lcv6hx4spidtgbcr3zjvq2djusu5otjm7cqzo3flkjtsm44xqd.onion/","http://qmqagfw4imrtiutf.onion/","http://nguvjgdxce6j4cac.onion/","http://m4gs4ali4kub7wlo.onion/","http://6g2ugu6vnx5ioizo.onion/","http://2kyxttcrp3kgh3nt.onion/","http://dhdlxpqdteodjhrh.onion/","http://spookulag6zjjt34.onion/","http://35hlwrgfbxotey5n.onion/","http://4nemfjztqypcyhb5.onion/","http://4qliagigorafq3wt.onion/","http://l4xes7ggkbgazffp.onion/","http://shopif7a6vgrb3pu.onion/","http://myre5ztjxe4n2dg4.onion/","http://vnp7agdlmsa4iqqv.onion/","http://yzpayb4sqad7gnin.onion/","http://gsqkg7pqjsvgn2jx.onion/","http://shops7twcwpa7p4e.onion/","http://apple7xy753qjdlf.onion/","http://hiddencv4di7vzsh.onion/","http://sandme4t4wqet3dq.onion/","http://wj335224jmriavnc.onion/","http://e2fsf6zcqnoz4mdb.onion/","http://z3pv3uohh6kdmerw.onion/","http://yztiisyv4ws5a4d2.onion/","http://rossarrztiivc2dl.onion/","http://hostingv5fypnk3u.onion/","http://tjeg5prbuqb6jkun.onion/","http://mibdrhy5oibvdrwf.onion/","http://didw2lzi3hdapqzs.onion/","http://67c3c3vgvuo6q2yn.onion/","http://7obciefokkjpr7ut.onion/","http://o43pds3l3kgowgt4.onion/","http://img4ukdtnqnalncq.onion/","http://eyesftstxxt5bgtr.onion/","http://zcew2gwdn44r267w.onion/","http://tun73ihf32kf75oi.onion/","http://iclxwfqv5fha7vf6.onion/","http://i2krij7vcjrejipt.onion/","http://i2cd7lskmfiv2p4c.onion/","http://hffp33b3xwznzhtp.onion/","http://f66mg7zmvh6dgcir.onion/","http://d62fkf72tv5xc6hk.onion/","http://bxtzulqh4jliu64n.onion/","http://5cdsbojbtmyggmqp.onion/","http://43jnwf6lzjhnl3gb.onion/","http://hydraruzsiqm6r5d.onion/","http://nwnwnnv7gmyt25ir.onion/","http://hydraruhi2xnt6tl.onion/","http://2panjkxemgz7aekg.onion/","http://m4zirhgimv6y6tf7.onion/","http://opwm25obnrnfnh5j.onion/","http://nicevps66zvn6a47.onion/","http://k5x5spivrjvk4idw.onion/","http://wishing4kvnaki5j.onion/","http://dmojsiteox2gl6n5sj6aslbchjma3gyvon2rdawb625p4f2dd434i6ad.onion/","http://4chdqx4cgsje7cj4qlqqyvumvlyi2yjpiesd44fiecozclwwgce6lyid.onion/","http://artgalernkq6orab.onion/","http://wwwgpe4ohqdkpwa7ft7ktvl7dw2bnf5tdgszlovu5hrmlwdoqstmvqqd.onion/","http://zgfaymz2wjbciztn.onion/","http://ypjtamcod4efw2au.onion/","http://ynmxi5wlsavwpa3y.onion/","http://x36pibytckjmrivh.onion/","http://u44ozr6oyr7shybn.onion/","http://tvrjl72j2wkam6io.onion/","http://tl7cblw73y6bs7ql.onion/","http://qg7nrroshajbecqa.onion/","http://qd3q5qfonlxibnst.onion/","http://p5ajcmpajaxpnrfe.onion/","http://nvi5naaahmott4yn.onion/","http://lr3saufy4goec2z4.onion/","http://hzx5fxdapzacw762.onion/","http://hn2jmd5a2c2xn2lt.onion/","http://g5otux6f62zin3b6.onion/","http://baf43dmyzbqqwn5j.onion/","http://axkyotvi42avixg3.onion/","http://7bvg75nnm3lal2ml.onion/","http://6hjq3lp3npvd3umy.onion/","http://4fx4vi6tc7iuue4s.onion/","http://rerg66fejfl74mae.onion/","http://3nymbygktyh6u7ea.onion/","http://2vy4vmreonlglcu5.onion/","http://2llkbhj457xc2jh3.onion/","http://fnpqrgim4bsjlfhs.onion/","http://5pagpaecjtzxtskf.onion/","http://yc7iqi2z5fyfi2nq.onion/","http://zvepknm42kzuslzy.onion/","http://gooo6hmmszkqskpy.onion/","http://hmy6457iplcgkyy2.onion/","http://dzhsn35mztp77nta.onion/","http://iloveyou776dskgx.onion/","http://uniccxide6hker6y.onion/","http://22tj73hejnqj2fgy.onion/","http://cgrevelhatbns37m.onion/","http://pjzzfamhsufmi4hm.onion/","http://5bnetansmofuahvs.onion/","http://magnetxticiuv5sy.onion/","http://twowjlkcz2xz3h7f.onion/","http://trywifewearw3haz.onion/","http://familyrez3e5nxwg.onion/","http://rbo7jz3k2faixbw3.onion/","http://daddybuuwcvt3rfk.onion/","http://fkdogsdysjb6u5dx.onion/","http://o2hjflbnhafltbbz.onion/","http://hydraru5mmjmx4fr.onion/","http://ycngzafvhbrxl5w3.onion/","http://666666677563g5vi.onion/","http://mmnr2x4aczms4v2j.onion/","http://wmxyocodhiurcroc.onion/","http://yhdnp372d7du7sul.onion/","http://notndu3rgltj5vbk.onion/","http://r5ucrt2awdv3foy7.onion/","http://prophecyeazdqp7g.onion/","http://hoppcnv3c6vf5er6.onion/","http://3qiawf6j2uhppauy.onion/","http://5knpli2f5lx4qfwb.onion/","http://xqvpszlueifaecry.onion/","http://vfdqieiodz7mwqnx.onion/","http://mn5dbabfmjep5gxe.onion/","http://mnaqelu35wrg6wkk.onion/","http://kuceepzqkzzbmmos.onion/","http://g2polr4buwlfgvns.onion/","http://dgip6wpbp32oxdqn.onion/","http://calhezfbh4srlbta.onion/","http://7gygrgfyswpecr3k.onion/","http://kvttxuubqk7yw2qn.onion/","http://itsip4b6igv662ve.onion/","http://jponu5gaiaoetj3k.onion/","http://fyj4gpr5qnojd2w5.onion/","http://d4eivhlr4zh7xigb.onion/","http://5mwcrvkp74hnqehy.onion/","http://32bjrfdqsz4uw2za.onion/","http://4xvozgvyzenn52wj.onion/","http://w7fmbuewputvyvrq.onion/","http://pakistan2mkivh5q.onion/","http://kse6hnb546prpjnb.onion/","http://wry34wgtocrzu2ma.onion/","http://zk5r53pvuvosrocc.onion/","http://yz4goypemxz37ia2.onion/","http://wqfdtr6ccdm7s2nv.onion/","http://wjq3fusv3pto3znd.onion/","http://wi5z2auerocwd4pv.onion/","http://uszaoyogxq2uqls3.onion/","http://u4hpxmok35zqsu77.onion/","http://ureol73reiewrpp6.onion/","http://scjuvpx6hvvb67za.onion/","http://dtz7vbtvesne4kbk.onion/","http://sgeup5xpkldzkdx4.onion/","http://sb6zmtwdyog7voom.onion/","http://redglgzyg74pxuqx.onion/","http://qwszvdgt2sqnmd2g.onion/","http://lavowdil4gzqa7fz.onion/","http://xgsvwzunchadxb66.onion/","http://freerqtfxhahy5cs.onion/","http://nreboh7ukv3ngodb.onion/","http://xd777yn5scfrdius.onion/","http://pk34kwndmipvsxeo.onion/","http://freera5bf6sfpojr.onion/","http://nts2w3gq3uxssz3w.onion/","http://n2pm5rhjtu2xkteq.onion/","http://ty2sxzmjrkxojl6b.onion/","http://vbh6n34enayqunpd.onion/","http://mssynykz2naapjip.onion/","http://tsyjkuxv3a7ct5s6.onion/","http://renugg46beaj67qx.onion/","http://lkfp2waqj22ibftv.onion/","http://lyfywzf3pewzclvv.onion/","http://pqnlanf4u2hjhyqt.onion/","http://l5uav3xp5tstpuey.onion/","http://lukkhwvupwhtji5q.onion/","http://kl6jhuqlfuzoekz7.onion/","http://nro2l2xg3a6i5ywg.onion/","http://lundchnuvy4zht5d.onion/","http://lcwi5apssa3ofa6h.onion/","http://l6esukwglcadi25c.onion/","http://jv37kogvfqsqbwsh.onion/","http://jpzcbnwwki36xc2o.onion/","http://jww4s35zpvpu2odp.onion/","http://iyvrecv7cjsfi7dw.onion/","http://jfpi3wk3amr2kn4o.onion/","http://hto5lxs4ifx7cwc7.onion/","http://iubiklqrufidrelr.onion/","http://iltksspye23e4es3.onion/","http://grq3cx5cmtbg25h7.onion/","http://gifkcdg4bs6oesaj.onion/","http://ghsvbtaefaegyu5k.onion/","http://eyfgi52e25pho2w4.onion/","http://fb66bfwflfnd4q4y.onion/","http://evjz4r6itzvwqfcu.onion/","http://cp4y3bwixd5zrfqh.onion/","http://fik6rmgijtj6ieo3.onion/","http://dao6vzpyskqmgjue.onion/","http://clp5mbywxox4eoyf.onion/","http://7ycmrebb4r5xpfbb.onion/","http://ecqru7e4nb5ba2l4.onion/","http://acjzpqkmmcnk5sbn.onion/"]




with open('forums_status1000.csv', 'a') as csvfile:
	fieldnames = ['website', 'status', 'Description']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0, len(arrlen)):
		# r = requests.get(forums[i])
		# r.status_code
		print "forum : %s :" % i
		url = arrlen[i]
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0")
		# driver = webdriver.PhantomJS(desired_capabilities=dcap)
		# PhantomJS Driver
		service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any', '--proxy=127.0.0.1:9050', '--proxy-type=socks5']
		driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs', service_args=service_args,
								 desired_capabilities=dcap)

		# driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--proxy=127.0.0.1:9050', '--proxy-type=socks5'])
		driver.get(url)
		print "Website ::", url
		print(driver.title)
		writer.writerow({'website': url, 'status': driver.title, 'Description': 'Freshonions'})
		csvfile.flush()
		print "File completed successfully.."
