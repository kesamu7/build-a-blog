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
import os
import jinja2


from google.appengine.ext import db

#jinja setup below.
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Apost(db.Model):
    title = db.StringProperty(required = True)
    post_bod = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(Handler):

    def render_posts(self, title="", post_bod = "", error = ""):
        posts = db.GqlQuery("SELECT * FROM Apost ORDER BY created DESC")

        self.render("frontpage.html", title = title, post_bod = post_bod, error=error, posts=posts)


    def get(self):
        self.render_posts()

    def post(self):

        self.redirect("/newpost")

class NewPosts(Handler):
    def get(self):

        self.render("newposting.html")

    def post(self):
        #Here I will either do self.render('frontpage.html' + the new post)
        #Or I will do, self.redirect('frontpage.html' + the new post)Lets experiment and find out which one.
        #I think that my post here needs to follow a similar path as the post in asciichan, but it needs to direct the new blog post to the frontpage.
        title = self.request.get("title")
        post_body = self.request.get("post_bod")

        if title and post_body:
            p = Apost(title = title, post_body = post_body)
            p.put()
            self.redirect("/")

        else:
            error = "Please enter a post title and some content in the post body."
            self.render_posts(title,post_body,error)







app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost',NewPosts)
], debug=True)
