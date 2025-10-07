
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,Optional
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from carForum.models import Users

class LoginForm(FlaskForm):

    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('LOG IN')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('USername',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Password MUST MAtch')])
    password_confirm=PasswordField('COnfirm PAssword',validators=[DataRequired()])
    submit=SubmitField('Register!!')


    def validate_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('EMAIL already Exists!!')
        
    def validate_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Your USername is Alreay REgistered')
        

class UpdateUserForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('USername',validators=[DataRequired()])
    picture=FileField('Update PIcture',validators=[FileAllowed(['jpg','png'])])
   
    submit=SubmitField('UPdate')

    def validate_email(self,field):
        if field.data != current_user.email:
            if Users.query.filter_by(email=field.data).first():
                raise ValidationError('EMAIL already Exists!!')
            
    def validate_username(self,field):
        if field.data != current_user.username:
            if Users.query.filter_by(username=field.data).first():
                raise ValidationError('Your USername is Alreay REgistered')
        
