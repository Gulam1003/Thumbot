from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, BlogPost
from auth.routes import admin_required

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog')
def blog():
    """
    Render the blog page with all blog posts.

    Queries all blog posts from the database and renders them on the blog page.

    Returns:
        Response: The rendered blog template with all posts.
    """
    posts = BlogPost.query.all()
    return render_template('blog.html', posts=posts)

@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    """
    Render a single blog post page.

    Queries a blog post by ID and renders it on the post page.

    Args:
        post_id (int): The ID of the blog post to be displayed.

    Returns:
        Response: The rendered post template with the specified blog post.
    """
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@blog_bp.route('/admin')
@admin_required
def admin():
    """
    Render the admin page with all blog posts.

    Queries all blog posts from the database and renders them on the admin page.
    This route is protected and requires admin privileges.

    Returns:
        Response: The rendered admin template with all posts.
    """
    posts = BlogPost.query.all()
    return render_template('admin.html', posts=posts)

@blog_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    """
    Handle adding a new blog post.

    If the request method is POST, it processes the form data to create a new blog post.
    This route is protected and requires admin privileges.

    Returns:
        Response: The rendered add post template or a redirect to the admin page after adding the post.
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('user')

        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('blog.admin'))

    return render_template('add_post.html')

@blog_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def edit(post_id):
    """
    Handle editing an existing blog post.

    If the request method is POST, it processes the form data to update the blog post.
    This route is protected and requires admin privileges.

    Args:
        post_id (int): The ID of the blog post to be edited.

    Returns:
        Response: The rendered edit post template with the post data or a redirect to the admin page after updating the post.
    """
    post = BlogPost.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('blog.admin'))

    return render_template('edit_post.html', post=post)

@blog_bp.route('/delete/<int:post_id>', methods=['POST'])
@admin_required
def delete(post_id):
    """
    Handle deleting a blog post.

    Processes the request to delete the specified blog post from the database.
    This route is protected and requires admin privileges.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        Response: A redirect to the admin page after deleting the post.
    """
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('blog.admin'))
