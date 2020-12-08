def get_user(request):

    username_value = request.get_argument('username')
    password_value = request.get_argument('password')

    if ((username_value == 'nyc') and (password_value == 'iheartnyc')):
        return 1
    else:
        return None

login_url = '/login'
