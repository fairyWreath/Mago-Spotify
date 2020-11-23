''' extracting user data '''
def getUserImageUrl(sp):
    user_info = sp.me()
    url = user_info['images'][0]['url']
    return url