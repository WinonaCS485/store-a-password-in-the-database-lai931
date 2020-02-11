import pymysql.cursors
import hashlib, uuid



connection = pymysql.connect(host='mrbartucz.com',
                             user='gw2246fx',
                             password='9Astronaut',
                             db='gw2246fx',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        username = input("enter a username: ")
        password = input("enter a password: ")
        
        salt = uuid.uuid4().hex
        print("password + salt is: " + password + str(salt))
        hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

        print ("the hashed password is: ", hashed_password)
        
        sql = "INSERT INTO login_credentials (username, salt, hash) Values (%s, %s, %s)"
        to_sql = (username, salt, hashed_password)
        cursor.execute(sql, to_sql)
        connection.commit()
        
        #attempt to reauthenticate
        username2 = input("enter username again: ")
        password2 = input("enter password to log in: ")
        
        sql_query = "SELECT salt FROM login_credentials WHERE username LIKE %s"
        cursor.execute(sql_query, (username2))
        for result in cursor:
            salt2 = result['salt']
            #print(salt2)
            
        sql_query = "SELECT hash FROM login_credentials WHERE username LIKE %s"
        cursor.execute(sql_query, (username2))
        for result in cursor:
            hashServer = result['hash']
        
        #recreate hash using recent password and retreived salt
        hashed_password2 = hashlib.sha512((password2 + salt2).encode('utf-8')).hexdigest()
        print("the hashed password is: ", hashed_password2)
        
        if hashed_password2 == hashServer:
            print("the credentials match")
        else:
            print("the credentials do not match")
            
                
      
        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        # connection.commit()
        

finally:
    connection.close()



