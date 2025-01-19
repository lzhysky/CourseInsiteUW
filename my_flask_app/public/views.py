# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user
from flask import jsonify
from my_flask_app.extensions import login_manager, cache
from my_flask_app.public.forms import LoginForm,LoginFormUW
from my_flask_app.user.forms import RegisterForm, RegisterFormUW, FeedbackForm
from my_flask_app.user.models import User, Course, Feedback
from my_flask_app.utils import flash_errors
from my_flask_app.extensions import db
from sqlalchemy import text

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.login"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)

@blueprint.route("/helloworld/")
def helloworld():
    return "Hello world!"


@blueprint.route("/index")
def index():
    return render_template("startbootstrap-sb-admin-2-gh-pages/index.html")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Home page."""
    form = LoginFormUW(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        current_app.logger.info("Hello from the home page POST!")
        if form.validate_on_submit():
            current_app.logger.info("Hello from the home page POST validate_on_submit!")
            login_user(form.user)
            current_app.logger.info("Hello from the home page POST validate_on_submit user login success!")
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("public.index")
            return redirect(redirect_url)
        else:
            # flash("username or password error", "error")
            flash_errors(form)
    return render_template("startbootstrap-sb-admin-2-gh-pages/login.html",form=form)


@blueprint.route("/reg", methods=["GET", "POST"])
def reg():
    form = RegisterFormUW(request.form)
    if form.validate_on_submit():
        print(User)

        User.create(
            first_name=form.firstName.data,
            last_name=form.lastName.data,
            username=form.email.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.login"))
    else:
        flash_errors(form)
    return render_template("startbootstrap-sb-admin-2-gh-pages/register.html", form=form)

@blueprint.route("/table")
def table():
    return render_template("startbootstrap-sb-admin-2-gh-pages/course.html")

@blueprint.route("/feedback")
def feedback():
    return render_template("startbootstrap-sb-admin-2-gh-pages/feedback.html")


@blueprint.route("/forgot-password")
def forgotPassword():
    return render_template("startbootstrap-sb-admin-2-gh-pages/forgot-password.html")


users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

@blueprint.route("/tables", methods=["GET"])
def tables():
    # """Home page."""
    # form = LoginFormUW(request.form)
    # current_app.logger.info("Hello from the home page!")
    # # Handle logging in
    # if request.method == "GET":
    #     current_app.logger.info("Hello from the home page POST!")
    #     if form.validate_on_submit():
    #         current_app.logger.info("Hello from the home page POST validate_on_submit!")
    #         login_user(form.user)
    #         current_app.logger.info("Hello from the home page POST validate_on_submit user login success!")
    #         flash("You are logged in.", "success")
    #         redirect_url = request.args.get("next") or url_for("public.index")
    #         return redirect(redirect_url)
    #     else:
    #         # flash("username or password error", "error")
    #         flash_errors(form)
    # return render_template("startbootstrap-sb-admin-2-gh-pages/login.html",form=form)
    # 获取分页后的用户数据

    courses = Course.get_all_data()
    print(courses)
    users = User.get_all_data()
    # print("courses =  + " + str(courses))
    # users = db.session.execute(text("select * from users"))
    # 将 User 对象列表转换为字典列表
    users_list = [user.to_dict() for user in users]
    # users_list = [
    #     {key: (value.decode('utf-8') if isinstance(value, bytes) else value) for key, value in row._mapping.items()}
    #     for row in users
    # ]
    courses_list = [course.to_dict() for course in courses]
    print("courses_list = " + str(courses_list))
    print("users_list = " + str(users_list))
    return jsonify(courses_list)



@blueprint.route("/feedbacks", methods=["GET"])
def feedbacks():
    # """Home page."""
    # form = LoginFormUW(request.form)
    # current_app.logger.info("Hello from the home page!")
    # # Handle logging in
    # if request.method == "GET":
    #     current_app.logger.info("Hello from the home page POST!")
    #     if form.validate_on_submit():
    #         current_app.logger.info("Hello from the home page POST validate_on_submit!")
    #         login_user(form.user)
    #         current_app.logger.info("Hello from the home page POST validate_on_submit user login success!")
    #         flash("You are logged in.", "success")
    #         redirect_url = request.args.get("next") or url_for("public.index")
    #         return redirect(redirect_url)
    #     else:
    #         # flash("username or password error", "error")
    #         flash_errors(form)
    # return render_template("startbootstrap-sb-admin-2-gh-pages/login.j",form=form)
    # 获取分页后的用户数据
    feedbacks = db.session.execute(text("select c.course_name,f.feedback,u.username from feedback f"
                                        " left join course c on f.course_id = c.id left join users u "
                                        "on f.user_id = u.id")).mappings()
    # feedbacks = Feedback.get_all_data()
    print(str(feedbacks))
    # users = User.get_all_data()
    # print("courses =  + " + str(courses))
    # users = db.session.execute(text("select * from users"))
    # 将 User 对象列表转换为字典列表
    feedback_list = [dict(feedback) for feedback in feedbacks]
    # users_list = [
    #     {key: (value.decode('utf-8') if isinstance(value, bytes) else value) for key, value in row._mapping.items()}
    #     for row in users
    # ]
    print("feedback_list = " + str(feedback_list))
    return jsonify(feedback_list)

@blueprint.route("/dashboard/summary", methods=["GET"])
def summary():

    coursesNumber = len(Course.get_all_data())
    feedbackNumber = len(Feedback.get_all_data())
    userNumber = len(User.get_all_data())



    data = {
        "courses_number": coursesNumber,
        "feedback_number": feedbackNumber,
        "comment_rate": "{:.2%}".format(feedbackNumber/coursesNumber),
        "users": userNumber,
        "real_name": "Welcome!"
    }
    print(str(data))
    return jsonify(data)


@blueprint.route("/dashboard/barchart", methods=["GET"])
def barchart():
    barchartData = db.session.execute(text("select f.course_id,c.course_name, count(*) as feedback_num from feedback f left join course c on f.course_id = c.id group by course_id order by count(*) desc limit 5;")).mappings().all()

    data = [dict(row) for row in barchartData]
    print(str(data))
    return jsonify(data)

@blueprint.route("/dashboard/piechart", methods=["GET"])
def piechart():
    piechartData = db.session.execute(text("select course_type,count(*) as course_type_num from course group by course_type;")).mappings().all()

    data = [dict(row) for row in piechartData]
    print(str(data))
    return jsonify(data)


@blueprint.route('/feedback/submit/', methods=['POST'])
def submit_feedback():
    print("Headers:", request.headers)
    print("Data:", request.data)

    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data received'}), 400

    return jsonify({'message': 'Data received!'})