from firebase import firebase
import datetime
from example_enroll import enroll_students  
from example_search import search_students
import os
from flask import Flask, render_template, redirect, jsonify, request

app = Flask(__name__)
app.debug = True
firebase = firebase.FirebaseApplication('https://attendance-system-51f12.firebaseio.com/', None)  


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    

@app.route('/')
def root():
    return redirect("/index"), 302


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', data='')


@app.route('/index', methods=['POST'])
def index_post():
    print(request.data)
    hash_val = enroll_students();
    if hash_val:
        data =  { 'Name': request.form['name'],  
          'uuid': hash_val,  
          'TP': '018574'  
          }  
        result = firebase.post('/users/',data)  
        print(result)  

    return render_template('index.html', data='')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html', data=str(e)), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error-404.html', data=str(e)), 405



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# hash_val = search_students();

# if hash_val:
#     firebase = firebase.FirebaseApplication('https://attendance-system-51f12.firebaseio.com/', None)  
#     data =  { 'name': 'Vivek',  
#           'hash': hash_val,  
#           'time': datetime.datetime.now(),
#           'subject': 'Bangla',
#           'room_no': '01'  
#           }  
#     result = firebase.post('/attendance/',data)  
#     print(result)  



# hash_val = enroll_students();

# print(hash_val)

# firebase = firebase.FirebaseApplication('https://attendance-system-51f12.firebaseio.com/', None)  
# data =  { 'Name': 'Vivek',  
#           'RollNo': hash_val,  
#           'Percentage': 76.02  
#           }  
# result = firebase.post('/users/',data)  
# print(result)  


# result = firebase.get('/users', '')  
# print(result) 
