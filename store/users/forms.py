
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from store.models.user import User
import phonenumbers

datarequired= DataRequired('Por favor llenar este campo')

class RegistrationForm(FlaskForm):
    
    firstName= StringField('Nombre', 
                            validators=[datarequired, Length(min=2, max=10)])
    lastName= StringField('Apellido', 
                            validators=[datarequired, Length(min=2, max=10)])
    email= StringField('', 
                            validators=[datarequired, Email('Email no valido')])
    phone = StringField('Telefono', validators=[datarequired])
    password= PasswordField('Contraseña', validators=[datarequired])
    confirm_password= PasswordField('Confirmar contraseña', validators=[datarequired, 
                                    EqualTo('password', 'Las contraseñas deben coincidir')])
    submit= SubmitField('Crear cuenta')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Numero de telefono no valido')

    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email en uso')

class LoginForm(FlaskForm):
    
    email= StringField('', 
                        validators=[datarequired, Email('Email no valido')])
    password= PasswordField('', validators=[datarequired])
    remember= BooleanField('Recuerdame')
    submit= SubmitField('Iniciar sesion')