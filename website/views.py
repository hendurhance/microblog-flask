from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
# Home page
def home():
    # Get all posts from database
    posts = Post.query.all()
    # Render the home page with posts as the template context
    return render_template("home.html", user=current_user, posts=posts)


# Create post route for creating a new post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    # if request method is POST
    if request.method == "POST":
        # Get the post content from the form
        text = request.form.get('text')

        # if post content is empty
        if not text:
            flash('Post cannot be empty', category='error')
        # If post content is not empty then create a new post
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
    # Render the create post page with User as the template context
    return render_template('create_post.html', user=current_user)


# Create a route for deleting a post with a post id
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    # Get the post from the database using the post id
    post = Post.query.filter_by(id=id).first()

    # if post does not exists
    if not post:
        flash("Post does not exist.", category='error')
    # if post exists but is not owned by the current user
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    # if post exists and is owned by the current user then delete the post
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
    # Redirect to the home page
    return redirect(url_for('views.home'))

# Create a route for getting all posts from a user
@views.route("/posts/<username>")
@login_required
def posts(username):
    # Get the user from the database using the username
    user = User.query.filter_by(username=username).first()

    # if user does not exists
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    # All posts from the user
    posts = user.posts
    # Render the posts page with user and posts as the template context
    return render_template("posts.html", user=current_user, posts=posts, username=username)

# Create a comment route for creating a new comment
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    # Get text from the form
    text = request.form.get('text')

    # if text is empty
    if not text:
        flash('Comment cannot be empty.', category='error')
    # If text is not empty then create a new comment
    else:
        post = Post.query.filter_by(id=post_id)
        # If post does exist
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        # if post does not exist then flash an error
        else:
            flash('Post does not exist.', category='error')
    # Redirect to the home page
    return redirect(url_for('views.home'))

# Create a route for deleting a comment with a comment id
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    # Get the comment from the database using the comment id
    comment = Comment.query.filter_by(id=comment_id).first()
    # If comment does not exist
    if not comment:
        flash('Comment does not exist.', category='error')
    # If comment exists but is not owned by the current user then flash an error
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    # If comment exists and is owned by the current user then delete the comment
    else:
        db.session.delete(comment)
        db.session.commit()
    # Redirect to the home page
    return redirect(url_for('views.home'))

# Create a route for liking a post with a post id
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    # Get the post from the database using the post id
    post = Post.query.filter_by(id=post_id).first()
    # Like the post if it exists
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    # If post does not exist then return a json response with an error message
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    # Remove the like if it exists when the user unlikes the post
    elif like:
        db.session.delete(like)
        db.session.commit()
    # If post exists and user has not liked the post then like the post
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    # Return a json response with the likes count for the post, the user's id and the post id
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})
