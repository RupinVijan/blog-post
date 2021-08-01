from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail
from flask_migrate import Migrate


with open('config.json' , 'r') as c:
    paras=json.load(c)["para"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=paras['gmail_id'],
    MAIL_PASSWORD=paras['gmail_pass']

)
mail=Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = paras['local_uri']
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Phone = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Name
class Blogs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Topic = db.Column(db.String(80), nullable=False)
    Name = db.Column(db.String(120), unique=True, nullable=False)
    slug=db.Column(db.String(25),unique=True)
    Content = db.Column(db.String(1200), unique=True, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<User %r>' % self.Name

@app.route("/")
def hello_world():
    blog=Blogs.query.all()
    return render_template("front.html",blog=blog)
@app.route("/logout")
def logout():
    
    return redirect("/admin")

@app.route("/delete/<string:sno>" , methods=['GET','POST'])
def delete(sno):
    dets=Details.query.filter_by(sno=sno).first()
    db.session.delete(dets)
    db.session.commit()
    return redirect("/admin")



@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method=='POST':
        user=request.form.get('user')
        password=request.form.get('pass')
        if user==paras['id'] and password==paras['pass']:
            dets=Details.query.all()
            return render_template("info.html",dets=dets)
        else:
            return render_template("admin.html")
    return render_template("admin.html")

@app.route('/front' , methods=['GET'])
def mainscreen():
    blog=Blogs.query.all()
    return render_template('front.html', blog=blog)



@app.route('/contact', methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')

        entry=Details(Name=name,Email=email,Phone=phone)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('This message is from ' + name,
        sender=email, recipients=[paras['gmail_id']],
        body="\ncontact number" + phone
        )
    return render_template('contact.html')

@app.route("/blog/<string:Slugs>",methods=['GET'])
def blog(Slugs):
    blog=Blogs.query.filter_by(slug = Slugs ).first()
    return render_template('blog.html',blog=blog)

@app.route("/addcontent" , methods=['GET','POST'])
def addcontent():
    if request.method=='POST':
        topic=request.form.get('topic')
        author=request.form.get('author')
        slug=request.form.get('slug')
        blog=request.form.get('blog')
        quest=Blogs(Topic=topic,Name=author,Content=blog,slug=slug)
        db.session.add(quest)
        db.session.commit()
    return render_template('addcontent.html')

if __name__=="__main__":
    app.run(debug=True)