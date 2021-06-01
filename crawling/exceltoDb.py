import openpyxl
import mysql.connector
import os
import sys

result = []

#wb = openpyxl.load_workbook("DeepSearch-hc-news-2021-04-24-2021-05-24-20210524-235718.xlsx")
wb = openpyxl.load_workbook("DeepSearch-ec-news-2021-04-24-2021-05-24-20210524-235653.xlsx")
ws = wb.worksheets[1]

db = mysql.connector.connect(
		host="vi-eco.cecgsm74tces.ap-northeast-2.rds.amazonaws.com",
		user="admin",
		passwd="1q2w3e4r",
		database="vi_eco"
	)

tmp_data = []

for r in ws.rows:
    date = r[0].value
    category = r[1].value
    section = r[2].value
    publisher = r[3].value
    author = r[4].value
    title = r[5].value
    content_url = r[6].value

    url = content_url.split('"')

    if len(url)<2 :
        tmp_data = []
        continue

    if author == None :
        author = "undefined"

    
    tmp_data.append(date)
    tmp_data.append(category)
    tmp_data.append(section)
    tmp_data.append(publisher)
    tmp_data.append(author)
    tmp_data.append(title)
    tmp_data.append(url[1])

    if len(tmp_data) == 7:
        result.append(tuple(tmp_data))
        #print(result)
        tmp_data = []

try:
    cursor = db.cursor()
    sql = "INSERT INTO ec_news(date,category,section,publisher,author,title,url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql,result)
    db.commit()
    print("[+] Insertion success\n")
    
except Exception as e:
    print(e)
    print("[ERROR] Insertion failed\n")

finally:
    db.close()