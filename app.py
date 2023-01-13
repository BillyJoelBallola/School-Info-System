import os
import random
from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret'

UPLOAD_FOLDER = "static/uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'billyjoel'
app.config['MYSQL_DB'] = 'school-info-system'


mysql = MySQL(app)


def userlogout(loggedIn, username):
    session.pop(loggedIn, None)
    session.pop(username, None)


def get_announcement_id(announcement_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM announcement WHERE id = %s", (announcement_id,))
    announcement = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    if announcement is None:
        abort(404)

    return announcement


def get_article_id(article_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM article WHERE id = %s", (article_id,))
    article = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    if article is None:
        abort(404)

    return article


def get_event_id(event_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM event WHERE id = %s", (event_id,))
    event = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    if event is None:
        abort(404)

    return event


def get_all_items(table_name):
    cur = mysql.connection.cursor()
    get_all_query = "SELECT * FROM " + table_name + " ORDER BY id DESC"
    cur.execute(get_all_query)
    articles = cur.fetchall()

    if articles is None:
        abort(404)

    return articles


@app.route("/admin/delete/article", methods=['POST', 'GET'])
def delete_article():
    if request.method == 'POST':
        item_id = request.form['item_id']

        article = get_article_id(item_id)

        os.remove(os.path.join(
            app.config['UPLOAD_FOLDER'], article[3]))

        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM article WHERE id = %s"
        cur.execute(delete_query, (item_id,))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('articles_admin'))


@app.route("/admin/delete/event", methods=['POST', 'GET'])
def delete_event():
    if request.method == 'POST':
        item_id = request.form['item_id']

        event = get_event_id(item_id)

        os.remove(os.path.join(
            app.config['UPLOAD_FOLDER'], event[5]))

        cur = mysql.connection.cursor()
        delete_query = "DELETE FROM event WHERE id = %s"
        cur.execute(delete_query, (item_id,))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('events_admin'))


def is_accessible(whos):
    if whos in session:
        return True
    else:
        abort(403)


# logout
@app.route('/logout_parent')
def logout_parent():
    userlogout('logged_in_parent', 'parent_login')
    return redirect(url_for('login'))


@app.route('/logout_teacher')
def logout_teacher():
    userlogout('logged_in_teacher', 'teacher_login')
    return redirect(url_for('login'))


@app.route('/logout_admin')
def logout_admin():
    userlogout('logged_in_admin', 'admin_login')
    return redirect(url_for('login'))


def getAll(sql_table):
    cur = MySQL.connect.cursor()
    getAllData = cur.execute(f"SELECT * FROM {sql_table} ORDER BY id")
    getAllData.fetchAll()
    cur.close()
    return getAllData


@ app.route('/')
def index():
    return render_template('index.html')


# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        accType = request.form['accType']

        if accType == 'Parent':
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s AND role = 'Parent' AND status = '1'", (username, password,))
            getUser = cur.fetchall()

            if getUser:
                session['logged_in_parent'] = True
                session['parent_login'] = getUser[0]
                cur.close()

                return redirect(url_for('home_parent'))
            else:
                return abort(404)

        elif accType == 'Teacher':
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username =  %s AND password = %s AND role = 'Teacher' AND status = '1'", (username, password,))
            getUser = cur.fetchall()

            if getUser:
                session['logged_in_teacher'] = True
                session['teacher_login'] = getUser[0]
                cur.close()

                return redirect(url_for('home_teacher'))
            else:
                return abort(404)

        elif accType == 'Admin':
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s AND role = 'Admin' AND status = '1'", (username, password,))
            getUser = cur.fetchall()

            if getUser:
                session['logged_in_admin'] = True
                session['admin_login'] = getUser[0]
                cur.close()

                return redirect(url_for('home_admin'))
            else:
                return abort(404)

    return render_template('auth/login.html')


# register
@ app.route('/register', methods=['POST', 'GET'])
def register():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        childFname = request.form['childFname']
        childLname = request.form['childLname']
        childMname = request.form['childMname']

        parentFirstName = request.form['parentFirstName']
        parentLastName = request.form['parentLastName']
        username = request.form['username']
        createPassword = request.form['createPassword']

        cur.execute(
            f"SELECT * FROM student WHERE fname LIKE '%{childFname}' AND lname LIKE '%{childLname}' AND mname LIKE '%{childMname}'")
        student_data = cur.fetchall()

        if len(student_data) <= 0:
            return abort(404)

        insertParentRegistration_query = "INSERT INTO users (fname, lname, username, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(insertParentRegistration_query, (parentFirstName,
                                                     parentLastName,
                                                     username,
                                                     createPassword,
                                                     'Parent',
                                                     '1'))
        mysql.connection.commit()

    return render_template('auth/register.html')


# parents home page
@ app.route('/parent/home')
def home_parent():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        getOneAnnouncement_query = "SELECT * FROM `announcement` WHERE `status` =  'Posted' ORDER BY id DESC LIMIT 1"
        cur.execute(getOneAnnouncement_query)
        getOneAnnouncement = cur.fetchall()

        getArticles_query = "SELECT * FROM `article` ORDER BY id DESC LIMIT 5 "
        cur.execute(getArticles_query)
        getArticles = cur.fetchall()

        getEvents_query = "SELECT * FROM `event` ORDER BY id DESC LIMIT 3 "
        cur.execute(getEvents_query)
        getEvents = cur.fetchall()

    return render_template('parent/home.html', username=session['parent_login'][1], announcements=getOneAnnouncement, articles=getArticles, events=getEvents)


@ app.route('/parent/about')
def about_parent():
    is_accessible('logged_in_parent')
    return render_template('parent/about.html')


@ app.route('/parent/events')
def events_parent():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        getAllEvents_query = "SELECT * FROM `event` ORDER BY id DESC"
        cur.execute(getAllEvents_query)
        getAllEvents = cur.fetchall()

    return render_template('parent/events.html', events=getAllEvents)


@ app.route('/parent/articles')
def articles_parent():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        getAllArticles_query = "SELECT * FROM `article` ORDER BY id DESC"
        cur.execute(getAllArticles_query)
        getAllArticles = cur.fetchall()

    return render_template('parent/articles.html', articles=getAllArticles)


@ app.route('/parent/announcements')
def announcements_parent():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        getAllAnnouncement_query = "SELECT * FROM `announcement` WHERE `status` =  'Posted' ORDER BY id DESC"
        cur.execute(getAllAnnouncement_query)
        getAllAnnouncement = cur.fetchall()

    return render_template('parent/announcements.html', announcements=getAllAnnouncement)


@ app.route('/parent/faculty')
def faculty_parent():
    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        faculty_data = (
            ('Billy Joel Ballola', 'Principal'),
            ('Joel Billy Ballola', 'Math Teacher'),
            ('Jay Ballola', 'P.E Teacher'),
            ('Bjay Ballola', 'English Teacher'),
            ('Jayb Ballola', 'Filipino Teacher'),
            ('Jay jay Ballola', 'History Teacher'),
            ('Joel jay Ballola', 'ESP Teacher'),
            ('Joel jay Ballola', 'MAPEH Teacher'),
        )

    return render_template('parent/faculty.html', data=faculty_data)


@ app.route('/parent/account/username', methods=['POST', 'GET'])
def account_username_parent():
    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        cur = mysql.connection.cursor()
        parent_id = session['parent_login'][0]
        parent_username = session['parent_login'][3]
        parent_pass = session['parent_login'][4]

        if request.method == 'POST':
            new_username = request.form['newUsername']
            password = request.form['password']

            if parent_pass != password:
                return abort(404)

            cur.execute(
                "UPDATE users SET username = %s WHERE id = %s", (new_username, parent_id))
            mysql.connection.commit()

            return redirect(url_for('logout_parent'))

    return render_template('parent/account/username-form.html', parent_username=parent_username)


@ app.route('/parent/account/password', methods=['POST', 'GET'])
def account_password_parent():
    if not is_accessible('logged_in_parent'):
        is_accessible('logged_in_parent')
    else:
        cur = mysql.connection.cursor()
        parent_id = session['parent_login'][0]
        parent_pass = session['parent_login'][4]

        if request.method == 'POST':
            new_password = request.form['confirmPassword']

            cur.execute("UPDATE users SET password = %s WHERE id = %s",
                        (new_password, parent_id,))
            mysql.connection.commit()

            return redirect(url_for('logout_parent'))

    return render_template('parent/account/password-form.html', parent_pass=parent_pass)


# teacher home page
@ app.route('/teacher/home')
def home_teacher():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        getOneAnnouncement_query = "SELECT * FROM `announcement` WHERE `status` = 'Posted' LIMIT 1"
        cur.execute(getOneAnnouncement_query)
        getOneAnnouncement = cur.fetchall()

        getEvents_query = "SELECT * FROM `event` ORDER BY id DESC LIMIT 3"
        cur.execute(getEvents_query)
        getEvents = cur.fetchall()

        getArticles_query = "SELECT * FROM `article` ORDER BY id DESC LIMIT 5"
        cur.execute(getArticles_query)
        getArticles = cur.fetchall()

    return render_template('teacher/home.html', username=session['teacher_login'][1], announcements=getOneAnnouncement, events=getEvents, articles=getArticles)


@ app.route('/teacher/events')
def events_teacher():
    cur = mysql.connection.cursor()

    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        getAllEvents_query = "SELECT * FROM `event` ORDER BY id DESC"
        cur.execute(getAllEvents_query)
        getAllEvents = cur.fetchall()

    return render_template('teacher/events.html', events=getAllEvents)


@ app.route('/teacher/articles')
def articles_teacher():
    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        cur = mysql.connection.cursor()
        getAllArticles_query = "SELECT * FROM `article` ORDER BY id DESC"
        cur.execute(getAllArticles_query)
        getAllArticles = cur.fetchall()

    return render_template('teacher/articles.html', articles=getAllArticles)


@app.route('/teacher/announcements/archive/<int:announcement_id>', methods=['POST', 'GET'])
def announcement_teacher_arvhive(announcement_id):
    cur = mysql.connection.cursor()
    archiveAnnouncement_query = f"UPDATE `announcement` SET `status`='Archive' WHERE id = {announcement_id}"
    cur.execute(archiveAnnouncement_query)
    mysql.connection.commit()

    return redirect(url_for('announcements_teacher'))


@ app.route('/teacher/announcements', methods=['POST', 'GET'])
def announcements_teacher():
    cur = mysql.connection.cursor()
    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        if request.method == 'POST':
            user_id = session['teacher_login'][0]
            title = request.form['title']
            audience = request.form['audience']
            purpose = request.form['purpose']
            place = request.form['place']
            date = request.form['date']

            insert_query = "INSERT INTO `announcement`(`title`, `audience`, `purpose`, `place`, `date`, `status`, `uid`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, (title, audience,
                        purpose, place, date, 'Posted', user_id))
            mysql.connection.commit()

        getYourAnnouncement_query = f"SELECT a.id, a.title, a.audience, a.purpose, a.place, a.date FROM users u JOIN announcement a ON u.id=a.uid WHERE a.uid = {session['teacher_login'][0]} AND a.status = 'Posted' ORDER BY id DESC"
        cur.execute(getYourAnnouncement_query)
        getYourAnnouncement = cur.fetchall()

        getAllAnnouncement_query = f"SELECT * FROM `announcement` WHERE `status` = 'Posted' AND `uid` != {session['teacher_login'][0]} ORDER BY id DESC"
        cur.execute(getAllAnnouncement_query)
        getAllAnnouncement = cur.fetchall()

    return render_template('teacher/announcements.html',  announcements=getAllAnnouncement, announcement=getYourAnnouncement)


@ app.route('/teacher/account/username', methods=['POST', 'GET'])
def account_username_teacher():
    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        cur = mysql.connection.cursor()
        teacher_id = session['teacher_login'][0]
        teacher_username = session['teacher_login'][3]
        teacher_pass = session['teacher_login'][4]

        if request.method == 'POST':
            newUsername = request.form['newUsername']
            password = request.form['password']

            if teacher_pass != password:
                return abort(404)

            cur.execute(
                "UPDATE users SET username = %s WHERE id = %s", (newUsername, teacher_id))
            mysql.connection.commit()

            return redirect(url_for('logout_teacher'))

    return render_template('teacher/account/username-form.html', teacher_username=teacher_username)


@ app.route('/teacher/account/password', methods=['POST', 'GET'])
def account_password_teacher():
    if not is_accessible('logged_in_teacher'):
        is_accessible('logged_in_teacher')
    else:
        cur = mysql.connection.cursor()
        teacher_id = session['teacher_login'][0]
        teacher_pass = session['teacher_login'][4]

        if request.method == 'POST':
            password = request.form['confirmPassword']

            cur.execute(
                "UPDATE users SET password = %s WHERE id = %s", (password, teacher_id))
            mysql.connection.commit()

            return redirect(url_for('logout_teacher'))

    return render_template('teacher/account/password-form.html', teacher_pass=teacher_pass)


# admin home page
@ app.route('/admin/home')
def home_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        cur.execute(
            '''
                SELECT COUNT(*) AS dashboard FROM event
                UNION ALL
                SELECT COUNT(*) AS dashboard FROM article
                UNION ALL
                SELECT COUNT(*) AS dashboard FROM announcement WHERE status = 'Posted'
                UNION ALL
                SELECT COUNT(*) AS dashboard FROM users
            '''
        )
        dashboard_data = cur.fetchall()

        cur.execute("SELECT * FROM event ORDER BY id DESC LIMIT 3")
        event_data = cur.fetchall()

        cur.execute("SELECT * FROM article ORDER BY id DESC LIMIT 3")
        article_data = cur.fetchall()

    return render_template('admin/home.html', username=session['admin_login'][1], dashboard_data=dashboard_data, event_data=event_data, article_data=article_data)


@app.route('/admin/article/view/<int:article_id>')
def admin_article_view(article_id):
    article = get_article_id(article_id)
    articles = get_all_items('article')

    return render_template('admin/articles.html', username=session['admin_login'][1], article=article, articles=articles)


@ app.route("/admin/articles/edit_save/<int:article_id>", methods=['POST', 'GET'])
def admin_edit_article_save(article_id):
    cur = mysql.connection.cursor()
    article_title = request.form['title']
    article_content = request.form['content']
    article_date = request.form['date']
    ranNum = random.random()

    if len(request.files) == 0:
        article_img = request.form['current_img']
    else:
        article_img = request.files['img']
        article_img_name = secure_filename(f'{ranNum}{article_img.filename}')

        article_img.save(os.path.join(
            app.config['UPLOAD_FOLDER'], article_img_name))

        os.remove(os.path.join(
            app.config['UPLOAD_FOLDER'], request.form['current_img']))

        article_img = article_img_name

    edit_article_query = "UPDATE `article` SET `title`=%s, `content`=%s, `date`=%s, `img`=%s WHERE `id` = %s"
    cur.execute(edit_article_query, (article_title,
                article_content, article_date, article_img, article_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("articles_admin"))


@ app.route('/admin/articles/edit/<int:article_id>', methods=['POST', 'GET'])
def articles_admin_edit(article_id):
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        article = get_article_id(article_id)

    return render_template('admin/articles_edit.html', article=article)


@ app.route('/admin/articles', methods=['POST', 'GET'])
def articles_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()
        articles = get_all_items('article')

        if request.method == 'POST':
            article_title = request.form['title']
            article_content = request.form['content']
            article_date = request.form['date']
            article_img = request.files['img']
            randNum = random.random()

            article_img_name = secure_filename(
                f'{randNum}{article_img.filename}')
            article_img.save(os.path.join(
                app.config['UPLOAD_FOLDER'], article_img_name))

            add_article_query = "INSERT INTO `article` (`title`, `content`, `img`, `date`) VALUES (%s, %s, %s, %s)"
            cur.execute(add_article_query, (article_title,
                        article_content, article_img_name, article_date))
            mysql.connection.commit()

    return render_template('admin/articles.html', username=session['admin_login'][1], articles=articles)


@ app.route('/admin/events', methods=['POST', 'GET'])
def events_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()
        events = get_all_items('event')

        if request.method == 'POST':
            event_title = request.form['title']
            event_content = request.form['content']
            event_date = request.form['date']
            event_img = request.files['img']
            ranNum = random.random()

            event_img_name = secure_filename(f'{ranNum}{event_img.filename}')
            event_img.save(os.path.join(
                app.config['UPLOAD_FOLDER'], event_img_name))

            add_event_query = "INSERT INTO `event` (`title`, `content`, `img`, `date`) VALUES (%s, %s, %s, %s)"
            cur.execute(add_event_query, (event_title,
                        event_content, event_img_name, event_date))
            mysql.connection.commit()

    return render_template('admin/events.html', username=session['admin_login'][1], events=events)


@app.route('/admin/event/view/<int:event_id>')
def admin_event_view(event_id):
    event = get_event_id(event_id)
    events = get_all_items('event')

    return render_template('admin/events.html', event=event, events=events)


@ app.route("/admin/events/edit_save/<int:event_id>", methods=['POST', 'GET'])
def admin_edit_event_save(event_id):
    cur = mysql.connection.cursor()
    event_title = request.form['title']
    event_content = request.form['content']
    event_date = request.form['date']
    ranNum = random.random()

    if len(request.files) == 0:
        event_img = request.form['current_img']
    else:
        event_img = request.files['img']
        event_img_name = secure_filename(f'{ranNum}{event_img.filename}')

        event_img.save(os.path.join(
            app.config['UPLOAD_FOLDER'], event_img_name))

        os.remove(os.path.join(
            app.config['UPLOAD_FOLDER'], request.form['current_img']))

        event_img = event_img_name

    edit_event_query = "UPDATE `event` SET `title`=%s, `content`=%s, `date`=%s, `img`=%s WHERE `id` = %s"
    cur.execute(edit_event_query, (event_title,
                event_content, event_date, event_img, event_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("events_admin"))


@ app.route('/admin/events/edit/<int:event_id>', methods=['POST', 'GET'])
def events_admin_edit(event_id):
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        event = get_event_id(event_id)

    return render_template('admin/events_edit.html', event=event)


@app.route('/admin/announcements/archive/<int:announcement_id>', methods=['POST', 'GET'])
def announcement_admin_arvhive(announcement_id):
    cur = mysql.connection.cursor()
    archiveAnnouncement_query = f"UPDATE `announcement` SET `status`='Archive' WHERE id = {announcement_id}"
    cur.execute(archiveAnnouncement_query)
    mysql.connection.commit()

    return redirect(url_for('announcements_admin'))


@app.route('/admin/announcement/view/<int:announcement_id>')
def admin_announcement_view(announcement_id):
    announcement = get_announcement_id(announcement_id)
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM announcement WHERE status = 'Posted' ORDER BY id DESC")
    announcements = cur.fetchall()

    return render_template('admin/announcements.html', announcement=announcement, announcements=announcements)


@app.route('/admin/announcements/archive')
def announcements_archives_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM announcement WHERE status = 'Archive' ORDER BY id DESC")
        announcement_archives = cur.fetchall()

    return render_template('admin/announcements_archives.html', announcement_archives=announcement_archives)


@app.route('/admin/announcements', methods=['POST', 'GET'])
def announcements_admin():
    cur = mysql.connection.cursor()
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        if request.method == 'POST':
            user_id = session['admin_login'][0]
            title = request.form['title']
            purpose = request.form['purpose']
            audience = request.form['audience']
            place = request.form['place']
            date = request.form['date']

            insertAnnouncement_query = "INSERT INTO `announcement` (`title`, `audience`, `purpose` , `place`, `date`, `status`, `uid`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insertAnnouncement_query,
                        (title, audience, purpose,  place, date, 'Posted', user_id))
            mysql.connection.commit()

        getAllAnnouncements_query = "SELECT * FROM announcement WHERE `status` = 'Posted' ORDER BY id DESC"
        cur.execute(getAllAnnouncements_query)
        getAllAnnouncements = cur.fetchall()

    return render_template('admin/announcements.html', username=session['admin_login'][1], announcements=getAllAnnouncements)


@ app.route('/admin/students', methods=['POST', 'GET'])
def students_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        cur.execute('''
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '1' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '2' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '3' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '4' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '5' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '6' AND status = '1'
        ''')
        student_num = cur.fetchall()

        cur.execute('''
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '1' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '2' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '3' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '4' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '5' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '6' AND status = '2'
        ''')
        archives_student_num = cur.fetchall()

        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            mname = request.form['mname']
            dob = request.form['dob']
            age = request.form['age']
            lrn = request.form['lrn']
            grade = request.form['grade']
            section = request.form['section']
            address = request.form['address']

            cur.execute(
                f'SELECT COUNT(*) FROM `student` WHERE lrn = {str(lrn)}')
            stud = cur.fetchall()

            if stud[0][0] != 0:
                return abort(404)

            inserStudentInfo_query = "INSERT INTO `student`(`fname`, `lname`, `mname`, `dob`, `age`, `LRN`, `grade`, `section`, `address`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cur.execute(inserStudentInfo_query, (fname, lname, mname,
                        dob, age, lrn, grade, section, address, '1'))
            mysql.connection.commit()

    return render_template('admin/students.html', username=session['admin_login'][1], students_num=student_num, archives_num=archives_student_num)


@ app.route('/admin/students/update', methods=['POST', 'GET'])
def students_admin_update():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            stud_id = request.form['stud_id']
            fname = request.form['fname']
            lname = request.form['lname']
            mname = request.form['mname']
            dob = request.form['dob']
            age = request.form['age']
            lrn = request.form['lrn']
            grade = request.form['grade']
            section = request.form['section']
            address = request.form['address']

            updateStudentInfo_query = "UPDATE `student` SET `fname` = %s, `lname` = %s, `mname` = %s, `dob` = %s, `age` = %s, `LRN` = %s, `grade` = %s, `section` = %s, `address` = %s WHERE id = %s"

            cur.execute(updateStudentInfo_query, (fname, lname, mname,
                        dob, age, lrn, grade, section, address, stud_id))
            mysql.connection.commit()

    return redirect(url_for('students_admin'))


@ app.route('/admin/students/edit/<int:stud_lrn>', methods=['POST', 'GET'])
def students_admin_edit(stud_lrn):
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        cur.execute('''
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '1' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '2' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '3' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '4' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '5' AND status = '1'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '6' AND status = '1'
        ''')
        student_num = cur.fetchall()

        cur.execute('''
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '1' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '2' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '3' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num FROM student WHERE grade = '4' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '5' AND status = '2'
            UNION ALL
            SELECT COUNT(*) AS students_num  FROM student WHERE grade = '6' AND status = '2'
        ''')
        archives_student_num = cur.fetchall()

        cur.execute(f"SELECT * FROM student WHERE lrn = {stud_lrn}")
        student_info = cur.fetchall()

        if student_info == None:
            return abort(404)

    return render_template('admin/students.html', students_num=student_num, archives_num=archives_student_num, student_info=student_info[0])


@app.route('/admin/students/archive/<int:student_id>', methods=['POST', 'GET'])
def student_archive(student_id):
    cur = mysql.connection.cursor()

    archive_grade_one = f"UPDATE student set status = '2' WHERE id = {student_id}"
    cur.execute(archive_grade_one)
    mysql.connection.commit()

    return redirect(url_for('students_admin'))


# grade 1
@ app.route('/admin/students/grade-one/view/<int:student_id>')
def students_grade_one_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '1' AND status = '1' ORDER BY section")
    grade_one = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '1' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-one/grade-one.html', grade_one=grade_one, student=student)


@ app.route('/admin/students/grade-one/archives')
def students_grade_one_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '1' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeOne_archives = cur.fetchall()

    return render_template('admin/grade/grade-one/grade-one-archives.html', grade_one=gradeOne_archives)


@ app.route('/admin/students/grade-one')
def students_grade_one():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '1' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeOne_student = cur.fetchall()

    return render_template('admin/grade/grade-one/grade-one.html', grade_one=gradeOne_student)


# grade 2
@ app.route('/admin/students/grade-two/view/<int:student_id>')
def students_grade_two_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '2' AND status = '1' ORDER BY section")
    grade_two = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '2' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-two/grade-two.html', grade_two=grade_two, student=student)


@ app.route('/admin/students/grade-two-archives')
def students_grade_two_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '2' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeTwo_archives = cur.fetchall()

    return render_template('admin/grade/grade-two/grade-two-archives.html', grade_two=gradeTwo_archives)


@ app.route('/admin/students/grade-two')
def students_grade_two():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '2' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeTwo_student = cur.fetchall()

    return render_template('admin/grade/grade-two/grade-two.html', grade_two=gradeTwo_student)


# grade 3
@ app.route('/admin/students/grade-three/view/<int:student_id>')
def students_grade_three_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '3' AND status = '1' ORDER BY section")
    grade_three = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '3' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-three/grade-three.html', grade_three=grade_three, student=student)


@ app.route('/admin/students/grade-three/archives')
def students_grade_three_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '3' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeThree_archives = cur.fetchall()

    return render_template('admin/grade/grade-three/grade-three-archives.html', grade_three=gradeThree_archives)


@ app.route('/admin/students/grade-three')
def students_grade_three():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '3' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeThree_student = cur.fetchall()

    return render_template('admin/grade/grade-three/grade-three.html', grade_three=gradeThree_student)


# grade 4
@ app.route('/admin/students/grade-four/view/<int:student_id>')
def students_grade_four_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '4' AND status = '1' ORDER BY section")
    grade_four = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '4' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-four/grade-four.html', grade_four=grade_four, student=student)


@ app.route('/admin/students/grade-four/archives')
def students_grade_four_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '4' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeFour_archives = cur.fetchall()

    return render_template('admin/grade/grade-four/grade-four-archives.html', grade_four=gradeFour_archives)


@ app.route('/admin/students/grade-four')
def students_grade_four():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '4' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeFour_student = cur.fetchall()

    return render_template('admin/grade/grade-four/grade-four.html', grade_four=gradeFour_student)


# grade 5
@ app.route('/admin/students/grade-five/view/<int:student_id>')
def students_grade_five_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '5' AND status = '1' ORDER BY section")
    grade_five = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '5' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-five/grade-five.html', grade_five=grade_five, student=student)


@ app.route('/admin/students/grade-five/archives')
def students_grade_five_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '5' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeFive_archives = cur.fetchall()

    return render_template('admin/grade/grade-five/grade-five-archives.html', grade_five=gradeFive_archives)


@ app.route('/admin/students/grade-five')
def students_grade_five():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '5' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeFive_student = cur.fetchall()

    return render_template('admin/grade/grade-five/grade-five.html', grade_five=gradeFive_student)


# grade 6
@ app.route('/admin/students/grade-six/view/<int:student_id>')
def students_grade_six_view(student_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM student WHERE grade = '6' AND status = '1' ORDER BY section")
    grade_six = cur.fetchall()

    cur.execute(
        f"SELECT * FROM student WHERE grade = '6' AND status = '1' AND id = {student_id} ORDER BY section")
    student = cur.fetchone()

    return render_template('admin/grade/grade-six/grade-six.html', grade_six=grade_six, student=student)


@ app.route('/admin/students/grade-six/archives')
def students_grade_six_archives():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '2' AND status = '2' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeSix_archives = cur.fetchall()

    return render_template('admin/grade/grade-six/grade-six-archives.html', grade_six=gradeSix_archives)


@ app.route('/admin/students/grade-six')
def students_grade_six():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        getAllInfo_query = "SELECT * FROM student WHERE grade = '6' AND status = '1' ORDER BY section"
        cur.execute(getAllInfo_query)
        gradeSix_student = cur.fetchall()

    return render_template('admin/grade/grade-six/grade-six.html', grade_six=gradeSix_student)


# faculty
@ app.route('/admin/faculty', methods=['POST', 'GET'])
def faculty_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            fname = request.form['teacher_fname']
            lname = request.form['teacher_lname']
            dob = request.form['teacher_dob']
            email = request.form['teacher_email']
            address = request.form['teacher_address']
            contact = request.form['teacher_contact']

            cur.execute(
                f"SELECT * FROM teacher WHERE emailAddress = '{email}'")
            teachersEmail = cur.fetchall()

            if teachersEmail:
                return abort(404)

            insertTeacher_query = "INSERT INTO teacher (fname, lname, dob, emailAddress, address, contact, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insertTeacher_query,
                        (fname, lname, dob, email, address, contact, '1'))

            # create account for teacher
            account = dob + "-SIS"
            createAcc_query = "INSERT INTO users (fname, lname, username, password, role, status) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(createAcc_query,
                        (fname, lname, account, account, 'Teacher', '1'))

            mysql.connection.commit()

        getAllTeacher_query = "SELECT * FROM teacher WHERE status = '1' ORDER BY id DESC"
        cur.execute(getAllTeacher_query)
        teachers = cur.fetchall()

    return render_template('admin/faculty.html', teachers=teachers)


@ app.route('/admin/faculty/archive/<int:teacher_id>', methods=['POST', 'GET'])
def faculty_archives(teacher_id):
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        cur.execute(f"UPDATE teacher SET status = '2' WHERE id ={teacher_id}")
        cur.execute(f"UPDATE users SET status = '2' WHERE id ={teacher_id}")
        mysql.connection.commit()

    return redirect(url_for('faculty_archives_admin'))


@ app.route('/admin/faculty/archives')
def faculty_archives_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM teacher WHERE status = '2' ORDER BY id DESC")
        faculty_archives = cur.fetchall()
        mysql.connection.commit()

    return render_template('admin/faculty_archives.html', archives=faculty_archives)


@ app.route('/admin/faculty/view/<int:teacher_id>')
def faculty_view_admin(teacher_id):
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM teacher WHERE status = '1' ORDER BY id DESC")
    teachers = cur.fetchall()

    cur.execute(
        f"SELECT * FROM teacher WHERE id = {teacher_id}")
    teacher = cur.fetchone()

    return render_template('admin/faculty.html', teachers=teachers, teacher=teacher)


@ app.route('/admin/settings', methods=['POST', 'GET'])
def settings_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()
        teacher_id = session['admin_login'][0]
        teacher_username = session['admin_login'][3]
        teacher_password = session['admin_login'][4]

        if request.method == 'POST':
            new_username = request.form['newUsername']
            password = request.form['password']

            if teacher_password != password:
                return abort(404)

            cur.execute("UPDATE users SET username = %s WHERE id = %s",
                        (new_username, teacher_id))
            mysql.connection.commit()

            return redirect(url_for('logout_admin'))

    return render_template('admin/account/username.html', teacher_username=teacher_username)


@ app.route('/admin/settings/password', methods=['POST', 'GET'])
def settings_password_admin():
    if not is_accessible('logged_in_admin'):
        is_accessible('logged_in_admin')
    else:
        cur = mysql.connection.cursor()
        teacher_id = session['admin_login'][0]
        teacher_password = session['admin_login'][4]

        print(teacher_password)

        if request.method == 'POST':
            new_password = request.form['confirmPassword']

            cur.execute("UPDATE users SET password = %s WHERE id = %s",
                        (new_password, teacher_id))
            mysql.connection.commit()

            return redirect(url_for('logout_admin'))

    return render_template('admin/account/password.html', teacher_password=teacher_password)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
