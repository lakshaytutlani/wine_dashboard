from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Wine'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

master_data = None

@app.route("/")
def main():
    return render_template('login.html')
    
    
@app.route("/dashboard")
def dashboard():
    
    conn = mysql.connect()
    cursor = conn.cursor ()
    sql = "select * from wine_data"
    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.commit()
    return render_template('dashboard.html',data=rows)    
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')    
 

@app.route('/logIn',methods=['POST','GET'])
def logIn():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            print _email
            print _password
            cursor.callproc('sp_checkUser',(_email,_password))
            data = cursor.fetchall()
            master_data = data
            
            if str(data[0][0]) == "Enter correct Username/Password !!":
                cursor.close() 
                conn.close()
                return json.dumps({'error':str(data[0])})
            else:
                conn.commit()
                cursor.close() 
                conn.close()                
                return json.dumps({'message':'Loading.......'})            
                
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
 
    
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()
            
            if len(data) is 0:
                conn.commit()
                cursor.close() 
                conn.close()                
                return json.dumps({'message':'success'})
            else:
                cursor.close() 
                conn.close()
                return json.dumps({'error':str(data[0])})
                
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})


if __name__ == "__main__":
    app.run()    