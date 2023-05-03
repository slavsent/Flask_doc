from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectMultipleField


class CreateDocumentForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()], )
    body = TextAreaField("Body", [validators.DataRequired()], )
    submit = SubmitField("Publish")
