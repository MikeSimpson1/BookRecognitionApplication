#Python connect to database / scrape images
import psycopg2
import urllib.request
import os
#establishing the connection
conn = psycopg2.connect(
   database="Library", user='postgres', password='postgres', host='127.0.0.1', port= '5433'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute('select * from public."Books"')

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)
for i in range(50):
    data = cursor.fetchone()
    fileName = data[0]+"-"+data[2].replace(':','').replace('?','').replace('/','').replace('"','').replace('\'','') +"-" +data[3] + ".jpg"
    try:
        file = urllib.request.urlopen(data[4])
        if (file.length > 500 and file.length != 44259):
            urllib.request.urlretrieve(data[4], 'C:/Users/Mike/Desktop/BookAppraisalApplication/BookCovers/'+fileName)
    except:
        print("An error has occurred. FileName: " + fileName)
#Closing the connection
conn.close()
