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
    <style>
        input:invalid{
        border : 2px solid red
        }
    </style>
</head>
<body>
"""

bottom = """
</body>
</html>
"""


#Errors
username_problems = top + "<p>Your username is invalid. Please, don't use spaces or any coding of your own...</p>" + bottom
mail_problems = top + "<p>The email address you entered is not or  valid. Please do not use a temporary host or a host that will filter out our mail.</p>" + bottom
password_problems = top + "<p>Your passwords do not match. Please try again.</p>" + bottom


def password_validation(entered,truepass):
    if entered == truepass and not entered == "":
        return True
    return False

def username_validation(user):
    if " " not in user and not user == "":
        return True
    return False

def email_validation(email):
    essentials = [".com",".org",".biz",".edu",".net",".gov","@","."]
    for element in essentials:
        if element in email:
            return True
        else:
            return False
    bad_things = ["mvrht.com","zasod.com","my10minutemail.com","hellokitty.com", " "]
    for thing in bad_things:
        if thing in email:
            return False
    return True
    #Make a username validator using cgi

    #Make email validaion

    #Make 4 input fields, with four values to correspond with validation

    #Greet the user when they hit submit

big_title = """<h1>Signup</h1>"""

class Homepage(webapp2.RequestHandler):

    def get(self):
        forms = """
        <form method="post" action="/greetings">
            <label> Enter Username
                <input type="text" name="user" value=user>
            </label>
            <br>
            <label> Enter Password
                <input type="password" name="truepass">
            </label>
            <br>
            <label> Confirm Password
                <input type="password" name="entered">
            </label>
            <br>
            <label> (Optional) Enter Email
                <input type="text" name="email" value="email">
            </label>
            <input type="submit">
        </form>
            """

        final = top + big_title + forms + bottom
        self.response.write(final)


class Greetings(webapp2.RequestHandler):

    def post(self):
        tbe = self.request.get("user") #To-Be-Escaped
        tbe = cgi.escape(tbe, quote=True)
        password = password_validation(self.request.get("truepass"),self.request.get("entered"))
        user = username_validation(tbe)
        mail = email_validation(self.request.get("email"))

        if user == True:
            if password == True:
                if mail == True:
                    greetings = """
                    <h3>Welcome,
                    """
                    final = top + greetings + self.request.get("user") + "!</h3>" + bottom
                    self.response.write(final)
                else:
                    self.response.write(mail_problems)
                    self.redirect("/?error=mail_error")
            else:
                self.response.write(password_problems)
                self.redirect("/?error=pass_error")
        else:
            self.response.write(username_problems)
            self.redirect("/?error=name_error")





app = webapp2.WSGIApplication([
    ('/', Homepage),
    ('/greetings',Greetings)
], debug=True)
