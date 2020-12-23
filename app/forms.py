from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class SingleInputPlaylistForm(FlaskForm):
    input = StringField('Input (one genre or artist)', validators=[DataRequired()])
    name = StringField('Playlist name', validators=[DataRequired()])

class RecommendationForm(FlaskForm):
    genres = StringField('Genres')
    artists = StringField('Artists')
    tracks = StringField('Tracks')
    amount = IntegerField('Amount of Tracks', validators=[DataRequired(), NumberRange(min=0, max=550, message="Amount must be between 0 and 550")])
    name = StringField('Playlist name', validators=[DataRequired()])
    unique = BooleanField('Unique')




