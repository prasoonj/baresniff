#login.py
from baresniff import app
from baresniff import models

#from mongoengine import ValidationError



# 
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         #login and validate the user
#         login_user(user) #TODO: Implement the login_user(user) function
#         flash("Logged in successfully.")
#         return redirect(request.args.get("next") or url_for("index"))
#     return render_template("login.html", form=form)
#     