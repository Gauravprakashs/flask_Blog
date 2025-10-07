
#views for register, login, list, account ,update ,list blog posts

from flask import render_template,redirect,Blueprint,url_for,request,flash
from flask_login import current_user,login_user,logout_user,login_required
from carForum import db

from carForum.models import Users,BlogPost
from carForum.users.forms import UpdateUserForm,LoginForm,RegistrationForm
from carForum.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash,check_password_hash
users=Blueprint('users',__name__)


@users.route('/register',methods=["GET","POST"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=Users(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Welcome to OUr Comunnity!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html',form=form)


@users.route('/login',methods=["GET","POST"])
def login():

    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()

        if user.verify_password(form.password.data) and user is not None:
            login_user(user)
            flash('Welcome')

            next=request.args.get('next')

            if next == None or not next[0]=='/':
                next=url_for('core.index')

            return redirect(next)
    return render_template('login.html',form=form)

@users.route('/account',methods=["GET","POST"])
@login_required
def account():
    form =UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username=form.username.data
            pic=add_profile_pic(form.picture.data,username)
            current_user.profile_image=pic
        
        current_user.username=form.username.data
        current_user.email=form.email.data
       
        db.session.commit()
        flash('User Updated')

        return redirect(url_for('users.account'))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email

    profile_image=url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)

@users.route('/<username>')
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=Users.query.filter_by(username=username).first_or_404()
    blog_posts=BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_post.html',blog_posts=blog_posts,user=user)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


