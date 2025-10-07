from carForum import db
from carForum.blog_posts.forms import BlogPostForm
from flask import render_template,redirect,url_for,flash,request,Blueprint,abort
from flask_login import login_user,logout_user,login_required,current_user
from carForum.models import BlogPost
# from carForum.blog_posts.save_post_image import save_post_image



blog_posts=Blueprint('blog_posts',__name__)

@blog_posts.route('/create',methods=["GET","POST"])
@login_required
def create_post():

    form=BlogPostForm()
    if form.validate_on_submit():

        # if form.post_pic.data:
        #     username=current_user.username
        #     pic=save_post_image(form.post_pic.data,username)
        #     current_user.post_picture=pic


        post=BlogPost(title=form.title.data,text=form.text.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        flash("POST Created 📬📬📬")

        return redirect(url_for('core.index'))
    return render_template('create_post.html',form=form)


@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):

    blog_post=BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',title=blog_post.title,
                           date=blog_post.date,post=blog_post)

@blog_posts.route('/<int:blog_post_id>/update',methods=["GET","POST"])
@login_required
def update(blog_post_id):

    blog_post=BlogPost.query.get_or_404(blog_post_id)
    
    if blog_post.author != current_user:
        abort(403)

    form=BlogPostForm()
    if form.validate_on_submit():

        blog_post.title=form.title.data
        blog_post.text=form.text.data
        db.session.commit()

        flash("Updated POst")

        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))
    
    elif request.method == 'GET':
        form.title.data=blog_post.title
        form.text.data=blog_post.text
    
    return render_template('create_post.html',title='Updatiing',form=form)


@blog_posts.route('/<int:blog_post_id>/delete',methods=["GET","POST"])
@login_required
def delete_post(blog_post_id):

    blog_post=BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash("Deleted Suceess ")
    return redirect(url_for('core.index'))

   

        

