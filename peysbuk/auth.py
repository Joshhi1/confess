from flask import (
  render_template,
  Blueprint,
  session,
  request,
  url_for,
  redirect
)
from .models import User, msg

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    check = User.login(username, password)
    if check["status"]:
      session['is_login'] = True
      session['data'] = check['msg']
      return redirect(url_for('view.account'))#render_template('pages/account.html', error={"check": False, "msg": 'Successfully'})
    else:
      return render_template('auth/login.html', error={"check": True, "msg": check['msg']})
  return render_template('auth/login.html', error={"check": False, "msg": None})

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('auth/signup.html',error={"check": False, "msg": None})
  user = request.form.get('username')
  passw = request.form.get('password')
  confirm = request.form.get('confirm')
  err = lambda x,y: {"check": x, "msg": y}
  if passw != confirm:
    return render_template('auth/signup.html', error=err(True, "Password dont match"))
  register = User.signup(user, passw)
  if register['status']:
    session['is_login'] = True
    session['data'] = register['msg']
    return render_template("pages/account.html", user=session['data'], messages=msg.get_messages(session['data']['username']))
  else:
    return render_template('auth/signup.html', error=err(True, register['msg']))

@auth.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('auth.login'))