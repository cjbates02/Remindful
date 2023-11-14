from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3

app = Flask(__name__)

def getDatabaseConnection():
    con = sqlite3.connect('Remindful.db')
    con.row_factory = sqlite3.Row
    return con

@app.context_processor
def delete_reply():
    def delete_reply_func(reply_id):
        return url_for('delete_reply_action', reply_id=reply_id)

    return {'delete_reply': delete_reply_func}

@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply_action(reply_id):
    con = getDatabaseConnection()
    cur = con.cursor()
    cur.execute('SELECT post_id FROM Reply WHERE reply_id = ?', (reply_id,))
    post_id = cur.fetchone()
    con.execute('DELETE FROM Reply WHERE reply_id = ?', (reply_id,))
    con.commit()
    con.close()
    return redirect(url_for('reply', post_id=post_id[0]))


@app.context_processor
def delete_post():
    def delete_post_func(post_id):
        return url_for('delete_post_action', post_id=post_id)

    return {'delete_post': delete_post_func}

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post_action(post_id):
    con = getDatabaseConnection()
    con.execute('DELETE FROM Posts WHERE post_id = ?', (post_id,))
    con.commit()
    con.close()
    return redirect(url_for('view_posts'))

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

        return redirect(url_for('view_posts'))

    return render_template('create_post.html')

@app.route('/reply/<int:post_id>', methods=('GET', 'POST'))
def reply(post_id):
    conn = getDatabaseConnection()
    cursor = conn.cursor()

    if request.method == 'POST' and 'reply_content' in request.form:
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        reply_content = request.form['reply_content']

        cursor.execute('INSERT INTO Reply (title, first_name, last_name, description, post_id) VALUES (?,?,?,?,?)',
                        (title, first_name, last_name, reply_content, post_id))
        conn.commit()
        conn.close()

        return redirect(url_for('reply', post_id=post_id))

    
    # Use fetchone() to retrieve the data
    cursor.execute('SELECT * FROM Posts WHERE post_id = ?', (post_id,))
    post = cursor.fetchone()

    cursor.execute('SELECT * FROM Reply WHERE post_id = ?', (post_id,))
    replys = cursor.fetchall()

    # Close the cursor and connection after fetching the data
    cursor.close()
    conn.close()
    return render_template('reply.html', post=post, replys=replys)

@app.route('/view_posts', methods=('GET', 'POST'))
def view_posts():
    if request.method == 'POST':
        post_id = request.form['post_id']
        return redirect(url_for('reply', post_id=post_id))
    cur = getDatabaseConnection()
    posts = cur.execute('SELECT * FROM posts')

    return render_template('view_posts.html', posts=posts)


    