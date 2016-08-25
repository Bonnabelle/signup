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

def password_validation(truepass,entered):
    if truepass != "" and not " " in truepass and entered == truepass:
        return True
    return False

def username_validation(user):
    if " " not in user and not user == "":
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
    <form method="post" action="/">
        <label> Enter Username
            <input type="text" name="user" value="%(user)s" required />
            <span style="color: red">%(error)s</span>
        </label>
        <br>
        <label> Enter Password
            <input type="password" name="truepass" required placeholder="Enter a password."/>
            <span style="color: red">%(error)s</span>
        </label>
        <br>
        <label> Confirm Password
            <input type="password" name="entered" required placeholder="Confirm password."/>
            <span style="color: red">%(error)s</span>
        </label>
        <br>
        <label> (Optional) Enter Email
            <input type="email" name="email" value="%(email)s" placeholder="Enter an email, if you'd like.">
            <span style="color: red">%(error)s</span>
        </label>
        <br>
        <a href=?username=%(user)s">
            <input type="submit">
        </a>
    </form>
</div>
    """

class Homepage(webapp2.RequestHandler):
    def write_page(self,error="",user="",email=""):
        self.response.out.write(top + big_title + forms % {"error":error, "user":user, "email":email} + bottom)

    def get(self):
        self.write_page()

    def post(self):
        tbe = self.request.get("user") #To-Be-Escaped
        tbe = cgi.escape(tbe, quote=True)
        password1 = self.request.get("truepass")
        password2 = self.request.get("entered")
        mail = self.request.get("email")

        tbe_valid = username_validation(tbe)
        pass_valid = password_validation(password1,password2)
        mail_validation = email_validation(mail)



        if tbe_valid == False:
            self.write_page("Your username is invalid.",tbe,mail)
        if pass_valid == False:
            self.write_page("Your password is invalid. Please try again.",tbe,mail)
            return
        if mail_validation == False:
            self.write_page("This email address cannot be used. Make sure you are not providing a temporary host address, or a spam email.",tbe,mail)
            return
        else:
            greetings = """
                <h3>Welcome,
                """
            final = top + greetings + tbe + "!</h3>" + bottom
            self.response.write(final)



app = webapp2.WSGIApplication([
    ('/', Homepage)
], debug=True)
