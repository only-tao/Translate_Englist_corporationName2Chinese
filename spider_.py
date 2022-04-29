# 所有的信息整合到了一个网址里，那么只需要对一个网站进行分析？！
import re
import requests
from bs4 import BeautifulSoup
def getHtmltxt(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error in getHtmlTxt")
        return ''
def getStockList(lst,html): #lst存储，通过html，regex 页面查找需要的信息 
    # 获取all stock's code
    # 得到所有的a
    soup = BeautifulSoup(html,"html.parser")
    tbodyStr = soup.find_all('tbody')
    # print(tbodyStr)#good
    alist = tbodyStr[0].find_all('a')#find all <a>....</a>
    # tbodyStr 因为是一个list 因此要用[0]，(只有一个元素)
    # print(type(alist[0]))  alist[0] 是一个bs tag 类型!!!
    #todo 解决重复问题!
    for i in range(len(alist)):
        if i%2 == 0:
            href = alist[i].attrs['href']
            lst.append(re.findall(r'\d{6}',href)[0])
    # lst = list(set(lst))
    print(len(lst))
def printList(lst,stockInfoUrl,output_file,all_info):#lst 是所有的stock的 code ['111223','344554','234533','563463']  type(lst[0]) -> str
    template = "{:3}\t{:10}\t{:10}\t{:6}\t{:6}"
    print(template.format("序号","代码","名称","净值","累计净值"))
    for i in range(len(lst)):
        allUrl = stockInfoUrl + lst[i] + ".shtml" # 访问的网址
        html = getHtmltxt(allUrl)
        # 接下来从网址中获取每一只股票的信息
        # name code 净值 累计净值 使用list 存储
        # 找到 class: trscontent
        soup = BeautifulSoup(html,"html.parser")
        divTag = soup.find('div',attrs={'class':'trscontent'})#attention the type
        # find h1
        nametxt = soup.find('h1').text.strip()
        # print(nametxt)
        netWorth = soup.find('em').text.strip()
        #累计净值 使用 re 获取
        netWorth_add = re.findall(r'累计净值：[\d\.]*',divTag.text)#return str
        all_info.append([i,lst[i],nametxt,netWorth,netWorth_add[0].split('：')[1]])

        item = all_info[i]
        print(template.format(item[0],item[1],item[2],item[3],item[4]))
        fpath = output_file 
        with open(fpath, 'a', encoding='gb2312') as f:#good  a 追加写
            s=''
            for i in item:
                s = s+str(i)+',' 
            f.write(s[:-1]+'\r')
def main():
    url = "http://quote.stockstar.com/fund/stock_3_1_1.html"
    #   http://fund.stockstar.com/funds/920002.shtml
    stockInfoUrl = 'http://fund.stockstar.com/funds/'
    output_file = 'D:/BaiduStockInfo.csv'
    all_info = []
    lst = []
    html = getHtmltxt(url)
    getStockList(lst,html)
    printList(lst,stockInfoUrl,output_file,all_info)
    #? 去除 \r \n ' '
#!!!!!!!!!!!!!!!!!!!!!! 注意执行main()!!!!!!!!!!!!!!!!!!!!!!
main()
    
