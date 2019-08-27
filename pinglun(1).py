# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 09:14:40 2019

@author: Administrator
"""

from selenium import webdriver
from pyquery import PyQuery as pq
import csv

browser = webdriver.Chrome()

def get_source_page(cartype,page):
    url = 'https://k.autohome.com.cn/'+str(cartype)+'/'+'index_'+str(page)+'.html?#dataList'
    browser.get(url)
    return browser.page_source

def get_num(source):
    doc = pq(source)
    pag = doc('.page-item-info').text()[1:-1]
    return pag   

def parse_page(content,cartype):
    doc = pq(content)
    all = doc('.mouthcon').items()
    for item in all:
        yield{  'car':cartype,
                'name':item.find('.name-text').text(),
                'evaluation':item.find('.choose-dl .fn-clear').text()
                }

def save_to_csv(dics):
    with open('C:/Users/Administrator/Desktop/evaluation/eva.csv','a',encoding='GB18030',newline='') as csvfile:
        fieldnames = ['car','name','evaluation']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow(dics)

def main():
    for (cartype,order) in [('2886',263),('314',289),('1007',137)]:
        for page in range(order):
            a = get_source_page(cartype,page)
            b = parse_page(a,cartype)
            for item in b:
                save_to_csv(item)
        
        

            
if __name__ == '__main__':
    main()
    
    
'''    
source = get_source_page(cartype,2)
        pag = get_num(source)
        pagecout = pagecout.append(pag)
        pagecout = [205,504,1362,356]
        pagecout = [205,504,1362,356]
        
'''
###数据处理的部分
import pandas as pd

path='E:/崔庆才爬虫课程/evaluation1.csv'
data = pd.read_csv(path, sep=",",encoding="UTF-8",header=None,names=['车型','用户','买车目的'])
data.info()
data.head()
data['车型'].replace({2886:'K3',3959:'领动',448:'轩逸',526:'卡罗拉',364:'福克斯',3954:'KX5',358:'途胜',314:'CR-V',1007:'IX35',4235:'探界者'},inplace=True)
data

data['买车目的'].str.split('\n', expand=True).stack()
data['买车目的'].str.split('\n', expand=True).stack().reset_index(level=1, drop=True).rename('买车目的')
data1=data.drop('买车目的', axis=1).join(data['买车目的'].str.split('\n', expand=True).stack().reset_index(level=1, drop=True).rename('买车目的'))

data1.head(20)

data2 = data1.groupby(['车型','买车目的'])['买车目的'].count()
data2


###如何求取数据透视表的分组占比
data1=data.drop('买车目的', axis=1).join(data['买车目的'].str.split('\n', expand=True).stack().reset_index(level=1, drop=True).rename('买车目的'))

table = pd.pivot_table(data1, index=['车型','买车目的'],aggfunc='count')

table2=data1.groupby('车型')['用户'].count()

table3 = pd.merge(table,table2,on='车型')

table3.index=table.index

table3.columns = ['分列','组和']

table3['total'] = table3.apply(lambda x:round(x[0]/x[1],4)*100,axis=1)
table3

table3.to_csv(path)






data2.columns = ['车型','买车目的','数量统计']


data.to_csv('C:/Users/Administrator/Desktop/evaluation/evaluation.csv')


























