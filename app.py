from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def getDatabaseConnection():
    """
    Establishes a connection to the SQLite database and sets the row factory to sqlite3.Row.

    Returns:
        sqlite3.Connection: Connection to the SQLite database.
    """
    con = sqlite3.connect('Remindful.db')
    con.row_factory = sqlite3.Row
    return con

@app.context_processor
def delete_reply():
    """
    Context processor for handling the deletion of replies.

    Returns:
        dict: Dictionary containing the 'delete_reply' function.
    """
    def delete_reply_func(reply_id):
        """
        Generates a URL for the delete_reply_action route with the specified reply_id.

        Args:
            reply_id (int): The ID of the reply to be deleted.

        Returns:
            str: URL for the delete_reply_action route.
        """
        return url_for('delete_reply_action', reply_id=reply_id)

    return {'delete_reply': delete_reply_func}

@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply_action(reply_id):
    """
    Handles the deletion of a reply.

    Args:
        reply_id (int): The ID of the reply to be deleted.

    Returns:
        redirect: Redirects to the 'reply' route for the associated post.
    """
    con = getDatabaseConnection()
    cur = con.cursor()

    # Retrieve the associated post_id for the reply_id
    cur.execute('SELECT post_id FROM Reply WHERE reply_id = ?', (reply_id,))
    post_id = cur.fetchone()

    # Delete the reply with the specified reply_id
    con.execute('DELETE FROM Reply WHERE reply_id = ?', (reply_id,))
    con.commit()
    con.close()

    # Redirect to the 'reply' route for the associated post
    return redirect(url_for('reply', post_id=post_id[0]))

@app.context_processor
def delete_post():
    """
    Context processor for handling the deletion of posts.

    Returns:
        dict: Dictionary containing the 'delete_post' function.
    """
    def delete_post_func(post_id):
        """
        Generates a URL for the delete_post_action route with the specified post_id.

        Args:
            post_id (int): The ID of the post to be deleted.

        Returns:
            str: URL for the delete_post_action route.
        """
        return url_for('delete_post_action', post_id=post_id)

    return {'delete_post': delete_post_func}

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post_action(post_id):
    """
    Handles the deletion of a post.

    Args:
        post_id (int): The ID of the post to be deleted.

    Returns:
        redirect: Redirects to the 'view_posts' route.
    """
    con = getDatabaseConnection()

    # Delete the post with the specified post_id
    con.execute('DELETE FROM Posts WHERE post_id = ?', (post_id,))
    con.commit()
    con.close()

    # Redirect to the 'view_posts' route
    return redirect(url_for('view_posts'))

@app.route('/')
def index():
    """
    Renders the home page.

    Returns:
        render_template: Renders the 'index.html' template.
    """
    return render_template('index.html')

@app.route('/create_post', methods=('GET', 'POST'))
def create_post():
    """
    Handles the creation of a new post.

    Returns:
        redirect: Redirects to the 'view_posts' route after creating the post.
        render_template: Renders the 'create_post.html' template for GET requests.
    """
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
    
        cur = getDatabaseConnection()

        # Insert a new post into the 'Posts' table
        cur.execute('INSERT INTO Posts (title, description, first_name, last_name) VALUES (?,?,?,?)', 
                    (title, desc, firstName, lastName))
        
        cur.commit()
        cur.close()

        # Redirect to the 'view_posts' route after creating the post
        return redirect(url_for('view_posts'))

    # Render the 'create_post.html' template for GET requests
    return render_template('create_post.html')

@app.route('/reply/<int:post_id>', methods=('GET', 'POST'))
def reply(post_id):
    """
    Handles the viewing and replying to a post.

    Args:
        post_id (int): The ID of the post being viewed.

    Returns:
        render_template: Renders the 'reply.html' template with post and reply data.
        redirect: Redirects to the 'reply' route for the same post after submitting the reply.
    """
    conn = getDatabaseConnection()
    cursor = conn.cursor()

    if request.method == 'POST' and 'reply_content' in request.form:
        # If the form is submitted and 'reply_content' is present in the form data
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        reply_content = request.form['reply_content']

        # Insert a new reply into the 'Reply' table
        cursor.execute('INSERT INTO Reply (title, first_name, last_name, description, post_id) VALUES (?,?,?,?,?)',
                        (title, first_name, last_name, reply_content, post_id))
        conn.commit()
        conn.close()

        # Redirect to the 'reply' route for the same post after submitting the reply
        return redirect(url_for('reply', post_id=post_id))

    # Fetch the post details from the 'Posts' table
    cursor.execute('SELECT * FROM Posts WHERE post_id = ?', (post_id,))
    post = cursor.fetchone()

    # Fetch all replies for the specified post from the 'Reply' table
    cursor.execute('SELECT * FROM Reply WHERE post_id = ?', (post_id,))
    replys = cursor.fetchall()

    # Close the cursor and connection after fetching the data
    cursor.close()
    conn.close()

    # Render the 'reply.html' template with post and reply data
    return render_template('reply.html', post=post, replys=replys)

@app.route('/view_posts', methods=('GET', 'POST'))
def view_posts():
    """
    Handles the viewing of all posts.

    Returns:
        render_template: Renders the 'view_posts.html' template with the posts data.
        redirect: If the form is submitted, redirects to the 'reply' route for the selected post_id.
    """
    if request.method == 'POST':
        # If the form is submitted, redirect to the 'reply' route for the selected post_id
        post_id = request.form['post_id']
        return redirect(url_for('reply', post_id=post_id))

    # Fetch all posts from the 'Posts' table
    cur = getDatabaseConnection()
    posts = cur.execute('SELECT * FROM posts')

    # Render the 'view_posts.html' template with the posts data
    return render_template('view_posts.html', posts=posts)



    