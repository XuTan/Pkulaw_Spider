#### 1.中央法规司法解释 Db=chl menu_item=law
clust_param=
* 法律 0/XA01 clusterwhere:效力级别=XA01
* 行政法规 0/XC02 clusterwhere:效力级别=XC02 
* 司法解释 0/XG04 clusterwhere:效力级别=XG04
* 部门规章 0/XE03 clusterwhere: 效力级别=XE03
* 团体规定 0/XI05 clusterwhere: 效力级别=XI05
* 行业规定 0/XK06 clusterwhere: 效力级别=XK06
* 军事法规规章 0/XQ09 clusterwhere: 效力级别=XQ09
* 监察法规 (暂无)
#### 2.地方法规规章 Db=lar menu_item=law
clust_param=
* 地方性法规 0/XM07 clusterwhere: 效力级别=XM07
* 地方政府规章 0/XO08 clusterwhere: 效力级别=XO08
* 地方规范性文件 0/XP08 clusterwhere: 效力级别=XP08
* 地方司法文件 0/XP09 clusterwhere: 效力级别=XP09
* 地方工作文件 0/XP10 clusterwhere: 效力级别=XP10
* 行政许可复批 0/XP11 clusterwhere: 效力级别=XP11
#### 3.立法背景资料
##### 3.1立法草案 Db=protocol menu_item=lfbj_all
clust_param=
* 征求意见 3/091001 clusterwhere: 类别=091001
* 草案及其说明 3/091002 clusterwhere: 类别=091002
* 审议意见 3/091003 clusterwhere: 类别=091003
* 其他 3/091004 clusterwhere: 类别=091004
##### 3.2法规解读 Db=lawexplanation menu_item=lfbj_all
clust_param=
* 问答 3/093001 clusterwhere: 类别=093001
* 解读 3/093002 clusterwhere: 类别=093002
* 理解与适用 3/093003 clusterwhere: 类别=093003
* 其他 3/093004 clusterwhere: 类别=093004
##### 3.3白皮书 Db=protocol menu_item=lfbj_all
clust_db:whitebook
##### 3.4工作报告 Db=workreport menu_item=lfbj_all
clust_param=
* 全国人大常委会工作报告 1/090001 clusterwhere: 类别=090001
* 全国人大常委会执法检查 1/090002 clusterwhere: 类别=090002
* 国务院政府工作报告 1/090003 clusterwhere: 类别=090003
* 最高人民法院工作报告 1/090004 clusterwhere: 类别=090004
* 最高人民检察院工作报告 1/090005 clusterwhere: 类别=090005
* 地方政府工作报告 1/090006 clusterwhere: 类别=090006
##### 3.5机构简介 Db=protocol menu_item=lfbj_all
clust_db:introduction
#### 4.台湾法律法规 Db=twd menu_item=law
Search_Mode:accurate
#### 5.港澳法律法规 Db=hkd,aom menu_item=hkd_aom
Search_Mode:accurate
##### 5.1香港法律法规 clust_db:hkd
##### 5.2澳门法律法规 clust_db:aom
#### 6.外国法律法规 Db=iel menu_item=law
Search_Mode: accurate
#### 7.中外条约 Db=eagn menu_item=law
Search_Mode: accurate
#### 8.合同范本 Db=con menu_item=con_fmt
##### 8.1 合同范本 
Search_Mode: accurate

clust_param=
* 官方合同 1/#1% clusterwhere: 发布部门=#2%
* 非官方合同 2/#2% clusterwhere: 发布部门=data()
##### 8.2 法律文书样式
clust_param=
* 公安刑事文书 0/001001 clusterwhere: 文书分类=001001
* 检察文书 0/001002 clusterwhere: 文书分类=001002
* 法律文书 0/001003 clusterwhere: 文书分类=001003
* 监狱文书 0/002001 clusterwhere: 文书分类=002001
* 行政机关文书 0/002002 clusterwhere: 文书分类=002002
* 仲裁文书 0/002003 clusterwhere: 文书分类=002003
* 公证文书 0/002004 clusterwhere: 文书分类=002004
* 律师诉讼文书 0/002005 clusterwhere: 文书分类=002005
* 企业法律文书 0/002006 clusterwhere: 文书分类=002006
* 国家赔偿文书 0/002007 clusterwhere: 文书分类=002007
* 其他团体组织文书 0/002008 clusterwhere: 文书分类=002008
#### 9.法律动态 Db=news menu_item=law
orderby: 提交日期