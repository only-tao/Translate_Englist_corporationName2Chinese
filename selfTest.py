# 所有的信息整合到了一个网址里，那么只需要对一个网站进行分析？！

from encodings import search_function
import re
import requests
from bs4 import BeautifulSoup
def getHtmltxt(url):
    try:
        # param = {
        # 'wd': kw
        # }
        head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        }
        r = requests.get(url,headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error in getHtmlTxt")
        return ''
def lline():
    print("****************************************")
def main():
    # keyWord = "Oceana Group Ltd 中文名"
    factoryname = "Ford Otomotiv Sanayi AS"
    keyWord = factoryname+" 公司中文名"
    # url = "https://www.baidu.com/s?wd="+keyWord  TODO 百度
    url = "https://cn.bing.com/search?q="+keyWord+"&PC=U316&FORM=CHROMN"
     
    # stockInfoUrl = 'http://fund.stockstar.com/funds/'
    # output_file = 'D:/BaiduStockInfo.csv'
    all_info = []
    lst = []
    html = getHtmltxt(url)
    # get the content id ="b_results" in html 
    soup = BeautifulSoup(html,'html.parser')
    # print(soup.prettify())
    search_ans_bing = soup.find_all('ol',id='b_results')
    # turn search_ans_bing into a string
    search_ans_bing = str(search_ans_bing)
    lline()
    print("search_ans_bing=>",search_ans_bing)
    # print(soup.find_all('ol',id='b_results'))
    # 找到公司,集团等名称的字段 使用正则表达式
    pattern = re.compile(r'.{1,4}[公司|集团|会社|有限|商].{1,4}')
    # str = "谁的>>>>sfee公司t><<<<<<<<est   海思集团，集团名字是什么??"
    model_s = search_ans_bing
    l_ans = pattern.findall(model_s)
    print("re result => ",l_ans) # or findall??
    # check  item in list chooselist whether in l_ans
    lst = []
    chooselist = ["公司","集团","会社","有限","商"]
    for i in l_ans:
        for item in chooselist:
            if item in i:
                lst.append(i)
                break
    lline()
    print("lst => ",lst)
    # 存储文件
    filename = keyWord+'.html'
    with open(filename, 'w', encoding='utf-8') as tem:
        tem.write(html)
    
    print(filename, '保存成功')
    # print(html)
    # getStockList(lst,html)
    # printList(lst,stockInfoUrl,output_file,all_info)
    #? 去除 \r \n ' '
#!!!!!!!!!!!!!!!!!!!!!! 注意执行main()!!!!!!!!!!!!!!!!!!!!!!
main()
    
