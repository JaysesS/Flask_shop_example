from models import User

def get_user_info(username):
    user = User.query.filter_by(username = username).first()
    return {"email" : user.email, "money" : user.money, "phone" : user.phone, "adress" : user.adress}