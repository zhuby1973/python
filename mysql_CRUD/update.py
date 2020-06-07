import mysql.connector  
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password",database="dbpython")#established connection between your database  
mycursor=mysqldb.cursor()#cursor() method create a cursor object  
try:  
   mycursor.execute("UPDATE student SET name='Ramu', marks=100 WHERE roll=1")#Execute SQL Query to update record
   mysqldb.commit() # Commit is used for your changes in the database  
   print('Record updated successfully...')   
except:   
   # rollback used for if any error  
   mysqldb.rollback()  
mysqldb.close()#Connection Close  
