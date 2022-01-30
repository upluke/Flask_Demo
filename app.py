# request, represents web requests, helps access to the query string inside of "request.args[...]"
from flask import Flask, request
# instantiate a new application object and takes in the dunder name (__name__)
app = Flask(__name__)

# a decorator expecting a funciton to come right after this line
# listen for a request to '/', when that happens then call the following funciton


@app.route('/')
def index():
    """Show homepage"""
    # this returned string will be used to construct a full HTTP response
    return """
      <html>
        <body>
          <h1>I am the landing page</h1>
        </body>
      </html>
      """


@app.route('/hello')
def say_hello():
    return """
      <html>
        <body>
          <h1>I am a hello page</h1>
          <a href='/'>Go to home page</a>
        </body>
      </html>
    """

# Handling Query Arguments
# request.args is a dict-like object of query parameters.


@app.route("/search")
def search():
    """Handle GET requests like /search?term=fun&sort=new"""
    # extrating data in a GET request from query string using request.args
    term = request.args["term"]
    sort = request.args["sort"]
    return f"<h1>Searching for {term} </h1> <p>Sorting by: {sort} </p> "


# Handling POST Requests


# This route is responding to GET requests
# To accept POST requests, must specify that: methods=["POST"]

@app.route("/add-comment")
def add_comment_form():
    """Show form for adding a comment."""
    # the name attribute will be used to store the value from this input when it's sent to the server
    return """
      <form method="POST">
        <input text="text" placeholder="comment" name="comment">
         <input text="text" placeholder="username" name="username">
        <button>Submit</button>
      </form>
      """

# This route following is responding to POST requests
# and extracting the form data from the above POST requests that is sent
# request.form is a dict-like object of POST parameters.


@app.route("/add-comment", methods=["POST"])
def add_comment():
    """Handle adding comment."""
    print(
        request.form)  # ImmutableMultiDict([('comment', 'Yolo'), ('username', 'bobo')])
    comment = request.form["comment"]
    username = request.form["username"]
    return f"""
        <h1>SAVED YOUR COMMENT</h1>
        <ul>
            <li>Username: {username}</li>
            <li>Comment: {comment}</li>
        </ul>
    
    """


# Variables in a URL
# Argument capture in Flask:
USERS = {
    "whiskey": "Whiskey The Dog",
    "spike": "Spike The Porcupine",
}

# when we declare a route with a path variable in it (with those braces on either side),
# whatever name we put inside those braces is going to be used to pass an argument of that same name,
# to our view function/handler, show_user_profile, in this case, so we need to add in a parameter
# that matches it exactly


@app.route('/user/<username>')
def show_user_profile(username):  # matching parameter:username
    """Show user profile for user."""

    name = USERS[username]
    return f"<h1>Profile for {name}</h1>"


# Converts to integer when calling function:

POSTS = {
    1: "I like mayo!",
    2: "I hate double rainbow",
    3: "YOLO"
}


@app.route('/posts/<int:id>')
def find_post(id):
    # post = POSTS[id]
    post = POSTS.get(id, "Post not found")
    return f"<p>{post}</p>"

# Can have more variable:
