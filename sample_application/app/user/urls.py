from views import *

urls = [
  ('/user/', ['POST'], UserView.as_view('create_user')),
  ('/user/<string:user_id>/', ['GET', 'PUT'], UserView.as_view('user_updates')),
]
