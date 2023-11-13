from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3

app = Flask(__name__)

def getDatabaseConnection():
    con = sqlite3.connect('Remindful.db')
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_post', methods=('GET','POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
    
        cur = getDatabaseConnection()
        cur.execute('INSERT INTO Posts (title, description, first_name, last_name) VALUES (?,?,?,?)', 
                    (title, desc, firstName, lastName))
        
        cur.commit()
        cur.close()

        return redirect(url_for('index'))

    return render_template('create_post.html')