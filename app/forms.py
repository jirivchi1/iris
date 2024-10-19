from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Nombre de Usuario", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "Contraseña", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Iniciar Sesión")


class SignupForm(FlaskForm):
    username = StringField(
        "Nombre de Usuario", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "Contraseña", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Registrarse")
