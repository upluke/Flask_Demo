# request, represents web requests, helps access to the query string inside of "request.args[...]"
from flask import Flask, request, render_template
# Get the debugging tool on the right side of the page, but this is only going to work on pages, where we have a template involved
# for example, if it's not responding with an HTML file or template, it's a string of HTML
from flask_debugtoolbar import DebugToolbarExtension
from random import choice, randint
# instantiate a new application object and takes in the dunder name (__name__)
app = Flask(__name__)
# Later, when we talk about security & deployment, we’ll talk about when and how to actually keep this secret.
app.config['SECRET_KEY'] = "dumbonudumb"

debug = DebugToolbarExtension(app)
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


@app.route('/form')
def show_form():
    return render_template("form.html")


COMPLIMENTS = ["cool", "clever", "tenacious", "awesome", "Pythonic"]


@app.route('/greet')
def get_greeting():
    # get something from the query string is through this request object, object.args, which is a data structure that is similar
    # to a dictionary where we can use a key to get a value out. And the key is goning to be "username" in this case
    username = request.args["username"]
    # pick a random compliment
    nice_thing = choice(COMPLIMENTS)
    # an then we'll pass the two variables to our template called "greet.html"
    return render_template("greet.html", username=username, compliment=nice_thing)


# Jinja will replace things like {{msg}} with value of msg passed when rendering:
# here lucky_num will be passed to the lucky.html


@app.route('/lucky')
def lucky_number():
    num = randint(1, 10)
    return render_template("lucky.html", lucky_num=num, msg="You are so lucky!!")


@app.route('/hello')
def say_hello():
    return render_template("hello.html")

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


@app.route("/products/<category>/<int:product_id>")
def product_detail(category, product_id):
    """Show detail page for product."""
    return f"<h1>Viewing the product with id: {product_id} from the category: {category}</h1>"


# Query Params vs URL Params
# http://toys.com/shop/spinning-top?color=red
# URL Parameter                                   Query Parameter
# /shop/<toy>                                     /shop?toy=elmo
# Feels more like “subject of page”               Feels more like “extra info about page”
#                                                 Often used when coming from form


@app.route("/shop/<toy>")
def toy_detail(toy):
    """Show detail about a toy."""

    # Get color from req.args, falling back to None
    color = request.args.get("color")

    return f"<h1>{toy}</h1>Color: {color}"

# finished jinija condtion
