# -*- coding: utf-8 -*-

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import pandas as pd
import queue
import threading


class Paper:
    def __init__(self, title, author, journal, date, abstract, keywords, 
                 KnowledgeNetLink, downloadCnt):
        self.title = title
        self.author = author
        self.journal = journal
        self.date = date
        self.abstract = abstract
        self.keywords = keywords
        self.KnowledgeNetLink = KnowledgeNetLink
        self.downloadCnt = downloadCnt


# 关键字搜索得到的页面
def get_search_html(key_word, search_type, language_type):
    # 访问知网网站
    url = 'https://www.cnki.net/'
    driver.get(url)
    
    print('[+] 正在输入关键词 %s' % key_word)
    # 输入关键字
    driver.find_element(By.ID,"txt_SearchText").send_keys(key_word)
    
    # 默认选择主题
    if search_type == 'TKA': # 选择篇关摘
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[2]').click()
    elif search_type == 'KY': # 选择关键词
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[3]').click()
    elif search_type == 'TI': # 选择篇名
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[4]').click()
    elif search_type == 'FT': # 选择全文
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[5]').click()
    elif search_type == 'AU': # 选择作者
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[6]').click()
    elif search_type == 'FI': # 选择第一作者
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[7]').click()
    elif search_type == 'RP': # 选择通讯作者
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[8]').click()
    elif search_type == 'AF': # 选择作者单位
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[9]').click()
    elif search_type == 'FU': # 选择基金
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[10]').click()
    elif search_type == 'AB': # 选择摘要
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[11]').click()
    elif search_type == 'CO': # 选择小标题
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[12]').click()
    elif search_type == 'RF': # 选择参考文献
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[13]').click()
    elif search_type == 'CLC': # 选择分类号
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[14]').click()
    elif search_type == 'LY': # 选择文献来源
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[15]').click()
    elif search_type == 'DOI': # 选择DOI
        driver.find_element(By.XPATH,'//*[@id="DBFieldBox"]/div[1]').click()
        driver.find_element(By.XPATH,'//*[@id="DBFieldList"]/ul/li[16]').click()
    
    # 点击搜索按钮
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[1]/input[2]").click()
    print('[*] Crawler is beginning......')
    
    # 选择中英文
    time.sleep(1)
    if language_type == 'ch':
        driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/div/div/div/a[1]").click()
    elif language_type == 'en':
        driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/div/div/div/a[2]").click()
    else:
        driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/div/div/a").click()
    
    # 选择范围：学术期刊
    xsqk = driver.find_element(By.XPATH,'//div[@class="top-doctype"]/div/ul[1]/li[1]/a')
    driver.execute_script("arguments[0].click();", xsqk)
    
    # 显示详情
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="DivDisplayMode"]/li[1]').click()
    
    time.sleep(2)
    
    return driver.page_source


# 获取一篇论文的信息
def get_one_paper_data(soup):
    # 题目
    title = soup.select('.middle > h6 > a')[0].get_text().strip() 
    
    # 作者
    author = ''
    try:
        author = soup.select('.authorinfo > p > a')[0].get_text().strip()
        other_authors = soup.select('.authorinfo > div > p > a')
        authors = author
        for i in other_authors:
            au = (i.text).strip()
            authors = authors + ';' + au
    except:
        authors = author
    
    # 期刊名
    journal = soup.select('.middle p.baseinfo span.journal')[0].get_text().strip() 
    try:
        journal_num = soup.select('.middle > p.baseinfo > span:nth-child(2)')[0].get_text().strip()
        journal = journal + '(' + journal_num + ')'
    except:
        journal = journal
    
    # 发表时间
    try:
        date = soup.select('.middle p.baseinfo span.date')[0].get_text().strip() 
    except:
        date = soup.select('.middle p.baseinfo span.pubdate')[0].get_text().strip()
    
    # 被引量
    try:
        KnowledgeNetLink = soup.select('.middle p.baseinfo span.opts-count a.KnowledgeNetLink')[0].get_text().strip() 
    except:
        KnowledgeNetLink = '0'
    
    # 下载量
    try:
        downloadCnt = soup.find('a', class_ = 'downloadCnt').get_text().strip() 
    except:
        downloadCnt = '0'
    
    # 摘要
    try:
        abstract = soup.select('.middle p.abstract')[0].get_text().strip() 
        abstract = abstract.replace('\n','').replace('摘要：','').replace(' ','')
    except:
        abstract = ''
    
    # 关键词
    try:
        keyword = soup.select('.middle p.keywords a.KnowledgeNetLink') 
        keywords = ''
        for i in keyword:
            key = (i.text).strip().replace('\n',' ')
            keywords = keywords + key + ';'
    except:
        keywords = ''
    
    paper = Paper(title, authors, journal, date, abstract,
                  keywords, KnowledgeNetLink, downloadCnt)
    
    return paper


# 判断是否打开了新标签
def new_pag(web):
    try:
        driver.switch_to.window(web.window_handles[1])
        return True
    except:
        return False


# 获取论文的简介页网址
def get_paper_url(num):
    xpath = '//*[@id="gridTable"]/dl/dd[' + str(num) + ']/div[2]/h6/a'
    driver.find_element(By.XPATH, xpath).click()
    
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    url = driver.current_url

    if new_pag(driver):
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        driver.switch_to.window(driver.window_handles[0])

    return url


# 判断是否存在重复数据
def check(title):
    data_list = []
    df = pd.read_csv(file_name)
    data_list = df["题目"]
    for i in data_list:
        if title == i:
            return True
    return False


# csv文件初始化
def csv_init():
    if not os.access(file_name, os.F_OK):
        #创建csv，初始化
        with open(file_name, "w", encoding="utf-8", newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([
                "题目",
                "作者",
                "期刊",
                "发表时间",
                "摘要",
                "关键词",
                "被引量",
                "下载量",
                "简介页"
            ])


# 获取数据
def get_data(html_source):
    # 获取搜索页的数据
    soup = BeautifulSoup(html_source, 'html.parser')
    items = soup.find_all('div',class_='middle')
    f = open(file_name, "a", encoding="utf-8", newline='')
    csvwriter = csv.writer(f)
    num = 0
    for i in items:
        paper = get_one_paper_data(i) 
        num += 1
        # 检查爬取是否重复
        if not check(paper.title):
            # 简介页网址
            paper_url = get_paper_url(num)
            # 向csv存入数据
            csvwriter.writerow([
                paper.title,
                paper.author,
                paper.journal,
                paper.date,
                paper.abstract,
                paper.keywords,
                paper.KnowledgeNetLink,
                paper.downloadCnt,
                paper_url
            ])
        else:
            continue
    f.close()
    

# 判断是否存在下一页
def Next_page(html_source):
    try:
        driver.find_element(By.XPATH,'//*[@id="PageNext"]').click()
        time.sleep(2)
        return driver.page_source
    except:
        print('不存在下一页')
        return False


# 采用多线程方式    
def mult_search(html_source, pages):
    # csv文件初始化
    csv_init()
    
    # 首页搜索内容
    print('[+] 正在爬取第 1 页内容......')
    get_data(html_source)
    time.sleep(2)
    
    # 页数大于等于2时采用多线程方式
    threads = []
    q = queue.Queue()
    # 判断是否继续下一页
    page_num = pages
    while page_num > 1:
        html_new = Next_page(html_source)
        if html_new:
            print('[+] 正在爬取第 %s 页内容......' %(pages - page_num + 2))
            threads.append(threading.Thread(target=get_data, args=(html_new,)))
        page_num -= 1
    for t in threads:
        q.put(t)
    while not q.empty():
        q.get().start()
    for t in threads:
        t.join()
    print('[*] Crawler is over!')


if __name__ == '__main__':
    # 创建浏览器操作对象
    driver = webdriver.Chrome('chromedriver.exe')
    # 最大化
    driver.maximize_window()
    # 设置隐形等待
    driver.implicitly_wait(20)
    
    #--------------------------------------------#
    # 指定关键词
    key_input = "python" #input("输入指定的关键词") 
    
    # 指定搜索方式
    # '':       默认选择主题
    # 'TKA':    选择篇关摘
    # 'KY':     选择关键词
    # 'TI':     选择篇名
    # 'FT':     选择全文
    # 'AU':     选择作者
    # 'FI':     选择第一作者
    # 'RP':     选择通讯作者
    # 'AF':     选择作者单位
    # 'FU':     选择基金
    # 'AB':     选择摘要
    # 'CO':     选择小标题
    # 'RF':     选择参考文献
    # 'CLC':    选择分类号
    # 'LY':     选择文献来源
    # 'DOI':    选择DOI
    search_type = '' 
    
    # 指定中英文
    # '':       总库
    # 'ch':     中文
    # 'en':     英文
    language_type = '' 
    
    # 设置文件名
    file_name = './result of ' + str(key_input) + '.csv'
    
    # 设置爬取页数(最少页数为1, 默认每页20条, 以相关度排序)
    pages = 2
    
    html_source = get_search_html(key_input, search_type, language_type)
    mult_search(html_source, pages)

    time.sleep(6)
    print('[-] 结束运行，关闭浏览器')
    # 关闭webdriver
    driver.quit()
