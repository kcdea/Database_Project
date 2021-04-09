import cx_Oracle

# Put your own CISE username and password here.
# On future commits make sure you don't make this file visible to others.
username = ''
password = ''
dsn = cx_Oracle.makedsn("oracle.cise.ufl.edu", "1521", "orcl")
encoding = 'UTF-8'