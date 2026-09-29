from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps
import psycopg2
import os
 #rendertemplete is a HTML converted template.......,
 #request allows to get info submitted from form....,
 #redirect allows page changes
 #url_for allows generated urls based o  route names
 #session allows flask t remember admin logged in
 # generate password hashes oroginal password and doesnt store it
 #check password hash compares user password and stored password in database
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  #this secret key is for login and user remembring for next function


def get_db_connection():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conn
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in to access the admin area.", "error")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM articles ORDER BY publication_date DESC"
    )

    articles = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("home.html", articles=articles)


@app.route("/article/<int:article_id>")
def article(article_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM articles WHERE id = %s",
        (article_id,)
    )

    article = cur.fetchone()

    cur.close()
    conn.close()

    if article is None:
        return render_template("404.html"), 404

    return render_template("article.html", article=article)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()

        # Find the user
        cur.execute(
            "SELECT id, username, password FROM users WHERE username = %s",
            (username,)
        )

        user = cur.fetchone()

        # Close database connection
        cur.close()
        conn.close()

        # Check username and password
        if user and check_password_hash(user[2], password):

            # Remember the logged-in admin
            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect(url_for("dashboard"))

        # Wrong username or password
        flash("Incorrect username or password.", "error")

        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM articles ORDER BY publication_date DESC"  #shows all articles
    )

    articles = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        articles=articles,
        username=session["username"]
    ) #sends to HTMLpage


@app.route("/add-article", methods=["GET", "POST"])
@login_required
def add_article():
    # only logged admin can add article

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        publication_date = request.form["publication_date"]

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO articles (title, content, publication_date)
            VALUES (%s, %s, %s)
            """,
            (title, content, publication_date)
        )
        # this creates a new article

        conn.commit()
        # the saves changes permanently   WITHOUT"commit()" article may not be saved
        flash("Article published successfully!", "success")

        cur.close()
        conn.close()

       

        return redirect(url_for("dashboard")) #redirection to dashboard

    return render_template("add_article.html")

@app.route("/edit-article/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    # ONLY ADMIN LOGGED ANC EDIT OR ENTER EDIT PAGE

    conn = get_db_connection()

    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]
        publication_date = request.form["publication_date"]

        cur.execute(
            """
            UPDATE articles
            SET title = %s,
                content = %s,
                publication_date = %s
            WHERE id = %s
            """,
            (title, content, publication_date, article_id)
        )

        conn.commit()
        flash("Article updated successfully!", "success")

        cur.close()
        conn.close()

        return redirect(url_for("dashboard"))

    cur.execute(
        "SELECT * FROM articles WHERE id = %s",
        (article_id,)
    )

    article = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit_article.html",
        article=article
    )
@app.route("/delete-article/<int:article_id>", methods=["POST"])
@login_required
def delete_article(article_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM articles WHERE id = %s",
        (article_id,)
    )
    # pushes for any ID matching to be DELETED

    conn.commit()
    flash("Article deleted successfully!", "success")
# permentently makes this changes saves


    cur.close()
    conn.close()

    return redirect(url_for("dashboard"))
# returned to dashboard

@app.route("/logout")
def logout():

    session.clear()
    # sees logged session....intention to clear session and removelogin details

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)