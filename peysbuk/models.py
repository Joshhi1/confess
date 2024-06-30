from supabase import create_client
import uuid
from datetime import datetime

now = datetime.now()
dime = now.strftime("%-m/%-d/%Y - %-I:%M %p")

# Supabase database url & key
# lagay mo dito hunghang
DB_URL = ""
DB_KEY = ""

supabase = create_client(DB_URL, DB_KEY).table('ngl-account')
class User:
  def check(self, key, value):
    try:
      res = supabase.select('*').eq(key, value).execute()
      if res.data:
        return True
      else:
        return False
    except:
      return False
  def signup(self, username, password, role="user"):
    try:
      if self.check('username', username.lower().strip()):
        return {"status": False, "msg": 'Username already exists'}
      res = supabase.insert({"username": username.lower().strip(),"password": password,"role": role}).execute()
      if res.data:
        return {"status": True, "msg": res.data[0]}
      else:
        return {"status": False, "msg": 'failed to signup'}
    except Exception as e:
      return {"return": False, "msg": str(e)}
  def login(self, username, password):
    try:
      response = supabase.select('*').eq("username", username.lower().strip()).eq("password", password).execute()
      if response.data:
        return {"status": True, "msg": response.data[0]}
      else:
        return {"status": False, "mag": "Invalid username or password"}
    except Exception as e:
      return {"status": False, "msg": str(e)}
User = User()


anony = create_client(DB_URL, DB_KEY).table('messages')
class Message:
  def send_message(self, username, message):
    y = anony.insert({"for": username, "time": dime, "message": message}).execute()
    if y.data:
      return True
    else:
      return False
  def get_messages(self, username):
    ges = anony.select('*').eq("for", username).execute()
    return ges.data
  def del_message(self, id):
    g = anony.delete().eq("id", id).execute()
    return True

msg = Message()
