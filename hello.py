from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config['SECRET_KEY'] = 'macdaddymakeyoujump'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
bootstrap= Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)



############
# manager#####
############

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


migrate = Migrate(app,db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

##########
# mail ###
##########

app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USE_SSL"] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')



@app.route('/', methods=['GET',"POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known']=False
            if app.config["FLASKY_ADMIN"]:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known']=True
        session['name'] = form.name.data
        form.name.data =""
        return redirect(url_for('index'))
    return render_template("index.html",
        form=form, name=session.get('name'),
        known=session.get('known', False),
        current_time = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(Form):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


#############
# Models ####
#############


class Role(db.Model):
    __tablename__= 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref = "role", lazy="dynamic")

    def __repr__(self):
        return "<role %r>"% self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<user %r>"%self.username


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

if __name__ == '__main__':
    #app.run( debug=True)
    manager.run()




#msg = Message('test subject', sender='joshadamkerbel@gmail.com',recipients=['josh@rallyyourgoals.com'])