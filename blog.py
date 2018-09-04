#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import re
import sys

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'extra']
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route("/")
def index():
    return redirect(url_for('posts'))


@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    for x in posts:
        x.html = [y for y in x.html.split('\n')][0]
        x.html = re.sub(r'<h[1-9]>', '<p>', x.html)
        x.html = re.sub(r'</h[1-9]>', '</p>', x.html)
    return render_template('posts.html', posts=posts)


@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    post.html = post.html.replace('<table>', '<table class="table table-condensed">')   # for Booststrap/table
    return render_template('post.html', post=post)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('default'), 200, {'Content-Type': 'text/css'}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        pass
    else:
        app.run(debug=True, port=8000)
