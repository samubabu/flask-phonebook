from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class AddressForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    confirm_phone = StringField('Confirm Phone Number', validators=[DataRequired(), EqualTo('phone')])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField()

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()



    
    #def validate_phone(form, field):
        #if len(field.data) > 16:
            #raise ValidationError('Invalid phone number.')
        #try:
            #input_number = phonenumbers.parse(field.data)
            #if not (phonenumbers.is_valid_number(input_number)):
                #raise ValidationError('Invalid phone number.')
        #except:
            #input_number = phonenumbers.parse("+1"+field.data)
            #if not (phonenumbers.is_valid_number(input_number)):
                #raise ValidationError('Invalid phone number.')