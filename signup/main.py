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


top = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
"""

bottom = """
</body>
</html>
"""

def pass_correct(entered):
    if len(entered) < 1:
        return True
    return False

def password_validation(truepass,entered):
    if len(truepass) > 1 and truepass != "" and not " " in truepass and entered == truepass:
        return True
    return False

def username_validation(user):
    if len(user) > 1 and " " not in user and not user == "":
        return True
    return False

def email_validation(email):
    if email == "":
        return True
    essentials = [".com",".org",".biz",".edu",".net",".gov","@","."]
    for element in essentials:
        if element in email:
            return True
        else:
            return False

big_title = """<h1>Signup</h1>"""

forms = """
<div>
    <form method="get" action="/greetings">
        <label> Enter Username
            <input type="text" name="user" value="%(user)s" required />
            <span class="error" style="color: red">%(user_error)s</span>
        </label>
        <br>
        <label> Enter Password
            <input type="password" name="truepass" required placeholder="Enter a password."/>
            <span class="error" style="color: red">%(pass_error_one)s</span>
        </label>
        <br>
        <label> Confirm Password
            <input type="password" name="entered" required placeholder="Confirm password."/>
            <span class="error" style="color: red">%(pass_error_two)s</span>
        </label>
        <br>
        <label> (Optional) Enter Email
            <input type="email" name="email" value="%(email)s" placeholder="Enter an email, if you'd like.">
            <span class="error" style="color: red">%(mail_error)s</span>
        </label>
        <br>-
            <input type="submit">
        </a>
    </form>
</div>
    """

class Homepage(webapp2.RequestHandler):
    def write_page(self,user_error="",pass_error_one="",pass_error_two="",mail_error="",user="",email=""):
        self.response.out.write(top + big_title + forms % {"user_error":user_error,"pass_error_one":pass_error_one,"pass_error_two":pass_error_two,"mail_error":mail_error, "user":user, "email":email} + bottom)

    def get(self):
        self.write_page()

class Greetings(webapp2.RequestHandler):
    def write_page(self,user_error="",pass_error_one="",pass_error_two="",mail_error="",user="",email=""):
        self.response.out.write(top + big_title + forms % {"user_error":user_error,"pass_error_one":pass_error_one,"pass_error_two":pass_error_two,"mail_error":mail_error, "user":user, "email":email} + bottom)

    def get(self):
        user_error = ""
        pass_error_one = ""
        pass_error_two = ""
        mail_error = ""

        tbe = self.request.get("user") #To-Be-Escaped
        tbe = cgi.escape(tbe, quote=True)
        password1 = self.request.get("truepass")
        password2 = self.request.get("entered")
        mail = self.request.get("email")

        tbe_valid = username_validation(tbe)
        pass_valid = password_validation(password1,password2)
        mail_validation = email_validation(mail)

        if tbe_valid == False:
            user_error = "Your username is invalid."
            self.write_page(user_error,pass_error_one,pass_error_two,mail_error,tbe,mail)
            return
        if pass_valid == False:
            pass_error_one = "Your password is invalid."
            self.write_page(user_error,pass_error_one,pass_error_two,mail_error,tbe,mail)
            return
        if pass_correct == False:
            pass_error_two = "Your passwords do not match."
            self.write_page(user_error,pass_error_one,pass_error_two,mail_error,tbe,mail)

        if mail_validation == False:
            mail_error = "Your email address is invalid."
            self.write_page(user_error,pass_error_one,pass_error_two,mail_error,tbe,mail)
            return

        tbe = self.request.get("user") #To-Be-Escaped
        tbe = cgi.escape(tbe, quote=True)
        data = []
        data.append(tbe)
        greetings = """
            <h3>Welcome,
            """
        final = top + greetings + tbe + "!</h3>" + bottom
        self.response.write(final)





app = webapp2.WSGIApplication([
    ('/', Homepage),
    ('/greetings',Greetings)
], debug=True)
