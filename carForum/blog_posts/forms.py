from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed,FileField


class BlogPostForm(FlaskForm):

    title=StringField("Title",validators=[DataRequired()])
    text=TextAreaField('Text',validators=[DataRequired()])
    # post_pic=FileField('Add Image',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Post')