import requests
import urllib

# storing access token to app in a variable
token = '3516265067.a606bd5.6ac0cfccc602439c9551e758fbc87212'
# sandbox admin:im_vipul
# sandbox users:priyanka_verma96 and royalmohit

# this is the base url to access data from insta
base_url = 'https://api.instagram.com/v1/'


# Function declaration to get your own info
def self_info():
    request_url = base_url + 'users/self/?access_token=%s' % token
    print 'GET request url is %s' %request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' %user_info['data']['username']
            print 'No. of Followers:%s' %user_info['data']['counts']['followed_by']
            print 'No. of people you follow:%s' % user_info['data']['counts']['follows']
            print 'No. of posts:%s' % user_info['data']['counts']['media']
        else:
            print 'You don\'t exist or not have signup on instagram or you don\'t have any data'
            print 'Link for signup : https://www.instagram.com'
    elif 100 < user_info['meta']['code'] < 200:
        print 'Informational 1xx'
    elif 200 < user_info['meta']['code'] < 300:
        print 'Success 2xx. But it is not 200, so try again'
    elif 300 <= user_info['meta']['code'] < 400:
        print ' Redirection 3xx'
    elif 400 <= user_info['meta']['code'] < 500:
        print 'Client Error 4xx'
    elif 500 < user_info['meta']['code'] < 600:
        print 'Server Error 5xx'
    else:
        print 'Error in meta code, search on https://httpstatuses.com/ for furthermore details'


# Function declaration to get the ID of a user by username
def get_user_id(username):
    request_url = base_url + 'users/search/?q=%s&access_token=%s' % (username, token)
    print 'GET request url is %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received'
        exit(20)


# Function declaration to get the info of a user by username
def get_user_info():
    username = raw_input("Enter the username of person you want information")
    user_id = get_user_id(username)
    if user_id is None:
        print 'User does not exist!'
        exit()
    request_url = base_url + 'users/%s/?access_token=%s' % (user_id, token)
    print 'GET request url is %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % user_info['data']['username']
            print 'No. of Followers:%s' % user_info['data']['counts']['followed_by']
            print 'No. of people you follow:%s' % user_info['data']['counts']['follows']
            print 'No. of posts:%s' % user_info['data']['counts']['media']
        else:
            print 'There is no data for user'
    else:
        print 'Status code other than 200 received'


# Function declaration to get your recent post
def get_own_post():
    request_url = base_url + 'users/self/media/recent/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            img_name = media_info['data'][0]['id'] + '.png'
            img_url = media_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)
            print 'Your image is downloaded'
        else:
            print 'Post does\'nt exist'
    else:
        print 'Other than 200'


# Function declaration to get the recent post of a user by username
def get_user_post(username):
    user_id = get_user_id(username)
    request_url = base_url + 'users/%s/media/recent/?access_token=%s' % (user_id, token)
    print 'GET request url is %s' % request_url
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            img_name = media_info['data'][0]['id'] + '.png'
            img_url = media_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print 'Image of %s is downloaded' % username
        else:
            print 'Post does\'nt exist'
    else:
        print 'Other than 200'


#Function declaration to get the ID of the recent post of a user by username
def get_post_id(username):
    user_id = get_user_id(username)
    if user_id is None:
        print 'User does not exist!'
        exit()
    request_url = base_url + 'users/%s/media/recent/?access_token=%s' % (user_id, token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


# Function declaration to like the recent post of a user
def like_a_post(username):
    media_id = get_post_id(username)
    request_url = base_url + 'users/media/%s/likes' % media_id
    payload = {"access_token": token}
    print 'POST request url : %s' % request_url
    like = requests.post(request_url, payload).json()
    if like['meta']['code'] == 200:
        print 'your like was successful'
    else:
        print 'Your like was unsuccessful please try again'


# Function declaration to comment the recent post of a user
def comment_a_post(username):
    media_id = get_post_id(username)
    request_url = base_url + 'users/media/%s/comments' % media_id
    payload = {"access_token": token, "text": "😃" }
    print 'POST request url : %s' % request_url
    like = requests.post(request_url, payload).json()
    if like['meta']['code'] == 200:
        print 'your comment was successful'
    else:
        print 'Your comment was unsuccessful please try again'


# Function declaration to make delete negative comments from the recent post
def delete_negative_comment(username):
    media_id = get_post_id(username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            
# Function to initiate instaBot
def init_bot():
    while True:
        print '\nWelcome to instaBot'
        print '\nMENU OPTIONS:'
        print 'a.Get your own details of insta account'
        print 'b.Get a friend\'s details of insta account'
        print 'c.Get your own recent post'
        print 'd.Get the recent post of a user by username'
        print 'j.Exit'

        choice = raw_input("\nSelect any option:")
        if choice == 'a':
            self_info()
        elif choice == 'b':
            get_user_info()
        elif choice == 'c':
            get_own_post()
        elif choice == 'd':
            username = raw_input("Enter the username of person you want to download post")
            get_user_post(username)
        elif choice == 'j':
            exit(1)
        else:
            print 'Wrong! Choice'

init_bot()