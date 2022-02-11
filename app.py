# First we import the Flask class. An instance of this class will be our WSGI application.
# request, represents web requests, helps access to the query string inside of "request.args[...]"
from crypt import methods
from flask import Flask, request, render_template, redirect
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

# ---------------------------------------- redirect, POST reqeust
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


# fake DB
MOVIES = ['Amadeus', 'Chicken Run', 'Dances With Wolves']

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
    # Add to pretend DB
    MOVIES.append(title)
    # If we want to use the same template (bellow), render the same list of template the form post reqeust will be
    # resent when we refresh, becuase it's a post route it responded with a template
#    return render_template('movies.html', movies=MOVIES)
# So instead of doing the above code, what we do normally do is redirect to some other GET route.
    return redirect('/movies')
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

# finished falsk-redirects


# Most commonly will be redirecting when we have a POST request. And the reason for this is that POST requests usually
# include data from a user. Typically it's comming from a form. And that data is part of the request. It is sent
# with that request. And what that means is that, if a user were to refresh the page, when we serve HTML from a
# POST reqeust, they could resend that POST reqeust again and they get this weird "Are you sure you want to resubmit the form data?"
# It's a warning from the browser. And they would be sending that data again, even though they didn't type anything into
# a form, if they refresh, they're sending another POST reqeust. So instead of doing that, the typical workflow is to have
# a POST route where form data is sent to and process it inside of that route. And then when we're done, redirect a user
# to a different page, that is a GET request, and then we'll show some sort of confirmation or show proof that their form data
# was used in some way.
