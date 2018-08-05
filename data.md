{
"Category":类别/法规类别/条约分类/分类/合同分类/文书分类 STRING (NOT NULL),

"LawCategory":法规分类 STRING,

"Title":法律法规标题/标题/条约标题/中文标题/合同名称/文书标题 STRING(NOT NULL),

"TitleEn":法律法规英文标题 STRING,

"FullText":全文/中文全文 STRING(NOT NULL),

"DocumentNO":发文字号 STRING，

"Effectiveness":效力级别 [STRING,(STRING),...],

"IssueDepartment":发布部门/国家与国际组织/相关组织/官方合同 [STRING,(STRING),...],

"RatifyDepartment":批准部门 [STRING,(STRING),...],

"Timeliness":时效性 [STRING,(STRING),...],

"Kind":种类（条约种类）STRING,

"CLI":索引字号,

"law_change":法律变迁
}