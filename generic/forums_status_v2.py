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
arrlen = ["http://4zdccri7kz3zccrq.onion/","http://scangzh2q6l5utug.onion/","http://ncrb7blc4h76y4ou.onion/","http://hydrarezgnjfjrj2.onion/","http://fudmle2so7kt3tot.onion/","http://hell66nsdnoyx4bp.onion/","http://f5izbq2cidyxpo2j.onion/","http://aaaaaaaaaz6fohug.onion/","http://hosting5afrku32b.onion/","http://u7776qapmdeq3mbv.onion/","http://rl3t6qvcfivnm72x.onion/","http://eahfd4bjvgklinmt.onion/","http://b3urzn2a357x3pxi.onion/","http://7v6yjcmqem3jkjj2.onion/","http://jyvsrlhz45ndk4c6.onion/","http://mcretrorigsr7qag.onion/","http://2222222237z3q52l.onion/","http://boysland3nu6yyfq.onion/","http://3iavobfo47g3e3c5.onion/","http://toxic24p5jmxv444.onion/","http://torbayqqzcsl4no4.onion/","http://uojdjo2gs3kfqwd3.onion/","http://j7otcfisd54colpt.onion/","http://2fm2ccx5uze3zf4e.onion/","http://bht5zpejflmylmkl.onion/","http://zjcnlsigactn47b6.onion/","http://wmhcklwisqtuoowm.onion/","http://sfey5ekvh3p7zzpt.onion/","http://oiyghrmyp5p32ojy.onion/","http://tfbzfjhoffbqkgab.onion/","http://st2hbbesxf7uyed5.onion/","http://7wxmeiw463xd62qt.onion/","http://idiazjakgk3464dg.onion/","http://762cbxrn5n3qar4o.onion/","http://jpciqleyvxi4hlvt.onion/","http://acidsongafqbf4fx.onion/","http://jszatt5kxc5nxanp.onion/","http://b4uca3c33nm5e2uf.onion/","http://53gar5zcr2hyx6p7.onion/","http://cashoutr2inecwwy.onion/","http://gd7qzoaeok3corel.onion/","http://cdmsxo25y4lfht6v.onion/","http://fatmanfigyfynoew.onion/","http://cards7ybzsemc3t5.onion/","http://ns42i6ozn7uca4qz.onion/","http://dyab7jnvnfqcuwi5.onion/","http://wdbuklx3pajcnycv.onion/","http://rheda7rv7imny7yx.onion/","http://hehehekcec23tx3h.onion/","http://6mukl7ucbhv2yt6j.onion/","http://paypaleyixgwoeah.onion/","http://appleu2d4ycqdhq7.onion/","http://wd3ncl7x53at6szi.onion/","http://xlchenvtmb7ukayn.onion/","http://zlczuwla2wwtkhkb.onion/","http://xbctxjlm74h4acwe.onion/","http://wepljgluiutwapng.onion/","http://uqoxxkrqa44ahgly.onion/","http://5sz32gbexmvk6fbq.onion/","http://jirxzjvo63m3wgag.onion/","http://q4j2z76vbd2g4i22.onion/","http://prh537ipml7cvtah.onion/","http://aol26rfn7t3u7pf7.onion/","http://fy7ns5yhbvfxag2v.onion/","http://7gf33qtzuvpensyc.onion/","http://p24dk77r44dx4kf2.onion/","http://eqp5maarf6fjazjk.onion/","http://udmkwqw3vwj2znkc.onion/","http://ny4ckehopzquoaz5.onion/","http://mzp6oxacvgb4kwpb.onion/","http://pwe4jzro3l4fukn3.onion/","http://k43h7eo7nmpbszr5.onion/","http://jks7krgdet75qmim.onion/","http://ayghfxnnncebdwpg.onion/","http://4zyrlxuptmyh2tlk.onion/","http://gl4f6r72ci4ns6io.onion/","http://752ahi7gvliuhsi6.onion/","http://6csgnhslrtytglzo.onion/","http://2qppqo7iuh4keppc.onion/","http://iwsopikut5x2br3e.onion/","http://hqrs2p4uw4w2oapk.onion/","http://haul2ettxiglicdr.onion/","http://berjbd2olaiwpkfl.onion/","http://7eqbgqdkd5ybbetn.onion/","http://5xdxtmgg7cxlkxfv.onion/","http://2il3dakk5ewnz3de.onion/","http://fjuhmfajfvljgbpy.onion/","http://6kuxy4tfxdkyy6bx.onion/","http://royal25fphqilqft.onion/","http://accd5u65abud2bbb.onion/","http://mi5tacminfdvfnw2.onion/","http://girland6zsrdgrbn.onion/","http://mmp26upm3gig2ltk.onion/","http://rottawebcbcjkh5s.onion/","http://looutq4ebmotaao6.onion/","http://2ecdkjslqivebfp4.onion/","http://wsemgtfrikclishl.onion/","http://xkhroo5va7bvmyi4.onion/","http://zvydqdmp3kqj6cwn.onion/","http://xnh4urytqnjbpukf.onion/","http://yakuzawaxmvkmnc2.onion/","http://222222222fum5vem.onion/","http://asbsqay2fojouaxm.onion/","http://4e6rtycjjqeeudas.onion/","http://valhallaln53si3x.onion/","http://endlxmzjfzj37qx3.onion/","http://cbsc5vcyfy7zdg52.onion/","http://nlazcjkowxnjayla.onion/","http://chatukps3edzzo2n.onion/","http://p2uz5eoa26t6cef2.onion/","http://vgul4bxge273mghx.onion/","http://s4de6xreohyd7gog.onion/","http://ikkprhi7x2w4227s.onion/","http://iy3vphybx3tvmksk.onion/","http://fzla2hqhxcmyymwn.onion/","http://tokyopubtaixjfyk.onion/","http://e65sqiliizsxp23y.onion/","http://syclzo2fqyqn6hqk.onion/","http://nixjnfit2h5tq6zf.onion/","http://fhsg464v5fdaf2kp.onion/","http://5jbtsr7433oen5na.onion/","http://3q54qd44vtkgi6rr.onion/","http://obccvpn2zdmnmhvs.onion/","http://dkcz4qgrniwbqfca.onion/","http://dazncuoh7x6kw3lk.onion/","http://broy5jrjr3l3k3yg.onion/","http://m4npd2shtgvwaitm.onion/","http://vq72let7ogq5goyq.onion/","http://nsxjcgosummdyggd.onion/","http://5kwzdcy422xp7x2c.onion/","http://wofrmttjuea6qh6p.onion/","http://c3obgrvijaie2ejk.onion/","http://svzasbwn4hpqadf4.onion/","http://horoiomuy6xignjv.onion/","http://vtw7g7wcdsgxq4ru.onion/","http://oqaotj3jp45hz3sx.onion/","http://gs4kdswsmea24jfp.onion/","http://ireadu2auvddwhbl.onion/","http://f7wj3r354mli6axc.onion/","http://h6ghab7v47k7yspr.onion/","http://wgt2gjizfsog3gzs.onion/","http://trvv5c2faemdiu7h.onion/","http://container656ovix.onion/","http://hyqysf24psmud4ze.onion/","http://ftvtltvigweu2gif.onion/","http://44ojftf27zhynbkk.onion/","http://u2bg5wgqh4oxcave.onion/","http://hgk4phrgzrouwjn2.onion/","http://dg7c4ams7iocjpou.onion/","http://kx2tb7sp6tf74net.onion/","http://6cczmzh4wz4butlk.onion/","http://s2f6erhtfkqbooiv.onion/","http://3rcy2blcszymx7p4.onion/","http://ivkkg7imhznqujww.onion/","http://egixtiuageimhrcx.onion/","http://jbiuhieblupagnn4.onion/","http://wac74kg3sg2ypdzo.onion/","http://bxwn6g4gquzq7bht.onion/","http://vncrvnt3dbdazap6.onion/","http://7a7d3toeuok3fcft.onion/","http://hen4rucxp7fglwqe.onion/","http://zhlcii6eyls464of.onion/","http://wmjvp4upsnwypbkg.onion/","http://fakeidwgnkceppik.onion/","http://money5dicv74pgbk.onion/","http://fhganczrcqpjbraf.onion/","http://hitmann5zga4jlr5.onion/","http://2mknnaldkmfw5xii.onion/","http://d6t5uemwgcwqoq6d.onion/","http://rq22thgljuly2h5u.onion/","http://4q5awrn3kgclmlb3.onion/","http://dgsqe373djyg6kql.onion/","http://paypalf7e5earid7.onion/","http://57nukq2wt6t66whd.onion/","http://khrbu7zr3asuf7tg.onion/","http://ukgirlsgxyi5sfxz.onion/","http://mvmq3nlnh4owauhb.onion/","http://acardsxfhifgho2e.onion/","http://plo7mjkhvxlej52u.onion/","http://4nvz5gcykpanjtty.onion/","http://7j6ypmoaah5ajrwm.onion/","http://onehost4w6jfd4ly.onion/","http://pkls2lcjulexhb5u.onion/","http://sbnh3p4ire65xxif.onion/","http://7an3d3t5zccb4dqt.onion/","http://larshilse3xpyawo.onion/","http://hydrab5kzlivvdfi.onion/","http://6vqczfghvillat4z.onion/","http://wx5ygniw7aptlx3a.onion/","http://l3bp3iyo3rafq7om.onion/","http://v7ionnk2fheyipot.onion/","http://qhkd2krq2gzfeh6i.onion/","http://y5ot2yonv6lhocv5.onion/","http://cg42oylqvvg45d3s.onion/","http://4jjuxwqoseu4o6bw.onion/","http://gf2bui2fvavrqyr7.onion/","http://ixmew2x7ybh7maeg.onion/","http://epxvebg4ixrsqjer.onion/","http://m56sg5xhl5wu52lk.onion/","http://boq62kieate6fms6.onion"]

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


