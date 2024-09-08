from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret_key"

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return "<Article %r>" % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    subscribe_to_newsletter = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"


@app.route("/")
def main():
    articles = Article.query.order_by(Article.date.desc()).limit(6).all()
    return render_template("index.html", articles=articles)


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>")
def posts_details(id):
    article = Article.query.get(id)

    return render_template("post_detail.html", article=article)


@app.route("/posts/<int:id>/delete")
def posts_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Error delete arrticle!"


@app.route("/posts/<int:id>/update", methods=["POST", "GET"])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]
        try:
            db.session.commit()
            return redirect("/posts")
        except:
            return "Error update post!"
    else:
        return render_template("post_update.html", article=article)


@app.route("/create-article", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except:
            return "Error add-arrticle!"
    else:
        return render_template("create-article.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        address1 = request.form.get("address1")
        address2 = request.form.get("address2")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zip")
        subscribe_to_newsletter = "check_me_out" in request.form

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip=zip,
            subscribe_to_newsletter=subscribe_to_newsletter,
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("registration.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.first_name
            return redirect("/")

        return (
            "Invalid credentials",
            401,
        ) 

    return render_template("login.html") 


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect("/login")


@app.route("/success")
def success():
    if "user_id" not in session:
        return redirect("/login")

    users = User.query.all()
    return render_template("success.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
