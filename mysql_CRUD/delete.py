import mysql.connector   
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password",database="dbpython")#established connection between your database  
mycursor=mysqldb.cursor()#cursor() method create a cursor object   
try:   
   mycursor.execute("DELETE FROM student WHERE roll=3")#Execute SQL Query to detete a record   
   mysqldb.commit() # Commit is used for your changes in the database  
   print('Record deteted successfully...')  
except:  
   # rollback used for if any error  
   mysqldb.rollback()  
mysqldb.close()#Connection Close  
