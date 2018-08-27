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
arrlen = ["http://trini3wsazd6mcqi.onion/","http://2wkwvlmjhis4ohtc.onion/","http://applegftmg7jnzwd.onion/","http://udujmvy6pxnprw3v.onion/","http://zqktdno2ri3gizdm.onion/","http://m6zi3te5az6ytwah.onion/","http://bfmbfmq2wdo4gwwo.onion/","http://aqtf2r3digriswst.onion/","http://rdstnr4biap5nao2.onion/","http://ieshopxbmqxlka4a.onion/","http://metaldtoy5ktsxr3.onion/","http://omegaervdsjquv5m.onion/","http://ebprgtluo7ftxvhb.onion/","http://4tz34rtjhvpu7mgk.onion/","http://4xfqqm72warfafnv.onion/","http://autinv5q6en4gpf4.onion/","http://evilcorp6tqdni55.onion/","http://gtgmep4mv6gdyvav.onion/","http://nancyafb55rnxwem.onion/","http://sft7v7qwlsug36nh.onion/","http://ieshopqwkuururmu.onion/","http://4c7lpkd3v5gvd3f6.onion/","http://cn7v542gbwwtblca.onion/","http://2cgmcjb2567m5ihu.onion/","http://rc4itgiwqolue2ca.onion/","http://qz226vsfiwwwoiej.onion/","http://f76kjv7z3rnymawr.onion/","http://2weedmusr7fldufb.onion/","http://2weedmgnc6s2csk4.onion/","http://darktugaf7rp27uc.onion/","http://jtysc7irvqhaamn7.onion/","http://tvfwuldadbuem3bt.onion/","http://tqhc2rjadgqj3ylq.onion/","http://uhuak5r55e4lic7e.onion/","http://nlnjzbnok3df77un.onion/","http://torhostevzrd3l6u.onion/","http://2cgmc3xlmbrvbuti.onion/","http://2weedhxi7vth5tww.onion/","http://2cgmcc3mimvhzbqn.onion/","http://canna4jo3q6fwp4g.onion/","http://cannan53k7gr3pdv.onion/","http://cannadew6kmejyet.onion/","http://2cgmcf5vxcxm6eil.onion/","http://2weedoutw7bl6qpo.onion/","http://canna7jqg2lmxbeu.onion/","http://2cgmce3rwpc4reod.onion/","http://2weedkeahq3g3a4o.onion/","http://2weedckv6zz3bcmr.onion/","http://canna5navtigpzih.onion/","http://cannaalxnnzrypck.onion/","http://2cgmcbtxpjcytrcp.onion/","http://2weedvncsjtz7i66.onion/","http://2cgmcak37h6drolf.onion/","http://oyuds4cucq3y23uo.onion/","http://2weedzglph2sv57j.onion/","http://2weedw5hiir5ftcm.onion/","http://cannacdlwkzhrolb.onion/","http://cannal36nsyss3qf.onion/","http://cannal53y6panawu.onion/","http://2weedyrekmapdyux.onion/","http://2cgmce37wnc3iygk.onion/","http://2weedqzowsdnrt4c.onion/","http://jzx7ogbbrmte53bo.onion/","http://assassinec3wumxw.onion/","http://belrqxbmqgisp2cd.onion/","http://4dhznyhxfjwpuqko.onion/","http://ofn7ficadvdmozpx.onion/","http://22auadefxd7lzl6e.onion/","http://22aj22p34fczgf4a.onion/","http://jk4prisyvbfsopvb.onion/","http://pnxjrdveck6dx4qf.onion/","http://22ahiyg43btttswy.onion/","http://bitcois5y625bwqa.onion/","http://vbqwzm5ilwnkgul3.onion/","http://grams2o3bril2fr5.onion/","http://22a4ghpgv7iof5w6.onion/","http://tufdar7lksjgf6am.onion/","http://mo223xgiwgvw54r5.onion/","http://i7fcfbodov4m56qx.onion/","http://ddzhdibnf72y3vwx.onion/","http://pwqb6c7i6t6jgtsh.onion/","http://zsnkkap5xcjz3skh.onion/","http://xhk6tdt7si5kix2y.onion/","http://ts4w75jxb3plfteu.onion/","http://lolksweb3waft3gw.onion/","http://i3visioh6e3ibplo.onion/","http://t5pv5o4t6jyjilp6.onion/","http://pgqk33a2gvuwn3fg.onion/","http://tr5ods7ncr6eznny.onion/","http://ahaydkwihf4thyv6.onion/","http://occrpweb4n2vlmih.onion/","http://g6klvb3bfx3zuivo.onion/","http://hushnet2evovdyq5.onion/","http://gvvhyc5q7qcvz3hv.onion/","http://jabjabdevfoob7hl.onion/","http://tornulst2rbxvbpd.onion/","http://62glvg7qrxsjztpi.onion/","http://la7utxzw6ft3d3y7.onion/","http://5bmpx76qllutpcyp.onion/","http://opbod52qqfpdqupn.onion/","http://5cg4uomfj3cyiexg.onion/","http://6jnyk3igiphxjrig.onion/","http://ktg3bfvkzarqmchx.onion/","http://qualitykg247foha.onion/","http://dszgswrottqeohar.onion/","http://zazoid7vqqxcxhtm.onion:81/","http://wpscanskzvjc4s2s.onion/","http://xxxstarall5222sw.onion/","http://xxrlxxhjy6ed2d76.onion/","http://puta25qsnpoovjfi.onion/","http://pjmwycuystywzxwr.onion/","http://ivtjlpngajixbklh.onion/","http://go4jy6fuuvuqgqc2.onion/","http://a7irok66fwuechsk.onion/","http://76jcpjs7itwultnn.onion/","http://lain666qr74wihwk.onion/","http://fqxsl36gu7waxhc6.onion/","http://hpi62i3m5xwlynq6.onion/","http://g2flq6hly4i4frfr.onion/","http://yujwmnwlzmohcw6a.onion/","http://22222227qp2e2l7j.onion/","http://opiateco3fjzwtky.onion/","http://bakeryn4t2zyxmrx.onion/","http://3xvideonsnfxvcsw.onion/","http://cvvmezl6gtffprgt.onion/","http://quickbearrsk65rt.onion/","http://truemusicsrspqwy.onion/","http://ububabbtrjhkjyg2.onion/","http://uqmhrpskx6j3qsnx.onion/","http://goodapplenwgl537.onion/","http://buqlpzbbcyat2jiy.onion/","http://dirtycool6d2k6og.onion/","http://2weedajr7xajxyjz.onion/","http://2cgmcwccyfanewph.onion/","http://2cgmc3ep33e5r2ym.onion/","http://2cgmctgnzevpv4gm.onion/","http://2cgmcqawbgwfovcr.onion/","http://2cgmcs5h7yxr5iup.onion/","http://2weed5hvuchx2lhy.onion/","http://2cgmcovphsd4d5bj.onion/","http://2cgmcofxekvun7en.onion/","http://2cgmctl4hr2c2ccw.onion/","http://2cgmcnjebe3ur332.onion/","http://2weed2tr5bga4shf.onion/","http://2cgmclm2xvdjojnw.onion/","http://2weedbcyswlc3qb3.onion/","http://2cgmctkcydhcn2qm.onion/","http://2cgmcpfrymektixb.onion/","http://2weedchp4gh4t67i.onion/","http://2weed5blsyosculz.onion/","http://2cgmc2okekxehpjt.onion/","http://2weed5oiwk5dkytb.onion/","http://2cgmclhlesauepyb.onion/","http://2weed6oyly6vqqcq.onion/","http://qdmwuvsesrbazfi6.onion/","http://prvtzoneqaslqojh.onion/","http://snocirh344wv2gma.onion/","http://lmlnlio43rmi4jts.onion/","http://ppncys5qrazi6a3j.onion/","http://yhhyvif22flkku72.onion/","http://3eb4oh4xuhrc5ca4.onion/","http://2ucvcxv3canodidg.onion/","http://yymwt7qtkm7pxmtd.onion/","http://wiyjn6wvgqzmrx3d.onion/","http://rja2vlevomnwavoi.onion/","http://rewlfbkbp7i34sij.onion/","http://mpeimzdlmqvgfhxx.onion/","http://lzz3toovpitgffpa.onion/","http://h3rcnqowafzymyb5.onion/","http://7pp57kcjg7at4qal.onion/","http://6emt5u4smah4ek65.onion/","http://atlayohegxzianze.onion/","http://j6zb4g2mu5nn75tt.onion/","http://picxafxsrwh75kmc.onion/","http://yk26snmfuk2lexnj.onion/","http://joqpdgfowiwe7dai.onion/","http://wp5zda6x36moflsh.onion/","http://berlus2lsfi3dnpb.onion/","http://berluslbb2epoh76.onion/","http://berlusahd5otrcmo.onion/","http://berlusk37f443vn7.onion/","http://berlusp4xm7havyy.onion/","http://berlusz6dml222to.onion/","http://berluska7rediudv.onion/","http://berlusytl6nqdyvw.onion/","http://berlusrzrpn4hqi7.onion/","http://berlusl6ivdi7jks.onion/","http://berlusrhxkt7grh2.onion/","http://berlusluegbndpxk.onion/","http://berluspfjao3p35l.onion/","http://berlus76o5yyi7cp.onion/","http://berluskifrr7srjf.onion/","http://berlusp44zaqyg2e.onion/","http://berlusf7xog3hewq.onion/","http://berlusjh2vzamwjd.onion/","http://berluslex6ke4tnn.onion/","http://berlusptjo65kyfc.onion/","http://berlusenxhlwvbsr.onion/","http://berlusmfekg5rkno.onion/","http://berlushlxxtw4ll7.onion/","http://berluspqpezsg45k.onion/","http://berlusotmzqy26zo.onion/","http://berluslzwcpdcojc.onion/","http://berlusazv7u7zsnk.onion/","http://berlusvfq7d7r6w6.onion/","http://berlushw6hu7mr5x.onion/","http://6xjytib4jlbs2weu.onion/","http://zazoid7vqqxcxhtm.onion/","http://nyttips4bmquxfzw.onion/","http://7urdbv7ztyxttlsx.onion/","http://yavmob5dareyn5z6.onion/","http://wfe5dpy4ggovjwme.onion/","http://66gffy23sinyrxc5.onion/","http://c533yejjarshdbka.onion/","http://njxyfrru333aydnq.onion/","http://dx3g5ltzogj77mqu.onion/","http://smvdkh6nflywd64t.onion/","http://esjwngnhfqb4fax3.onion/","http://ocjqa4lmilqtvijm.onion/","http://axis7wm5f3sn6vet.onion/","http://3isbzrfiwtxpujv4.onion/","http://atlayowf6arroabf.onion/","http://sadfatraysax4eal.onion/","http://kkzbzsu5cqxlluie.onion/","http://2walletv43d63kfp.onion/","http://silver2ipggv7l4g.onion/","http://zinrm67igbdcdy5h.onion/","http://3gshsacpm54y2awh.onion/","http://wgrsskj6fsls75hv.onion/","http://sherivi5llggpb6h.onion/","http://wg3a5z4uv6gy3gfr.onion/","http://doublerajmfosfrz.onion/","http://sokd4o4qdk4pqfo3.onion/","http://dv7tgzsw7zgxgi6k.onion/","http://berlusconl7kq4dj.onion/","http://ok2utfuvknqy5wao.onion/","http://qplvvac4beoxezjf.onion/","http://jbdp6mmqfrr6fccg.onion/","http://iblackmnzab6lvjv.onion/","http://muhhu7tpiatg4swe.onion/","http://sd3y6vzijsrzfcgs.onion/","http://vgxwh2opvfxbk5wf.onion/","http://cbk4iqyencfqzmyu.onion/","http://nwe3cwuk6tcroeqq.onion/","http://ik3aml5qo37aeui4.onion/","http://occ4c3gx3w5esnmn.onion/","http://count7fqrdirj6ml.onion/","http://jbxwoz26447lhdjp.onion/","http://ijkmch45mxk3jnac.onion/","http://6mzu3etuaooadrnj.onion/","http://notaxbizae23xilv.onion/","http://secretsoufpkstaf.onion/","http://t3e6p2brzzyqzcw2.onion/","http://satoshiboxtxl3jh.onion/","http://oowade4e5mnynmih.onion/","http://mldolaese4gj6m7p.onion/","http://mo4ewnsy7r2j5khv.onion/","http://calmexitljiq5lty.onion/","http://tochka3m3iuiuqqf.onion/","http://jd6y26qodpevdt4e.onion/","http://vilpsgqxpa3decjo.onion/","http://fvg5wy6jy6ynnzpp.onion/","http://pissyv4c2xfkeqzv.onion/","http://irina6jjpf64tvqi.onion/","http://redroorkjv23wwpg.onion/","http://zxjfjmwtryninl2x.onion/","http://t2agpmao6yvu4xmi.onion/","http://timerwxjgququ3xh.onion/","http://ipfheqsid2ui576s.onion/","http://55ojvippcr4z3cif.onion/","http://o5lagghf6udjvinv.onion/","http://igttvp6myjenburt.onion/","http://darkxnlofu2bby27.onion/","http://75js7jjcwekw6geg.onion/","http://echbmnt7qx2wcsad.onion/","http://7lbg5jnfqko2nfmr.onion/","http://r6ykkqjvtvndydqk.onion/","http://2222222dhfeojzgo.onion/","http://rlpot5onsm352al4.onion/","http://ineuup2dpgjz6jit.onion/","http://zcjr5q2kymzqsu6h.onion/","http://calczc2f54fsnkhf.onion/","http://chat2djxbuggjqof.onion/","http://anheruexcqlcmotk.onion/","http://c2oreviewu3tlazn.onion/","http://2utgzidkmt3sict4.onion/","http://a7uxyc7o5wkjot4i.onion/","http://cashkxxqpzbgggg7.onion/","http://gauravocppcrj5wi.onion/","http://rsclubmoejblgmkb.onion/","http://vendozl4vya7i6ip.onion/","http://tochka3ev4zpekll.onion/","http://reviewef2jhdet6c.onion/","http://rvooavvs5ztc4ind.onion/","http://sovjoqjs5oh4iyrw.onion/","http://truth7mxripnsmmi.onion/","http://mdnhpj24s5a4soei.onion/","http://chattnx5gnmc6sqp.onion/","http://xcy7x6r56aok4uew.onion/","http://piratecrn2j6qvbh.onion/","http://empe2453l2eiuaqn.onion/","http://o4xh7z4igukzhluc.onion/","http://e7sinbno3tmp56j4.onion/","http://xillim7a2p2q4w6z.onion/","http://dmc6zftow7nlxbyp.onion/","http://hhkshb24j4kb43oa.onion/","http://dhlshophgafiohuw.onion/","http://z2hjm7buf4dv32cj.onion/","http://brocardspoatomdk.onion/","http://gygr2kk4z37yjztw.onion/","http://42x4panyccnjtw6o.onion/","http://ufp67mmcvg6eck43.onion/","http://hackr6rcgcyjclaw.onion/","http://lfbg75wjgi4nzdio.onion/","http://kd3yugq3tgcvwxrk.onion/","http://bitstlhqbyor2feo.onion/","http://tochka3oqunhm53a.onion/","http://rrbm3jiflz3euxhp.onion/","http://tochka3rmabu4p46.onion/","http://kplatypqsro7vsvg.onion/","http://ph7yz2mz64rcgyja.onion/","http://65px7kxuqi6s73zj.onion/","http://tochka34nwb5527c.onion/","http://z7kgttnatoa3iopq.onion/","http://tochka3kqjpgnzbb.onion/","http://tochka3nkz53rorx.onion/","http://tochka3aenhmvbsg.onion/","http://tochka3uetju2h7h.onion/","http://tochka3vhdxo3xlv.onion/","http://xyxdbvln3ipl7g27.onion/","http://tochka3oo34hax2k.onion/","http://cp5ju2qrbfrwz4z4.onion/","http://33lteihgfct47pmw.onion/","http://tochka3ntgcn25gh.onion/","http://pzdvtxlsskztuzqv.onion/","http://tochka3eoioifqem.onion/","http://uspadsk62m52nivb.onion/","http://tochka3wq5d3hr77.onion/","http://xljsxrmsa63g67em.onion/","http://v63r3c3tszc3crim.onion/","http://tochka3bumgkqmah.onion/","http://fakxn2uwihhvelsj.onion/","http://tochka3h47zny6hh.onion/","http://qputrhbinreoyw4j.onion/","http://ajq5g5fjimk4ezgg.onion/","http://gmslpovriwcfqzd3.onion/","http://cjcinyfh6cwcixd2.onion/","http://grams7enubqgvbfh.onion/","http://g4wmrmqxpj5bnvml.onion/","http://fovisionunz7mtxw.onion/","http://aecorgjoozota7sc.onion/","http://ai7kuomdzqzzqedh.onion/","http://tsteen46itfjilys.onion/","http://yandexey5vgybd5t.onion/","http://muslimlbcnmtdgwu.onion/","http://e3v3x57ykz25uvij.onion/","http://nswgrtkppv2q6w2j.onion/","http://yrz2nwkpkchl7cgo.onion/","http://b6tnq5nrhxu6tqeu.onion/","http://aw2knlnz3qs7kcq6.onion/","http://vceqn5ijfxpdosdi.onion/","http://hydrobulrm3lq5g4.onion/","http://storeq6uy47cxxxv.onion/","http://greats4cyh74auhk.onion/","http://qucswuzwk3ayzrqx.onion/","http://pastehtxeeuhkg6h.onion/","http://j7ljeh7yyefpzs2h.onion/","http://b32jile5ig27ozbb.onion/","http://uwyewfmz3m5pin7c.onion/","http://gbbeem5oogwssp57.onion/","http://lpkbsi574ode4ebv.onion/","http://ky4gpqoqvfgteh74.onion/","http://dcentralqknjxqy3.onion/","http://jlzxz2uhue5az4oq.onion/","http://me7lkvknj4kncahr.onion/","http://sieuowubaewxukbe.onion/","http://ukpxjtlp2gatrlhl.onion/","http://cardsm45wfaxtgrd.onion/","http://dpanely75rdnw7yv.onion/","http://espenav2n45atpsj.onion/","http://yb33xgpicm7deoby.onion/","http://enterccmdzerqlzs.onion/","http://2222222qbzrkxl7l.onion/","http://bkkhc7ana6wujsgg.onion/","http://day7ddcjfxrbemwp.onion/","http://didwforumsg2klx6.onion/","http://wannarcgxjn5hqc4.onion/","http://buywdci7rfvec725.onion/","http://6fneqswaqwevhvsf.onion/","http://slwdyj5yamu4hray.onion/","http://hncpugy26xw672s2.onion/","http://undl5y53u5grlvmm.onion/","http://5dcueb3vevjgpjnj.onion/","http://rasppixyesqtbhun.onion/","http://bicxrvlly4dxueka.onion/","http://fflmwwyjumwgsryx.onion/","http://s7wzxcyxf5yr55qv.onion/","http://vw7hn7dsyy75zglo.onion/","http://qly5mc72dcxupjdb.onion/","http://mlokkzaillfybfqc.onion/","http://llk4g25qoey7vf5a.onion/","http://universrdvf3doxb.onion/","http://freykjlgjyv4dx27.onion/","http://kaq6khemrnrk27qe.onion/","http://5qdge4eq5elnplq7.onion/","http://phroegpersewflua.onion/","http://5jdnctbmppvtsv2j.onion/","http://5hxkknmo7wemqf42.onion:84/","http://k5v6bb4dfwlvhovy.onion/","http://dkzwaqmcms6qledq.onion/","http://ktywpnwpr7hhlot5.onion/","http://7zu7dsntxmttnqyt.onion/","http://joho66dk6aovbl5j.onion/","http://qdg2vqtjhjntv2tz.onion/","http://e7snvnx3jj6aundq.onion/","http://c7o7u47cdr6fpj7e.onion/","http://znxwmp4r3m2tr3nf.onion/","http://ccavmwxs75pteetw.onion/","http://mid3de7dzajyaf5h.onion/","http://fakjgslqindxvaol.onion/","http://skoh2ov3yzwprcnu.onion/","http://gredc7zndtbkunkm.onion/","http://hxinkdmhbbnjlno5.onion/","http://fv4tyy66duvjcsd5.onion/","http://k5yoqktlkv6m2p3r.onion/","http://sophias3emyhti6v.onion/","http://kt2o5bkvaty4mwag.onion/","http://7cbvn7cqksjdcqo4.onion/","http://ykdqzqeejqhec22a.onion/","http://freddyq6t5fwz66t.onion/","http://5d6ihl6m2uvyvkxy.onion/","http://6uhryhsrr577vykz.onion/","http://ppcenthjv7r4uuxy.onion/","http://hljzmlorwllunrzs.onion/","http://dlggj2krbqzm5dru.onion/","http://ngkr4ihsbyxcmkle.onion/","http://fplmrobtk2xafypz.onion/","http://uryzjbwpc2oydqdk.onion/","http://oznfdgb3zhlotupv.onion/","http://4uluckyr37dccmjj.onion/","http://z4m3tksa7oan22zn.onion/","http://atmblc2s43smwrho.onion/","http://souolacbmsncl7rp.onion/","http://ghoctrhqhaua7a5f.onion/","http://clowiozj4xq2tf6u.onion/","http://ccswcghwmgwpxrhn.onion/","http://ccgqggl3calxoshx.onion/","http://unolieqxsxpnyjw2.onion/","http://xqxcqeillzal5ldp.onion/","http://smorfo7mjlha6kfa.onion/","http://tfwosuvvwkpe7u5g.onion/","http://njsbl7erklzhdefq.onion/","http://appeklqu6i3yzzze.onion/","http://monhu5l747tkqkfc.onion/","http://gc4yz3dvthcolcau.onion/","http://trazw266zdyqpile.onion/","http://65pg3cfnrc3fqt6m.onion/","http://rotcx7hvcm7yv3fm.onion/","http://kicaopbfaxoi4vpr.onion/","http://ccgsw2o557zjix3f.onion/","http://3dbkxpcny6pu52xp.onion/","http://venbpmdwc2ao4led.onion/","http://galmwlp5r7zd7ahu.onion/","http://fximywen2qshmiut.onion/","http://clg76tfxiwvtjm7s.onion/","http://easxj7dy64taslmf.onion/","http://weagokaoxq2rfne7.onion/","http://rtwv2h3gzj27hbnv.onion/","http://33oxridbl5rqa3xd.onion/","http://smoszrzottqzacly.onion/","http://en3znb2ybmcv7ryl.onion/","http://fix2eqczq7vcjnch.onion/","http://freet3vkyquubk2a.onion/","http://x75wyufapbsqvjil.onion/","http://euifynkwxoo7vzvg.onion/","http://easamjmwgvgaawlz.onion/","http://djnyk3opqkse266g.onion/","http://bh3jyzedqpdy7cj6.onion/","http://carp3zvq2a2q5oo2.onion/","http://gvnrp6yyo46xsktx.onion/","http://saf4mnceoo6vpa43.onion/","http://rsor444hl7q7qq64.onion/","http://vrmd7biuntnexocl.onion/","http://rcic4gafnschmmr7.onion/","http://bjjebcwfqmttn6jk.onion/","http://dir2dkvr2kimjtmk.onion/","http://thup7vnf6hto555g.onion/","http://dfcehba4i4diz7bd.onion/","http://foos5z5smq6ftsj6.onion/","http://venpqwrzslo3y4l3.onion/","http://oni7fk54ng2ye7p7.onion/","http://joifjmbnzmogky56.onion/","http://abbychp44hhgyfcw.onion/","http://gcz4bwnmqn5kzaoo.onion/","http://3luosk6acg2lox2y.onion/","http://5oz2wzzk6bmf5hdu.onion/","http://halfinzvpgeyumtd.onion/","http://piehbr46l5gcddur.onion/","http://sbd4nbngr6r7ss33.onion/","http://xwjo5cq2fuuh2iih.onion/","http://j4jw5bsfzlhh27cw.onion/","http://xr2l7y2cde6votrl.onion/","http://yezictqifnbrcbkj.onion/","http://agorarezkklcjpv2.onion/","http://rzjbrftkueoywd7v.onion/","http://bm6mvvp5deruwq6g.onion/","http://golden7djzq32zh4.onion/","http://easyvisa35qagd75.onion/","http://3g2gdd6mgvrqt5ve.onion/","http://gjoywniqxlea2etk.onion/","http://msyc3ehs7h2ve4nb.onion/","http://22dvf4xgaqa672b4.onion/","http://v5zdbzazt6kypfme.onion/","http://iubndoqsdttzg53h.onion/","http://4urimmgftmy3gb6d.onion/","http://onjw3aswwhahbzi3.onion/","http://agcrxgirblqow6ct.onion/","http://oninj3zhk7e64krj.onion/","http://btcwwhnqi5w5yxjb.onion/","http://dafynex6ytjnpeo4.onion/","http://ds4qg7ygmmdmz7fw.onion/","http://7yemlckvmno6yk7y.onion/","http://xilh6pazf3e6sxg7.onion/","http://maiufmtu6ohdchkw.onion/","http://ueuq4jcf7tvkedxy.onion/","http://cre7vocuuabyigce.onion/","http://vd6srajujbotikcl.onion/","http://noszhbeg5lqqawvd.onion/","http://zlaehcuajft45pvy.onion/","http://bfvcaznnxcucn5zc.onion/","http://buyjtasu6npq3rxk.onion/","http://dru7ftbwfunpvoim.onion/","http://euroopt2pscfiexp.onion/","http://w3ussgmz6ihmox3y.onion/","http://m26kmqhtqmb2ydsb.onion/","http://phozzhl5fie2r3kx.onion/","http://nopmzsme57dwwijo.onion/","http://umfgj5bqageje2e5.onion/","http://achyd2h5obe6qj7e.onion/","http://ngxgq6h3iub7uaxu.onion/","http://chatmoydxj7y3his.onion/","http://4p4sabmphzbkifwd.onion/","http://xxyqn3eyt5jqpmcf.onion/","http://btcwash42xhn5rkr.onion/","http://tut67mbrftvrqlku.onion/","http://wegrsp3fh6hdguhc.onion/","http://fhost3z3umfyfuwg.onion/","http://nqggd24kladclcrp.onion/","http://ccgalaxyarcymyhj.onion/","http://zfq7tgxed245jpdz.onion/","http://j4odlmt4ggo3fxai.onion/","http://h7ucigzrqi5rjigz.onion/","http://bwhostszufr7wlqc.onion/","http://smk4dw5cbxd6lttl.onion/","http://3ixxzhxifwsmo3bw.onion/","http://btcvanityuccobba.onion/","http://jmkxtevzkz4w4ctg.onion/","http://mb7ib6gsypaph6i5.onion/","http://godaddyyrebotebe.onion/","http://nv35unyqmxbbkfah.onion/","http://evilchatxp24s7vb.onion/","http://marleysne3mjnm3j.onion/","http://auuousc62vep34om.onion/","http://4rt37xtos5xbxzgy.onion/","http://rjye7v2fnxe5ou6o.onion/","http://legendaxdwra7ufm.onion/","http://bt4gofvhppoxvzxd.onion/","http://b45qviypbc3huiqj.onion/","http://2222222ugah2uexw.onion/","http://bdtq4shqkbb3yy7b.onion/","http://sml5wmpuq7ifq2mh.onion/","http://tumblerfl4m3qbgq.onion/","http://hackera66mgvcdbi.onion/","http://vendorrkw6jben43.onion/","http://zzqok25aw7xv6qio.onion/","http://5dq34twntth6vw63.onion/","http://consortqro3giwxg.onion/","http://43f74pccymmgu3sf.onion/","http://bit5ivgul5wi2jbh.onion/","http://app6c2aximup2sau.onion/","http://udufj6czhzuewpdg.onion/","http://trinsk54zywx6mpn.onion/","http://ct3vx6aeqkhitinj.onion/","http://young2cvcf546l2f.onion/","http://uw43tal2d7wwziju.onion/","http://kksldwjjgok6ymhd.onion/","http://gramskfaxyyr76my.onion/","http://ylcwna3vykfruojh.onion/","http://albqimsntkyaxra5.onion/","http://rlgl3jbvb4tcw543.onion/","http://4el33fbvm55z2aad.onion/","http://ryes2rgjweevgeim.onion/","http://gxlbqkzneavjh3co.onion/","http://a57mizpya7yeqvhk.onion/","http://jhcpvl2hgybface7.onion/","http://p22enwihrhxfay5p.onion/","http://6zccg6uvu4dfm3lo.onion/","http://jebuirc5j6cnrtft.onion/","http://app3plwpgy4ilcbj.onion/","http://selfhostoma2sbtv.onion/","http://ccqqo2jwgk73aoad.onion/","http://fn6njfnde4jcfrzb.onion/","http://dumnuhrvhkhh6rtg.onion/","http://clohyr7upnphax6z.onion/","http://32pdppwj3gbz4jcd.onion/","http://blkk2xol34ivyc5j.onion/","http://avekasodnjh34xat.onion/","http://2ppegyrfiivfsd4l.onion/","http://visazoo7xt2kzkn7.onion/","http://car7rmkohwqlpsai.onion/","http://druqbxiddp7ulcrn.onion/","http://hss7tftmhgire6nx.onion/","http://dig7sokwesjtzjcf.onion/","http://actxatnrkvqmzhmq.onion/","http://b34pgjrmuyxox2hh.onion/","http://carjruw5qwxuiquk.onion/","http://luxlabsatowqepew.onion/","http://burnerphjpurui6e.onion/","http://ddosiswanmkqqesy.onion/","http://eohmtpwpw4wzgfhf.onion/","http://2deeejwpe2uafwgb.onion/","http://yqlugargsfat6wp7.onion/","http://vtgnj3vecqvw72sd.onion/","http://valx4qsfdnwmmu5h.onion/","http://dszarlmp7b3etsf3.onion/","http://wk5zcekbdy3rw67n.onion/","http://b3n25wg2s2ghx6vp.onion/","http://7kbvnvzodzy76cx4.onion/","http://wg22u7loslfwf3jf.onion/","http://6tadkeyewzy3cvqo.onion/","http://awdac2ynp56jfn3x.onion/","http://wnmde4d7ofwxrzrq.onion/","http://armluyc7z5vwbswm.onion/","http://ewjann5aqsxl6kwy.onion/","http://ecwcn7kxkfcbaxab.onion/","http://f6n3slk5u2ncczzj.onion/","http://fvxpj3fspruw5fcx.onion/","http://ha347mmcolid3u2j.onion/","http://j6mjdy6hzs572qec.onion/","http://jd5dq5phjs5day4e.onion/","http://lila3i6652bmcxue.onion/","http://jau64rs5f73esq7h.onion/","http://odyr4nbvvjnwa6gq.onion/","http://oteacijijf2gosri.onion/","http://royepgvo56a42ow6.onion/","http://emp6o47fr723tfr2.onion/","http://z7fexvi2b32aqnwo.onion/","http://xbriltev7uoje77r.onion/","http://ytsvdfybuy624wvb.onion/","http://ysaovczviagafs3g.onion/","http://wrhr2jscceaj67jk.onion/","http://xstns34o5n6xt3jx.onion/","http://rupedo2jwz5l4lil.onion/","http://honestcmyjtyhi5d.onion/","http://qgicr4jsrxju2zee.onion/","http://jw52mhenlzlfn3ah.onion/","http://puxmeqpbytormyuz.onion/","http://mscf2endodmt6qga.onion/","http://byjxywdwf6wj34m4.onion/","http://z57whsalg3kuvseh.onion/","http://torbicihal7n3suw.onion/","http://luckpyskdd227zzu.onion/","http://vdwx3pkqdegp3vde.onion/","http://udis3bi6s3nmvjuv.onion/","http://astarotyn5uilwx2.onion/","http://3vjwtbo7lv5ch5hw.onion/","http://wu6fasrukd7uuq73.onion/","http://dwjobsyc5xlloug4.onion/","http://ys7bhdnc4csclgr7.onion/","http://apfront5qxkubpis.onion:4444/","http://phpbb4442zaxnzem.onion/","http://libbyyqebmv4c63w.onion/","http://punbbdm7hxesx2w2.onion/","http://chipmixerx2wuywh.onion/","http://ddosiotrexxbasdk.onion/","http://agiu2ehojyk3mxsn.onion/","http://uiqwb552flfimtbs.onion/","http://o275agykqaxpvip6.onion/","http://yaqefkkgxq2almdk.onion/","http://7ym4gje754hdwht4.onion/","http://openroomvru7anxk.onion/","http://annolnmf5dz6u5xy.onion/","http://33qvlt5je5kif3jq.onion/","http://recipeshtx3vpqjy.onion/","http://2ruvapnwc2rtbogj.onion/","http://3wirxietn4iktvf3.onion/","http://iamevilxgzo2y5xr.onion/","http://6z3abxnpg5vg33dz.onion/","http://cves25afu7udlwj2.onion/","http://drkqblouvg3rqqgg.onion/","http://deeq7pdquets5il7.onion/","http://fbc7jrx3dqmeoecj.onion/","http://gf2zt7i4xlat7ltp.onion/","http://grapbj3xfihbzhiy.onion/","http://h24o76gvuokgihxd.onion/","http://gxauintu6rsxorsk.onion/","http://kxoypudqmcmynfaa.onion/","http://sec2xmlwsdnite7t.onion/","http://jmkl5pqbxybcfitz.onion/","http://ityxhga27lcfot7e.onion/","http://oxwx7oetuhkdrsw3.onion/","http://qzbm7rpouwwdqkvh.onion/","http://ims766irfwcyscjx.onion/","http://onikmmou4bl2to34.onion/","http://kmaa74dzoqtbvahx.onion/","http://legrrdmyeoscqv63.onion/","http://mon7pbqcvd2mk227.onion/","http://phndf75fkcafa2eu.onion/","http://qvyn5g5inmna5uip.onion/","http://slavsvhhf7lviqir.onion/","http://torwag2wvuyoudc4.onion/","http://t6khyme3mvxi7ugu.onion/","http://tomstrejvyaxrgvw.onion/","http://222kehxsw6dvthv6.onion/","http://w36ug7hmamuleo22.onion/","http://xmaxu4peiv6iuiad.onion/","http://vriqcyenlvslskyv.onion/","http://xmhipvrbsjaxe4ay.onion/","http://whitemoagav4ttrg.onion/","http://watjvc7dh6zkn6tn.onion/","http://wt2gi6tpxkmz6ztq.onion/","http://y3zstq3rtzpjnwll.onion/","http://igyifrhnhqxmtj3v.onion/","http://2fvz6i2c5ap5wygc.onion/","http://newtochkakur5dc4.onion/","http://evilmln4ptxxwtug.onion/","http://paxt4n6urwx7uiah.onion/","http://filesgggipc4jwl7.onion/","http://4py2ph7eq3aopyug.onion/","http://ngp5wfw5z6ms3ynx.onion/","http://qsz4euwcidhjxewk.onion/","http://itabazmyqhetejqe.onion/","http://dbm6ubswxz3sibdm.onion/","http://sb25swetifbuja7m.onion/","http://cg4odxiherxhrplp.onion/","http://sibvdsitiy2oml4b.onion/","http://uhwiki3bjmzjxojn.onion/","http://y3ovdlfl53k7ulf3.onion/","http://cardsurfsyzmiepl.onion/","http://cashlordseysp5r4.onion/","http://mzlgvlcmsdksmsmb.onion/","http://7ep7eigbzvzpgbto.onion/","http://lclmnroewgycudgz.onion/","http://fadfnkdfbllvdzwd.onion/","http://poseipvskekd7wiq.onion/","http://zzq7g2f2spplomjs.onion/","http://deepsea2ou77c6vw.onion/","http://rm3tg3urhoppuprx.onion/","http://zreichmal46mtbcp.onion/","http://bitcoiamkbwscbb7.onion/","http://obg2befrwhdmhhrm.onion/","http://776mef5rfv3evriy.onion/","http://gkxxkddhnrqhdwlg.onion/","http://cdt74sr5buhezutf.onion/","http://vkphotofqgmmu63j.onion/","http://darkmzbu2ojpi2bk.onion/","http://gpwdyiew5mygjc6q.onion/","http://kuhfvm53zcetvdi4.onion/","http://czfuctuccsloeqsf.onion/","http://hwccoh2r7tm2yx5m.onion/","http://rpa57xh2wfmh4y5u.onion/","http://rrczvzeqlm7gx46r.onion/","http://social5dgegf5a7k.onion/","http://sgeffsn6tztqzlpx.onion/","http://citadelv53oultra.onion/","http://krpyovb2m6nfcose.onion/","http://moneyrnr22vgcil6.onion/","http://autshpxnxhuv4aip.onion/","http://xxxxxxvhtkilt6ju.onion/","http://cryptofxxpxdnelv.onion/","http://zxn544blenycpnvn.onion/","http://hydraruzsukalk7z.onion/","http://kjqq6sexhlaqyfgu.onion/","http://kopatvooh4bk6wcu.onion/","http://jncyepk6zbnosf4p.onion/","http://hho52bhyvh65fhlb.onion/","http://prnrpiiro4q3b6uf.onion/","http://intrcept32ncblef.onion/","http://26hjh3nxkqsgi4zl.onion/","http://fn7xosrfk6pfk2ts.onion/","http://xtthkg74zpt2skec.onion/","http://tho2f4fceyghjl6s.onion/","http://6ow32dhlifdn6ah2.onion/","http://ihz3xcqucwdrqna2.onion/","http://blackhost5xlrhev.onion/","http://jzxnsn6wgiwtzyr6.onion/","http://kpvz7kpnyemj5puw.onion/","http://qeya6vybwsiegmvz.onion/","http://yzdtu56mhivseonm.onion/","http://js27scjrosjfuviu.onion/","http://lchcddfydju4qdfj.onion/","http://jisis5ymzp4f2zzw.onion/","http://berlusconhhhpbdh.onion/","http://dbworldszyeggadi.onion/","http://dcplacegeackzjtf.onion/","http://answeixte6hpdfei.onion/","http://kxojyo345mp5bwsr.onion/","http://secretsomtkqkqtw.onion/","http://insdkhftd2p2xpd5.onion/","http://ros4fm35x7xn6man.onion/","http://darbxn5hc3tjf5ew.onion/","http://greue2kmr5nn34dv.onion/","http://tduh4bjmwm64tkbd.onion/","http://ans6gix25xdlqb7r.onion/","http://enmuoexke75skkuu.onion/","http://etrdwkkqvoqapz3g.onion/","http://yvwgafqnddrdmmhi.onion/","http://hnx3rifrpf74jseu.onion/","http://hhhe3bxncbgqsha6.onion/","http://suirhii74snoby7q.onion/","http://wgwzte6v6t2vtgd6.onion/","http://2222222fjgch7zpy.onion/","http://socialfortisciz3.onion/","http://plexcox52hxxrmaj.onion/","http://4cp5vnbcc7szxddd.onion/","http://kwn6i5jng6bsow5z.onion/","http://2bgqw5szz2i34nek.onion:10000/","http://2bgqw5szz2i34nek.onion:20000/","http://prefix64kxpwmzdz.onion/","http://ssystema5qgucqea.onion/","http://3rrpvbdzvbkzrwhu.onion/","http://applymxgdt32vjzq.onion/","http://blaze246uma23h7s.onion/","http://6ugt6t4rxit4w2va.onion/","http://wpressfuctwlk6iw.onion/","http://fvyfngblahhr2efa.onion/","http://i6zsoimtwuh6ulzz.onion/","http://hrbldkjg53ilkgk5.onion/","http://hss33mlbykbsxmug.onion/","http://oeyaizjbn5qugev4.onion/","http://u5yovkdeahw4hhim.onion/","http://vjxoruceujq2ds7v.onion/","http://zj5p6akh7prxlavt.onion/","http://cz3zmh6xmojyo27x.onion/","http://otakuqvjhvyxhu23.onion/","http://ohbxl7hdfwcwc2ix.onion:81/","http://hucoxxyf4y2nko6x.onion/","http://xanaxringrhrguit.onion/","http://rcking33viegekey.onion/","http://5mixe52ciigyf2vb.onion/","http://vndarkvwwannpa4c.onion/","http://i7ahrqp3juo3m5hi.onion/","http://2bgqw5szz2i34nek.onion/","http://3w7z4z4nkmu7psyb.onion/","http://3rayvk45ccni4nau.onion/","http://64e7tdjizjycvdbj.onion/","http://ajqvyk2kwgyvoss4.onion/","http://hlzqmmjwbuff7qx6.onion/","http://aglwvuqk6hzjekvq.onion/","http://ggerson5sqftmofo.onion/","http://lcrgwum4luxryiyi.onion/","http://s34jxzlzc73s7ak6.onion/","http://zthzvwn6aokht7ox.onion/","http://yulxt5toyxavkb7r.onion/","http://xbha3lq323ac5lbf.onion/","http://r4u6jtmqzuedlgle.onion/","http://hackthhi5zjgnxpp.onion/","http://bitmixbizymuphkc.onion/","http://vkusvilulz5q2sfn.onion/","http://dumpsmanicnptrgr.onion/","http://y3zcewihgcbvi6am.onion/","http://hskyo3zhqmdkpfoz.onion/","http://jlqqnfwxrkurzrla.onion/","http://r4qvpg7te7nooswd.onion/","http://tmxwwir2rbxakwmi.onion/","http://igyifrhnvxq33sy5.onion/","http://leb3rkvqzw2qd4dg.onion/","http://nxozapp6ag3yeuxi.onion/","http://skimmerkvmpi5vyn.onion/","http://uvovhkv4t7ku6p3t.onion/","http://s5lm6bpfhs7nrug4.onion/","http://nx7xw2x3flcrlvwt.onion/","http://nkzcfuoatveu26pe.onion/","http://darkwoodywhgd6hu.onion/","http://h2yodozj24uiim5y.onion/","http://dvqjiduavgd2itj6.onion/","http://cynpqiop45zmnm2l.onion/","http://clfafhbbepamjxgc.onion/","http://netflixow6sfugri.onion/","http://6psa7ryetayyhim3.onion/","http://africa3xmkxhjxz7.onion/","http://paypal46e2r3fm3g.onion/","http://aprovpnacgvqwh76.onion/","http://gus235m2le4ato4b.onion/","http://fulltalkthpriukq.onion/","http://auutwm46uxgypavg.onion/","http://xnaqhacxm7ekfyqm.onion/","http://z7tfewz5b3tydzmx.onion/","http://bitcoiq23uoml6qs.onion/","http://6b653stlyz3hqlyn.onion/","http://twftyemug4vtvm2s.onion/","http://tvhxx7ojzyvdpuqu.onion/","http://ttiywqzgo36r5ewl.onion/","http://tcy5ympaiuj4h2d6.onion/","http://testn5it462fcryw.onion/","http://rybvh5eltxkf7ddw.onion/","http://in73dwrj3ajer537.onion/","http://bitcoiimqy4kuj2v.onion/","http://bitcoi2zijrsw5xq.onion/","http://hostzk6yogkzahx6.onion/","http://cg42x4k3barr6goy.onion/","http://bitcoigktk3jdlvl.onion/","http://4pvv6e6plrfgwmep.onion/","http://v6z5mqsndxlpbjn4.onion/","http://wj2hfwd4x4w6p624.onion/","http://tp4dt6smuyzw44kc.onion/","http://r32rlkfglxy27rps.onion/","http://da5skoovledar6lp.onion/","http://dpccn7wxegr2ucj5.onion/","http://o3wj773vcn3l2eqk.onion/","http://o72rrnro7sa7mr45.onion/","http://nf7skuafvlgz35lq.onion/","http://annolnmf5dz6u5xy.onion:7001/","http://ard2lyowml4zol5h.onion/","http://jbmkwjtq2mv7ow7i.onion/","http://rolsyxlgetrzsf64.onion/","http://fpnmwpg6klsa2hrp.onion/","http://hohd2jwkc2oentqe.onion/","http://72v5sc2s6kh3epom.onion/","http://nzlbyrcvvqtrkxiu.onion/","http://p6afzcaghpulzr5r.onion/","http://ggovw2oumclyhjwf.onion/","http://2jqzwpj2ftcywncb.onion/","http://stpqmju5dngujirm.onion/","http://kznam6basvxxdcpf.onion/","http://atmjackrm2zolkiy.onion/","http://ir5aduqnh3xxuzb4.onion/","http://2oywvwmtzdelmiei.onion/","http://hydro3xpfcrwqoiv.onion/","http://hydrobuwolvx6gya.onion/","http://hydro2spqk2mu2vd.onion/","http://drupal63n2ah25qh.onion/","http://silkroadknd2nsso.onion/","http://silkroadaxfsonxn.onion/","http://silkroadh5xhchti.onion/","http://y5kawj4pacapewpr.onion/","http://greenhighmnfg2iy.onion/","http://enej6ausj3nkfwvf.onion/","http://hostdanyyyf65r4b.onion/","http://snz6hyhsq6wmecot.onion/","http://icube3w5rd5muuna.onion/","http://joomlaxwzzzfzt4r.onion/","http://psycosxy3qnmap4o.onion/","http://milkwxjpscr54dlm.onion/","http://7uuxkgy744yrye46.onion/","http://wqo5q3xlbmwyylmn.onion/","http://554iijfzf7hztntx.onion/","http://onionnon5utuaqfq.onion/","http://simpleacidcar43x.onion/","http://icloudt2m5mrjtxf.onion/","http://royaldmpsprlxhit.onion/","http://modx234ajkt7jhgf.onion/","http://faktory2kcaduuvm.onion/","http://deephousewavvhvb.onion/","http://bitcoiuh2afj5fvs.onion/","http://bzassxgorufaqfrx.onion/","http://2222222ep67fw3hd.onion/","http://74s7l75xdjbwlc26.onion/","http://22222222b5jjiakx.onion/","http://rsclubczyxya67fx.onion/","http://bdforumjlxvamrbj.onion/","http://bitcoijnadw7tzd4.onion/","http://bitcoitcityqqh3w.onion/","http://bitcoikrrorilqw6.onion/","http://bitcoizxxzje2eld.onion/","http://bitcoihoimasigli.onion/","http://bitcoidyvgrhvdnv.onion/","http://bitcoiiy5coqwlir.onion/","http://bitcoijllnuf4ard.onion/","http://bitcoimpqhbyqdwj.onion/","http://bitcoikcxhkchejv.onion/","http://bitcoiyxs44eei75.onion/","http://bitcoi23mhlxb3tl.onion/","http://zhiavgfsrustldya.onion/","http://moietybfhbdbulbw.onion/","http://gfzw3wyc5lzbro4d.onion/","http://bitcoirszago3q7l.onion/","http://freezelniasseeuv.onion/","http://cardinglsccjvcth.onion/","http://vdlsvi6c2vswvhfx.onion/","http://h45lm2za7jemmcvr.onion/","http://jabberlistbrrxyk.onion/","http://pzb2eyp3xsfrgwul.onion/","http://finedumps3ml4k3u.onion/","http://3n7jnjir2g2ddslv.onion/","http://glasswerkruxyorl.onion/","http://cyruservvvklto2l.onion/","http://kittyst7ey6shcg3.onion/","http://5ngkexajc2jvwgfo.onion/","http://blockchainsomexu.onion/","http://funfair76zpa7w4e.onion/","http://2pack24a3s6ikvg2.onion/","http://2222222kt6vihsl6.onion/","http://ukzrjclsfpovjhl2.onion/","http://m4dl3ztjlgvo7e3w.onion/","http://hackermyfnyubca5.onion/","http://7gsvzcjvupypvz66.onion/","http://mewchqgmqfe6zhnu.onion/","http://vkqebv44sobdpsom.onion/","http://llbsqyjysud7vjys.onion/"]

with open('forums_status4000-5000.csv', 'a') as csvfile:
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

