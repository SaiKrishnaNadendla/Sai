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
arrlen = ["http://7gk367csxlbh47mi.onion/","http://c2ww7ebsvjlcyzk6.onion/","http://747hqux32oe4wkgj.onion/","http://amdvwainsaqdblea.onion/","http://6zxgeffc6gafri3r.onion/","http://a6en2zi3yzczfqnt.onion/","http://6zoipq2vi7otdmel.onion/","http://6sp6rjw66nscagbh.onion/","http://67u2hmzbxkuddqa3.onion/","http://videonwcswhrqynk.onion/","http://y5gnrembtm772snc.onion/","http://dopefruqgev5v4ul.onion/","http://zyn6svtlcriym2en.onion/","http://hjiajblqc7retf4e.onion/","http://thexfilesp6dsazb.onion/","http://zp4dpmzp6pnswubf.onion/","http://xq7ahz3xkzilh3ta.onion/","http://coinbinap7rxddp5.onion/","http://3ta2mjxwxl2s6d7h.onion/","http://5g5paikyj7fx6bri.onion/","http://5q25e5iv25umwdvn.onion/","http://5yoxyogm4mvlt7z4.onion/","http://5mcjhk6ojjnwy5yq.onion/","http://5ipnh7ykx5kxo2km.onion/","http://2eq36v4c4nrqbs6g.onion/","http://2b5eyo6wvbpzuytr.onion/","http://weedclub3pnd2mhw.onion/","http://vb3n7f2vonqco4qd.onion/","http://tokyo2uikoquxthfrwg4vdqdi2hx2vb7ppanhup2a2ruffzjjtjpqiqd.onion/","http://hhk5qvdc6mwlfppn.onion/","http://arvx76r2knylc7jb.onion/","http://tt2mopgckifmberr.onion/","http://siodyrvlhfuus4cy.onion/","http://elfq2qefxx6dv3vy.onion/","http://wsv7lmjtxfuenm5y.onion/","http://sale24u3apkfx252.onion/","http://pnpotevstlmllayu.onion/","http://ahyp4oy3mbyqsbn3.onion/","http://73gh4j5aqqov2xw5.onion/","http://dzjxjco4uthvnt3q.onion/","http://iclzfuu2nkqg4xke.onion/","http://sbjzb2xy5g3z5tiy.onion:8080/","http://lu6oqe5e3bh7vsja.onion/","http://5hx2jppnk4vzr7cd.onion/","http://ydhre42a3olgwltx.onion/","http://leboncoinaskucig.onion/","http://saltoilt7w2gntdo.onion/","http://libert7thi6crlji.onion/","http://libertndtbmkbvue.onion/","http://k56fvg3kwldqyx3gv2zgumst7qimiql2fg55l7hhoshquhx5raeiibid.onion/","http://22222iortcdxrjo6.onion/","http://sbjzb2xy5g3z5tiy.onion/","http://myonionhyqwmuma2.onion/","http://dwiyomb6jwofxbuv.onion/","http://wumfl4whsotnswfu.onion/","http://o37hl6yryl56kh2m.onion/","http://kx4hdh2zo5rstcuj.onion/","http://rc2benpyetaatbdt.onion/","http://rev2qqywxzn67ept.onion/","http://vojg7abm5t2znijt.onion/","http://ssdvdivbjedefhsb.onion/","http://wstxnasfdrdzwk4j.onion/","http://vhhonvausdh7bulv.onion/","http://rnipxdrfzrwbgxsn.onion/","http://npv4yuth7ub6kmd4.onion/","http://jcfwttmyvzmvetku.onion/","http://kiaowvzq2pxvj4vu.onion/","http://hacc6iigdurka4fs.onion/","http://ivlz7rc6tuhsbtfa.onion/","http://d4cagqvqdzcpjyl4.onion/","http://ge5kdkg52a54zveg.onion/","http://5k6e5ajioc4sucq6.onion/","http://cjcvddgxuhmllfvs.onion/","http://4ike4qjvxn7ezd3l.onion/","http://3xeiol2bnhrsqhcsaifwtnlqkylrerdspzua7bcjrh26qlrrrctfobid.onion/","http://yi7mtn4t23ontrmi.onion/","http://tncttscdoxl7uqxq.onion/","http://thqh3v7jdcod4vd7.onion/","http://t3l2ufx3mpfylmoa.onion/","http://p7cgvteq2rfug54k.onion/","http://rm6cf7r5nhifbttt.onion/","http://vq7rvzbdrlogrfx6.onion/","http://nspp5brskwibbjcf.onion/","http://o2nulztggwmome5n.onion/","http://oe2boeuto27ojaqo.onion/","http://rscj2kxe75z46mhy.onion/","http://mytqqjx6qpc2dwdn.onion/","http://lol67pgq7qiemu5z.onion/","http://mdsrxt5akm3hdrhk.onion/","http://mzy76tt3bc3usfe7.onion/","http://lmpcu46fx3qbe2lk.onion/","http://mfzchnl2gsy6mtle.onion/","http://jloi5lou55trcoqs.onion/","http://jnpdys5vc4iee5n6.onion/","http://5dcgsgpuw5skq6c3.onion/","http://2g42quik4qa6weqj.onion/","http://cpzb6suwjfnmu7vb.onion/","http://glcaf7abpvgxv7em.onion/","http://bhjgaafdpo22oaaz.onion/","http://bskq7eatga4rtddc.onion/","http://ew7jixo3rbuealya.onion/","http://7mqnpygrnqr6s4un.onion/","http://7tuzqhktuijoo6ke.onion/","http://ds5gebfkymp7oeqs.onion/","http://7bjg7srvahdzzn3e.onion/","http://6oajjfiqnajvtfic.onion/","http://4nbnj2uqgrb5sppz.onion/","http://snowdrawcutezbrl.onion/","http://35z7phlp72hkbara.onion/","http://rqd6bhhgown53wum72bxticca3mexriudri5okxna63ltj5h6o5cu6qd.onion/","http://birdseggsmq7ikd3.onion/","http://2rstn7vutf6yrmz3.onion/","http://ow6z6hli3sbzxfkzvx2sr5wyfhwuoqbljpjkgewbzhhf4objbweftmqd.onion/","http://jbp56sfgbyjmxn66.onion/","http://zyd55gnxctpphw5f.onion/","http://y5zhzi7sdershbfa.onion/","http://wzcz3eioaok335ho.onion/","http://tachat3fqmnrdfpd.onion/","http://alc46qaydw6jldhm.onion/","http://4444444moqusjnjs.onion/","http://codigoq2rwu7ttsw.onion/","http://hfwmffbiphxpinca.onion/","http://t3e6l53mw4ow2xpz.onion/","http://es2p74ztvifttpkm.onion/","http://dcm6xhlrfyaek4si.onion/","http://q6di3hmsklj3xmnx.onion/","http://2nakedo7jo5go7n4.onion/","http://lchudvlge5qcqcp5.onion/","http://g5rydc4ynnppxqn2.onion/","http://tjlkabw5icnl5tls.onion/","http://x5ncm5ps4lc37rbkb4sb2bbdolopyqli2lxoshmfvtlo6sp4xq34cwid.onion/","http://tyfhynvn2skmyukh.onion/","http://i3kmkxtbe56na7ba.onion/","http://nbp3mok3zdm7v6cp.onion/","http://nonick7yncda4ktg.onion:420/","http://dmqbqksjkuv67ync.onion/","http://4lr3klgectas6tqs.onion/","http://7auisouypeegoefx.onion/","http://6rg2z67fkpco4poj.onion/","http://wallstz2m34ip523svfasst4iob3navmlmiblqjocizrui2gcoe2m7ad.onion/","http://secretmantgphhdb74d45c5mga7zcwx5bctjsn3pa42imay5kf4stpad.onion/","http://gotmilkfjxa6c3vd.onion/","http://hyibzyg7zj5jyful.onion/","http://mkjsmndp7pk5v327.onion/","http://3thilonwsr5okmnv.onion/","http://hmjwwsceqc6kyftb.onion/","http://qjp4tyuptvscswis.onion/","http://6zs2kgkmkh3zqws2.onion/","http://fqwng3lhx3piprdj.onion/","http://pmcz4titvczgfcrs.onion/","http://p7sjodulp43sez46.onion/","http://bitcoin3nqy3db7c.onion/","http://u2hx6oomkbwspywkknimeoieegghbsiynzmrohdiqtf6m4ni6xf5ymid.onion/","http://e3kewjfaphdzkrod7t6ttgnh2emcjwc7tcyuff4ejlyus4my725h6uid.onion/","http://tssa3yo5xfkcn4razcnmdhw5uxshx6zwzngwizpyf7phvea3gccrqbad.onion/","http://hchanu2or24rjm4dirxfo7uzbvd444uvg3uwdttdv4ikbabms6ddavyd.onion/","http://empty6suyb46r36d5hexlflt5cjnkmdw5mr4ij2k52oamgleerxm3uad.onion/","http://ctgpe2yc6ez56dhwd5hpj2tdkiuz4m5iy7347cpzmxyacphl72dmfyqd.onion/","http://5strggarp3gh73ehum32shras3rq3zmfxdahlcp5qer26jzdnvvlklid.onion/","http://headpetsv3ibutp2bg6yun62sed2kcdmui2qov6tknmkvvck5sex4rid.onion/","http://zionyay66mohoc2v47o52iz4q2mxac64olgqdqfvlhsnwui55j33jkid.onion/","http://giqffpotq4ywztyw.onion/","http://hkt47oecx3tkdyg6.onion/","http://vww6ybal4bd7szmgncyruucpgfkqahzddi37ktceo3ah7ngmcopnpyyd.onion/","http://ozmh2zkwx5cjuzopui64csb5ertcooi5vya6c2gm4e3vcvf2c2qvjiyd.onion/","http://oqwc4xrfgysdgw52tercv56vl2tfk5u7r6dspr2g2mwsj3dvb7zef4id.onion/","http://5rwsj326geilosq2sqth2r7hkbki5asgltd3uicccfgoc4wxsnveumqd.onion/","http://lgmtjgfpqk6hpik7yygkhavqivn6wsmfa7s7vszmcxwqkpwodinbhnad.onion/","http://y652ykp2irep7s7hn3cvgzdhycgyvw7twikcg6gqz5j4e2riwdw6kbqd.onion/","http://7fa6xlti5joarlmkuhjaifa47ukgcwz6tfndgax45ocyn4rixm632jid.onion/","http://4gpbpci6amqalhn76q6qo2vcbwnq5bv5zcstost3mp6tzoafqosxxtqd.onion/","http://j2eiu2izwjpazjevu4xs3muaif3jzex3nnvnu677vz2fypmzccvhhiid.onion/","http://oyt2243ddpi37zndrh5qkgwaidr5bgds34eoe7hgkozrldp7qh3nq7ad.onion/","http://45tbhx5prlejzjgn36nqaxqb6qnm73pbohuvqkpxz2zowh57bxqawkid.onion/","http://fakeidqmzq2kqvtf.onion/","http://usa7ks2j2zyvmgb6.onion/","http://megas62bfap52a4s.onion/","http://nx4ayfcyxcdenynx.onion/","http://myi5blmelcoulpa4.onion/","http://ldwjcwfruuxcuukc.onion/","http://gprkwvnqufby66ic.onion/","http://g36ypwhwuzmwo2ix.onion/","http://gz7sry5gachnw53j.onion/","http://ftbwfru6xeyilty3.onion/","http://kbb3mydergezd5ea.onion/","http://gbsmtwt7i4uhld7b.onion/","http://oynbzcpak3ws6fyd.onion/","http://cannazon4gbjluus.onion/","http://aruximnntveuhxx6.onion/","http://75uxxt4fqzmvgoqm.onion/","http://qi4qqwnfbmm4izsm.onion/","http://xhacker4c4zkvgbm.onion/","http://buc7olgk5wmmbhyd.onion/","http://dbezsgybfvgnag2b.onion/","http://bd2cllaq4gpt54de.onion/","http://ahiwdbtp7lmpza4p.onion/","http://bogkvjpmpyagsuvo.onion/","http://6azt2vs5rdhlzrb4.onion/","http://zk6u47ekcq447dzu.onion/","http://xndipxy3cvjw6js4.onion/"]

with open('forums_status1000.csv', 'a') as csvfile:
	fieldnames = ['website', 'status', 'Description']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	for i in range(22, len(arrlen)):
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

