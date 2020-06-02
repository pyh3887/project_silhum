from django.shortcuts import render
import MySQLdb
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt 

plt.rc('font',family='malgun gothic')   #한글 깨짐 방지.
plt.rcParams['axes.unicode_minus'] = False   # -부호 깨짐 방지
config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}




def mainFunc(request):   
    conn = MySQLdb.connect(**config)
    
    cursor = conn.cursor()
    
    sql = '''
    select jikwon_no,jikwon_name,buser_name,jikwon_jik,jikwon_pay from jikwon inner join buser on buser_num = buser_no
    '''
    cursor.execute(sql)
    df2 = pd.read_sql(sql,conn)
    df2.columns = ('번호','이름','부서','직급','연봉')
    
    print(df2.head(3))
    print()
    print(df2['직급'].value_counts())
    print(df2.loc[:,['연봉']].mean())
    jik_ysum = df2.groupby(['직급'])['연봉'].sum()
    jik_ymean = df2.groupby(['직급'])['연봉'].mean()
    
    jik_ysum2 = df2.groupby(['부서'])['연봉'].sum()
    jik_ymean2 = df2.groupby(['부서'])['연봉'].mean()
    
    #data['평균'] = pd.DataFrame([jik_ymean,jik_ysum] , columns=['연봉합','연봉평균'])
    
    #print(data)
    
    df3 = pd.DataFrame(jik_ysum)
    df4 = pd.DataFrame(jik_ymean)
    df5 = pd.DataFrame(jik_ysum2)
    df6 = pd.DataFrame(jik_ymean2) 
    
    
    plt.subplot(3,3,1)
    plt.bar(jik_ysum.index,jik_ysum.values)
    plt.title('직급 합')
    plt.subplot(3,3,3)
    plt.bar(jik_ymean.index,jik_ymean)
    plt.title('직급  평균')
    plt.subplot(3,3,7)
    plt.bar(jik_ysum2.index,jik_ysum2)
    plt.title('부서별 합')
    plt.subplot(3,3,9)
    plt.bar(jik_ymean2.index,jik_ymean2)
    plt.title('부서별 평균')
    #plt.show()
    
    fig = plt.gcf() #차트를 이미지로 저장 준비
    
    
    
    plt.savefig('C:/work/py_sou/django_ex_graph/myapp/static/image/aaa.png')
    
    return render(request,'list.html',{'y': df2.to_html(),'jikhap': df3.to_html(),'jikmean': df4.to_html(),
                                       'buhap': df5.to_html(),'bumean':df6.to_html()})