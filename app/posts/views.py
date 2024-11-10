from . import post_bp
from flask import render_template, abort, redirect, url_for, flash
from .forms import PostForm
import json, os

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

@post_bp.route("/") 
def get_posts():
    return render_template("posts.html", posts = posts)

@post_bp.route("/<int:id>") 
def detail_post(id):
    if id > 3:
        abort(404)
    post = posts[id-1]
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():

        if os.path.exists("posts.json"):
            with open("posts.json", 'r') as file:
                data = json.load(file)
            if data:
                last_id = data[-1]["id"]
            else:
                last_id = 0
        else:
            data = []
            last_id = 0

        post_data = {
            "id": last_id + 1,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": str(form.publish_date.data),
            "category": form.category.data,
            "author": form.author.data
        }

        data.append(post_data)

        with open("posts.json", "w") as file:
            json.dump(data, file, indent=4)

        # print(data)
        flash(f'Post {post_data["title"]} added successfully!', 'success')
        return redirect(url_for('.view_posts'))
    return render_template('add_post.html', form=form)

@post_bp.route("/view_posts")
def view_posts():

    if os.path.exists("posts.json"):
        with open("posts.json", "r") as file:
            posts = json.load(file)
    else:
        posts = []

    return render_template("view_posts.html", posts=posts)