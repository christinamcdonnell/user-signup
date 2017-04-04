#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
from string import letters

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h1>Christina's Stupendous Signup </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
    <h3 style="color:tourquoise">the footer ... the footer ... the footer </h3>

</body>
</html>
"""
#Username: "^[a-zA-Z0-9_-]{3,20}$"
#Password: "^.{3,20}$"
#Email: "^[\S]+@[\S]+.[\S]+$"

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.usersignup.com/
    """
    def get(self):
        edit_header = "<h3>Signup -H3 Header from the Index - get </h3>"
        # INITIALIZE ERROR MESSAGES - will this blank out my errror messages
#        username_err = ""
#        password_err = ""
#        verify_password_err = ""
#        email_err = ""

        username_form = ""
        username_form  = fill_form()
        page_content = edit_header + username_form
        #content = page_header + page_content + page_footer
        self.response.write(page_content)

def fill_form(username="", email="", username_err="", password_err="", verify_password_err="", email_err=""):

    my_form = """
    <form action="/signup" method="post">
        <label>
            <div>
            Username:
            <input type="text" name="username" value="{username}"/>
            </div>
        </label>
        <div style="color:red"> {username_err}</div> <!-- error message for invalid username -->
        <br><br>

        <label>
            Password:
            <input type="text" name="password"/>
        </label>
        <div style="color:red"> {password_err}</div> <!-- error message for invalid password & blank out password -->

        <label>
            Verify Password:
            <input type="text" name="verify_password"/>
        </label>
        <div style="color:red"> {verify_password_err}</div> <!-- error message for mismatched password & verify_password -->
        <br><br>

        <label>
            Email (Optional):
            <input type="text" name="email" value="{email}"/>
            <!-- add an error message display here for invalid email -->
        </label>
        <div style="color:red"> {email_err}</div>
        <br>
        <input type="submit" value="JOIN"/>
    </form>
    """.format(username_err=username_err, password_err=password_err, verify_password_err=verify_password_err,
    email_err=email_err, username=username, email=email)

    page_content = page_header + my_form + page_footer
    return(page_content)

##### CHECK USERNAME
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

##### CHECK PASSWORD
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

##### CHECK EMAIL
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

#####
class SignUpHandler(webapp2.RequestHandler):
    #def get(self):
    #    self.request("signup-form.html")
    #return

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['username_err'] = "Username is invalid. Please enter a valid username."
            have_error = True

        if not valid_password(password):
            params['password_err'] = "Password is invalid. Please enter a valid password."
            have_error = True
        elif password != verify_password:
            params['verify_password_err'] = "The password verification does not match. Please try again."
            have_error = True

        if not valid_email(email):
            params['email_err'] = "The email entered is not valid. Please try again."
            have_error = True

        if have_error:
            password = ""
            verify_password = ""
            SignUp_form = fill_form( **params)
            self.response.write(SignUp_form)
            #self.redirect('/') # how do I send  or otherwise make sure the pw fields are blanked out???
            #self.redirect('/', **params) # not sure about this yet
            #    self.render('signup-form.html', **params) #this from blog.py
        else:
            self.redirect('/welcome?username=' + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write("Welcome " + username + "!")
        else:
            self.redirect('/') # send back to initial screen or signup -do I send anything with it???

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUpHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
