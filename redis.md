#### 1.bz338 登录状态 db=0
* key = {"username":username,"password":password} | DICT

  value = Cookie | STRING

eg:{'username': 'xxtp', 'password': 'metasota'}: 'safedog-flow-item=;esybrmlauth=8484b880206e6aeb6ebff73b3f410dba;esybrmlgroupid=10;esybrmlrnd=jSoyxBZ2DvFrvilUQeaF;esybrmluserid=27187;esybrmlusername=xxtp'

#### 2.各个入口 登录状态 db=1
* key = PORT_URL | STRING

  value = Cookie | STRING
  
eg:'http://202.121.166.131:9155/cluster_call_form.aspx?menu_item=law&EncodingName=&key_word=':'SSLHTTPSESSIONID=wRidkvqM4VIKv1j;CheckIPAuto=0;CheckIPDate=2018-07-25 15:13:50;CookieId=majpbtdc2nigf2iii4jdm30h;User_User=%bb%aa%b6%ab%d5%fe%b7%a8%b4%f3%d1%a7;majpbtdc2nigf2iii4jdm30hisIPlogin=1;SSLHTTPSESSIONID=12ItIzKQ7RcgM2a'

#### 3.各个条文子类 重要参数 db=2
* key = {"Db": Db, "menu_item": menu_item, "clusterwhere": clusterwhere} | DICT

  value = [{"title": title, "href": href},{},{}......] | LIST
  
eg:{'Db': 'chl', 'menu_item': 'law', 'clusterwhere': '效力级别=XG04'}:[{'title': '最高人民法院关于适用《中华人民共和国民法总则》诉讼时效制度若干问题的解释', 'href': 'fulltext_form.aspx?Db=chl&Gid=333748837754f250bdfb&keyword=&EncodingName=&Search_Mode=&Search_IsTitle=0'},{},{}......]

