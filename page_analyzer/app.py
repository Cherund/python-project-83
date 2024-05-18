from flask import (Flask, render_template, get_flashed_messages, redirect,
                   flash, url_for, request)
from page_analyzer import db_manager as db
from dotenv import load_dotenv
import os
from page_analyzer.utils import (validate_url, normalize_url, get_url_info)


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template('index.html',)


@app.route('/urls')
def get_urls():
    # messages = get_flashed_messages(with_categories=True)
    # if messages:
    #     return render_template('index.html', messages=messages, ), 422
    urls_check = db.get_urls_last_check()
    return render_template('urls.html', urls_check=urls_check)


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    url = db.get_item(url_id)
    print(url)
    if not url:
        return render_template('errors/404.html'), 404
        # abort(404)
    else:
        checks = db.get_url_checks(url_id)
        messages = get_flashed_messages(with_categories=True)

        return render_template('url.html', url=url, checks=checks,
                               messages=messages)


@app.errorhandler(404)
def abort(error):
    return render_template('404.html'), 404



# @app.post('/url')
# def add_url():
#     url = request.form.get('url')
#     normal_url = normalize_url(url)
#     url_info = db.check_url_exists(normal_url)
#     message = check_url(normal_url, url_info)
#     flash(*message)
#     if 'danger' in message:
#         return redirect(url_for('get_urls'))
#     elif 'info' in message:
#     #if url_info:
#         url_id = url_info.id
#     else:
#         url_id = db.add_item(url)
#     # match message[1]:
#     #     case 'danger':
#     #         return redirect(url_for('get_urls'))
#     #     case 'info':
#     #         url_id = url_info.id
#     #     case _:
#     #         url_id = add_item(url)
#
#     return redirect(url_for('show_url_page', url_id=url_id))


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    validation_error = validate_url(normal_url)
    if validation_error:
        flash(validation_error, 'danger')
        return render_template('index.html'), 422

    url_info = db.check_url_exists(normal_url)
    if url_info:
        flash('Страница уже существует', 'info')
        url_id = url_info.id
    else:
        flash('Страница успешно добавлена', 'success')
        url_id = db.add_item(url)

    return redirect(url_for('show_url_page', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    url = db.get_item(url_id).name
    message, url_info = get_url_info(url)
    flash(*message)
    if url_info:
        db.add_check(url_id, url_info)

    return redirect(url_for('show_url_page', url_id=url_id))
