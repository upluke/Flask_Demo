# First we import the Flask class. An instance of this class will be our WSGI application.
# request, represents web requests, helps access to the query string inside of "request.args[...]"
from crypt import methods
from flask import Flask, request, render_template, redirect, flash, jsonify
# Get the debugging tool on the right side of the page, but this is only going to work on pages, where we have a template involved
# for example, if it's not responding with an HTML file or template, it's a string of HTML
from flask_debugtoolbar import DebugToolbarExtension
from random import choice, randint, sample
# Next we create an instance of this class. The first argument is the name of the application’s module or package. __name__ is a convenient shortcut for this that is appropriate for most cases.
# This is needed so that Flask knows where to look for resources such as templates and static files.
# instantiate a new application object and takes in the dunder name (__name__)
app = Flask(__name__)
# Later, when we talk about security & deployment, we’ll talk about when and how to actually keep this secret.
app.config['SECRET_KEY'] = "dumbonudumb"
# Turn off debug toolbar intercept redirect
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# We then use the route() decorator to tell Flask what URL should trigger our function.
# In this case we use / routh, which is the default route of any website.
# a decorator expecting a funciton to come right after this line
# listen for a request to '/', when that happens then call the following funciton


@app.route('/')
def index():
    # The function returns the message we want to display in the user’s browser.
    # The default content type is HTML, so HTML in the string will be rendered by the browser.
    """Show homepage"""
    # this returned string will be used to construct a full HTTP response

    # return """
    #   <html>
    #     <body>
    #       <h1>I am the landing page</h1>
    #     </body>
    #   </html>
    #   """
    return render_template('home.html')

# ---------------------------------------- redirect, POST reqeust, flash
# The status code is a “redirect code” (often, 302)
# we'll pretend that this old_home_page we actually had set up a couple of years ago,
# people might have bookmarked it, they might have it saved, it might be in Google search results,
# so we don't want to just elimiante it, and give a user an error if they try and request it.
# We'll just redirect them.
# Note: If you don’t want flask debug toolbar to intercept redirect, you can turn it off by:
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/old-home-page')
def redirect_to_home():
    """ Redirects to new home page"""
    return redirect('/')

# Most commonly will be redirecting when we have a POST request. And the reason for this is that POST requests usually
# include data from a user. Typically it's comming from a form. And that data is part of the request. It is sent
# with that request. And what that means is that, if a user were to refresh the page, when we serve HTML from a
# POST reqeust, they could resend that POST reqeust again and they get this weird "Are you sure you want to resubmit the form data?"
# It's a warning from the browser. And they would be sending that data again, even though they didn't type anything into
# a form, if they refresh, they're sending another POST reqeust. So instead of doing that, the typical workflow is to have
# a POST route where form data is sent to and process it inside of that route. And then when we're done, redirect a user
# to a different page, that is a GET request, and then we'll show some sort of confirmation or show proof that their form data
# was used in some way.


# fake DB
# we only want to allow a user to add a movie that is unique, sets automatically enforce that.
MOVIES = {'Amadeus', 'Chicken Run', 'Dances With Wolves'}

# sent a GET reqeust to /movies, and this responds with the list of movies,as well as the form (movies.html)


@app.route('/movies')
def show_all_movies():
    """Show list of all movies in fake DB"""
    return render_template('movies.html', movies=MOVIES)
# Add in methods equals POST in order to listen for a POST request coming in

# The data from the form input (in movies.html), the movie title is extracted from the form data
# and it's added into the fake database. Then, we redireted back to the same route ('/movies')


@app.route('/movies/new', methods=["POST"])
def add_movie():
    title = request.form['title']
    # Message Flashing
    # provide feedback to a user at whatever the next page is that they encounter,
    # so not permanent messages that we want to actually embed in the HTML,
    # but something that will only last for one-page load.
    # Flask will remove that msg after the user has seen it.
    if title in MOVIES:
        flash('Movie Already Exists!', 'error')
    else:
        # Add to pretend DB
        MOVIES.add(title)
        # pass a category through, all we do is add in a second argument
        # * inorder to access those categories, we need to add (with_categories=true)
        # as a parameter to get_flash_messages ("base.html")
        # we will use that category to style our actual content
        flash("Created Your Movie!", 'success')
    # We could have multiple flashes
        flash("Good choice!!")
    # If we want to use the same template (bellow), render the same list of template the form post reqeust will be
    # resent when we refresh, becuase it's a post route it responded with a template
#    return render_template('movies.html', movies=MOVIES)
# So instead of doing the above code, what we do normally do is redirect to some other GET route.
    return redirect('/movies')

# Not only does jsonify convert something into JSON format from Python/ we can respond with valid JSON objects ,
# it also is going to tell us in the response headers that content type is appplicaiton/json (inspect->Network->Headers)


@app.route('/movies/json')
def get_movies_json():
    return jsonify(list(MOVIES))
# ---------------------------------------- varibales, conditionals, loops, template inheritance


@app.route('/form')
def show_form():
    """Shows greeter V1 Form"""
    return render_template("form.html")


@app.route('/form-2')
def show_form_2():
    """Shows greeter V2 Form"""
    return render_template("form_2.html")


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


@app.route('/greet-2')
def get_greeting_2():
    """Greets and optionally compliments(3 random compliments) a user"""
    username = request.args["username"]
    # use get to prevent it from throwing an error if the box is not checked/ the boolean value wasn't passed as aprt of the query string
    wants = request.args.get("wants_compliments")
    # sample COMPLIMENTS adn we want 3 random compliments, and taht should give us a new list containing the compliments
    nice_things = sample(COMPLIMENTS, 3)
    return render_template("greet_2.html", username=username, wants_compliments=wants, compliments=nice_things)

# ---------------------------------------- variables, conditionals
# Jinja will replace things like {{msg}} with value of msg passed when rendering:
# here lucky_num will be passed to the lucky.html
# Conditionals in Jinja


@app.route('/lucky')
def lucky_number():
    num = randint(1, 10)
    return render_template("lucky.html", lucky_num=num, msg="You are so lucky!!")

# ---------------------------------------- Loops in Jinja


@app.route('/spell/<word>')
def spell_word(word):
    """Spells a word out letter by letter"""
    caps_word = word.upper()
    return render_template('spell_word.html', word=caps_word)


# ---------------------------------------- Handling Query Arguments
# request.args is a dict-like object of query parameters.


@app.route("/search")
def search():
    """Handle GET requests like /search?term=fun&sort=new"""
    # extrating data in a GET request from query string using request.args
    term = request.args["term"]
    sort = request.args["sort"]
    return f"<h1>Searching for {term} </h1> <p>Sorting by: {sort} </p> "


# ---------------------------------------- Handling POST Requests
# This route following is responding to GET requests
# To accept POST requests, must specify that: methods=["POST"]


@app.route("/add-comment") # GET method by default 
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
# POST requests, another type of request, can have a payload, also called a 'body', that is longer data that is included inside the request
# and that could be a string of data or it could be something a bit more formalized like json, it could also be a file or it could be form data:
# ```
# method: POST
# uri: /mysite
# body: {
#       "name", "chair",
#       "price", 17.99
#       }
# ```
# Some HTTP requests can have a payload, and others can't. GET requets for example can't have a payload, but POST and PUT can:
# ``` 
# method: GET
# uri: /mysite
# ``` 
# So why is this relevant? We can tell our form to use different types of requests depending on how we want it to send data. 
# If we tell our form to use get, then it can't put the data in the payload, it puts it in the url:
# ```
# GET
# <form> ------> ?date=2020-08-27&amount=70.00&account=Checking
# ```
# And if we use POST, then it'll put the data in the payload.
# ```
# POST/form
# <form method="POST"> ------>     Content-Type: x-www-form-urlencoded
#                                  Form Data:
#                                  
#                                  date: 2020-08-27
#                                  amount: 70.00
#                                  acount: Checking

# Another different between GET and POST: GET method is not secure which means anyone can see it's not secure information. It will 
# send to the server abnd then it will return to us the actual web page using a GET method.
# If we were to use post what we actually do is send secure iinformation that's encrypted that
# can't be you seen from either ends and is not stored on the actual web server. The basic way to think 
# of it is whenever you're using a GET command it's something that's not secure that you don't care if someone sees it, it's typically just typed in through 
# the address bar where it's just a link you redirecte to it. And then with POST, that's something secure it's usually form data and 
# it's something that we're not going to be sainvg on the the actual web server itself unless we're gonna be sending that to the data base.

# If we use the form method from GET to POST in the html code then we
# will no longer receive query strings, instead we'll need to change the flask
# code (from request.args) to request.form 

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

# Another example:

# login.html
<form action="#" method="post"> # if set action="#", you are going to stay on the same page
    <p>Name:</p>
    <p><input type="test" name="nm" /></p>
    <p><input type="submit" value="submit"/></p>
</form>

# app.py
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


# ----------------------------------------Variables in a URL
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

# ----------------------------------------Query Params vs URL Params
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

# finished f message categoreis


# -------------- python debugger (but flask_debugtoolbar is better)
# Python includes a built-in debugger, pdb. To add a breakpoint to your code:

# import pdb
# pdb.set_trace()

# When you hit that set_trace(), Python will stop so you can debug this.

# Debugger Basics:
# Key	Command
# ?	    Get help
# l	    List code where I am
# p	    Print this expression
# pp	Pretty print this expression
# n	    Go to next line (step over)
# s	    Step into function call
# r	    Return from function call
# c	    Continue to next breakpoint
# w	    Print “frame” (where am I?)
# q	    Quit debugger
