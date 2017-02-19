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
import logging
import time


from google.appengine.ext import db


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
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(Handler):
    def render_posts(self,title="title",body="body"):
        posts = db.GqlQuery("SELECT * FROM Apost ORDER BY created DESC LIMIT 5")
        self.render("frontpage.html", title=title,body=body,posts=posts)

    def get(self):
        #self.render("frontpage.html")
        self.render_posts()

    def post(self):

        self.redirect("/newpost")


class NewPosts(Handler):

    def new_form(self,title="",body="",error=""):

        logging.info(error)
        self.render("newposting.html",title=title,body=body,error=error)

    def get(self):

        self.new_form()

    def post(self):
        post_title = self.request.get("title")
        post_bod = self.request.get("body")

        if post_title and post_bod:
            new_post = Apost(body=post_bod,title=post_title)
            new_post.put()
            id = new_post.key().id()
            self.redirect('/blog/{}'.format(id))

        else:

            error = "Please provide a title and content in the post body."
            self.new_form(error=error)



class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        if Apost.get_by_id(int(id)) == None:
            self.response.write("No posts with that id.")

        else:
            blog_id = Apost.get_by_id(int(id))
            self.response.write(blog_id.title)
            self.response.write(blog_id.body)

        #replace this with some code to handle the request




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost',NewPosts),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)

],debug=True)
