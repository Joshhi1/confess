from flask import (
  render_template,
  Blueprint,
  session,
  redirect,
  url_for,
  request,
  jsonify
)
import random
from .models import msg, User

view = Blueprint('view', __name__)

@view.route('/')
def root():
  log = True if 'is_login' in session else False
  if log:
    return redirect(url_for('view.account'))
  return redirect(url_for('auth.login'))

@view.route('/account', methods=['GET'])
def account():
  log = True if 'is_login' in session else False
  if not log:
    return redirect(url_for('auth.login'))
  data = session['data']
  messages = []
  xyz_a = msg.get_messages(data['username'])
  for _ in xyz_a:
    i = _['message'].replace('\r\n', '<br>')
    messages.append({"message": i, "time": _['time'], "id": _['id']})
  return render_template('pages/account.html', user=data, messages=messages)

@view.route('/<username>', methods=['GET', 'POST'])
def sendMessage(username):
  x = User.check("username", username.lower().strip())
  if not x == True:
    return render_template('404.html'),400
  if request.method == 'POST':
    mess = request.form.get('text')
    send = msg.send_message(username, mess)
    if send:
      return render_template('pages/send_message.html', username=username, is_success=True)
    else:
      return render_template('pages/send_message.html', username=username, is_success=False)
  return render_template('pages/send_message.html', username=username, is_success=False)

@view.route('/fod/delete_msg',methods=['POST'])
def delete_msg():
  if request.method == 'POST':
    id = request.json.get('id')
    msg.del_message(id)
    print(id)
    return jsonify({"status": True})
  return render_template('pages/account.html')