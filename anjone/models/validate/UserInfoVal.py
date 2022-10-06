from wtforms import Form, StringField, validators


class UserInfoVal(Form):
    username = StringField('username', [validators.Length(min=1), validators.DataRequired()])
    phone = StringField('phone', [validators.Length(min=11, max=11), validators.DataRequired()])
    password = StringField('password')
    code = StringField('code')
