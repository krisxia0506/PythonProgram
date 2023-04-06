import re
from urllib.request import urlopen
html='''

    <tr class="firstRow" style="height:34px">
     <td width="131" style="padding:0px 7px;border:1px solid;background-color:transparent" rowspan="6"><p style="text-align:center"><span style="font-family:'宋体';font-size:16px"><img width="420" height="570" src="/pub/jsjxy/images/955dad48a63d42c0815191757f722646.JPG"></span></p></td>
     <td width="143" style="border-width:1px 1px 1px 0px;border-style:solid solid solid none;border-color:rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">姓名</span></p></td>
     <td width="274" style="border-width:1px 1px 1px 0px;border-style:solid solid solid none;border-color:rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">王贺祥</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="143" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">职称</span></p></td>
     <td width="274" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">助教</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="143" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">学位</span></p></td>
     <td width="274" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">学士</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="143" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">研究方向</span></p></td>
     <td width="274" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><br></td>
    </tr>
    <tr style="height:34px">
     <td width="143" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">所在系教研室</span></p></td>
     <td width="274" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">实验室</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="143" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:left"><span style="font-family:'等线'">邮箱</span></p></td>
     <td width="274" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">563138421@QQ.COM</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="131" style="border-width:0px 1px 1px;border-style:none solid solid;border-color:rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">教育背景</span></p></td>
     <td width="417" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent" colspan="2"><p style="text-align:center"><span style="font-family:'等线'">华北科技学院，法学本科，2010</span></p></td>
    </tr>
    <tr style="height:34px">
     <td width="131" style="border-width:0px 1px 1px;border-style:none solid solid;border-color:rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent"><p style="text-align:center"><span style="font-family:'等线'">个人简介</span></p></td>
     <td width="417" style="border-width:0px 1px 1px 0px;border-style:none solid solid none;border-color:rgb( 0 , 0 , 0 ) rgb( 0 , 0 , 0 );padding:0px 7px;background-color:transparent" colspan="2"><br></td>
    </tr>
   </tbody>
'''
name=''
title=''
degree=''
research_interests=''
department=''
email=''
education=''
bio=''
try:
    name = re.findall(r'<td.*?><p.*?><span.*?>姓名</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    title = re.findall(r'<td.*?><p.*?><span.*?>职称</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    degree = re.findall(r'<td.*?><p.*?><span.*?>学位</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    research_interests = re.findall(r'<td.*?><p.*?><span.*?>研究方向</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    department = re.findall(r'<td.*?><p.*?><span.*?>所在系教研室</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    email = re.findall(r'<td.*?><p.*?><span.*?>邮箱</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)[0]
except:
    pass
try:
    education = re.findall(r'<td.*?><p.*?><span.*?>教育背景</span></p></td>\s*<td.*?><p.*?><span.*?>(.*?)</span></p></td>', html)
except:
    pass
try:
    bio = re.findall(r'个人简介</span> \n <[^>]+>([^<]+)</[^>]+>', html)
except:
    pass

# 将提取的信息存储在一个Python字典中
data = {
    '姓名': name,
    '职称': title,
    '学位': degree,
    '研究方向': research_interests,
    '所在系教研室': department,
    '邮箱': email,
    '教育背景': education,
    # '个人简介': bio
}

print(data)  # 打印字典
