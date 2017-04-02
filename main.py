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
    <h1>Christina's Fabulous User Signup Heading</h1>
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
        edit_header = "<h3>H3 Header from the Index - get </h3>"
        # a form for username entry and verification
        username = self.request.get("username")
        if username and not valid_username:
            #set error

        password = self.request.get("username")


        username_form = """
        {username}
        <form action="/signup" method="post">
            <label>
                Username:
                <input type="text" name="username"/>
                <!-- add an error message display here for invalid username -->
            </label>
            <div style="color:red"> {username_err}</div>
            <br><br>

            <label>
                Password:
                <input type="text" name="password"/>
                <!-- add an error message display here for invalid password & blank out password -->
            </label>
            <div style="color:red"> {password_err}</div>

            <label>
                Verify Password:
                <input type="text" name="verify_password"/>
                <!-- add an error message display here for mismatched password & verify_password -->
            </label>
            <div style="color:red"> {verify_password_err}</div>
            <br><br>

            <label>
                Email (Optional):
                <input type="text" name="email"/>
                <!-- add an error message display here for invalid email -->
            </label>
            <div style="color:red"> {email_err}</div>
            <br>
            <input type="submit" value="Signup"/>
        </form>
        """.format(username_err = "Username is invalid. Please enter a valid username.",
        password_err = "Password is invalid. Please enter a valid password.",
        verify_password_err = "The password verification does not match. Please try again.",
        email_err = "The email entered is not valid. Please try again.",
        username=username)

        page_content = edit_header + username_form
        content = page_header + page_content + page_footer
        self.response.write(content)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class SignUpHandler(webapp2.RequestHandler):

    def get(self):
        self.request("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.redirect('/', **params)
        else:
            self.redirect('/welcome?username=' + username)


class WelcomeHandler(webapp2.RequestHandler):
    def get(self):

            welcome_form = """
            {username}
            <form action="/welcome" method="post">
                <label>
                    Username:
                    <input type="text" name="username"/>
                    <!-- add an error message display here for invalid username -->
                </label>
                <div style="color:red"> {username_err}</div>
                <br>
                <input type="submit" value="Welcome"/>
            </form>
            """.format(username_err = "Username is invalid. Please enter a valid username.",
            password_err = "Password is invalid. Please enter a valid password.",
            verify_password_err = "The password verification does not match. Please try again.",
            email_err = "The email entered is not valid. Please try again.",
            username=username)

        # Get username, password, verify_password & email, Check for validity and set error messages???
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup') # send back to initial screen or signup ???


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUpHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
