from typing import List
from models import User

def search_user_by_email(userlist: List, id:int) -> User|None:
    for u in userlist:
        if u.id == id:
            return u
        else:
            return None
        
def update_user_in_users(userlist: List, user:User):
    for u in userlist:
        if u.id == user.id:
            userlist.remove(u)
            userlist.append(user)
            