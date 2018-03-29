# coding:utf-8
# /usr/bin/python

# from flask_wtf import Form
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from . import *


class LoginForm(FlaskForm):
    email = StringField(label=u"邮箱地址", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(label=u"密码", validators=[DataRequired()])
    submit = SubmitField(label=u"提交")


class RegistrationForm(FlaskForm):
    email = StringField(label=u"邮箱地址", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(label=u"用户名", validators=[DataRequired(), Length(1, 64),
                                                     Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u"用户名必须由数字，字母，下划线或者.组成")])
    password = PasswordField(u"密码", validators=[DataRequired(), EqualTo('password2', message=u"密码必须相同")])
    password2 = PasswordField(u"确定密码", validators=[DataRequired()])
    submit = SubmitField(u"马上注册")
