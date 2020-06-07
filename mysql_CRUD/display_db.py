import mysql.connector  
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password",database="dbpython")#established connection between your database  
mycursor=mysqldb.cursor()#cursor() method create a cursor object  
try:  
   mycursor.execute("select * from student")#Execute SQL Query to select all record   
   result=mycursor.fetchall() #fetches all the rows in a result set   
   for i in result:    
      roll=i[0]  
      name=i[1]  
      marks=i[2]  
      print(roll,name,marks)  
except:   
   print('Error:Unable to fetch data.')  
mysqldb.close()#Connection Close  
