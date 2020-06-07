import mysql.connector #Importing Connector package   
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password")#established connection   
mycursor=mysqldb.cursor()#cursor() method create a cursor object  
mycursor.execute("create database dbpython")#Execute SQL Query to create a database    
mysqldb.close()#Connection Close  

#Create a table into dbpython database  
import mysql.connector  
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password",database="dbpython")#established connection between your database   
mycursor=mysqldb.cursor()#cursor() method create a cursor object  
mycursor.execute("create table student(roll INT,name VARCHAR(255), marks INT)")#Execute SQL Query to create a table into your database  
mysqldb.close()#Connection Close  

import mysql.connector  
mysqldb=mysql.connector.connect(host="localhost",user="root",password="password",database="dbpython")#established connection between your database  
mycursor=mysqldb.cursor()#cursor() method create a cursor object    
try:  
   #Execute SQL Query to insert record  
   mycursor.execute("insert into student values(1,'Sarfaraj',80),(2,'Kumar',89),(3,'Sohan',90)")  
   mysqldb.commit() # Commit is used for your changes in the database  
   print('Record inserted successfully...')   
except:  
   # rollback used for if any error   
   mysqldb.rollback()  
mysqldb.close()#Connection Close  
