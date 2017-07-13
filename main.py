import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# storing access token to app in a variable
token = '3516265067.a606bd5.6ac0cfccc602439c9551e758fbc87212'
# sandbox admin:im_vipul
# sandbox users:priyanka_verma96 and royalmohit

# this is the base url to access data from insta
base_url = 'https://api.instagram.com/v1/'


# function to give status code info
def status_code_info(info):
        print "Status Code:%s" % info['meta']['code']
        print "Error Type:%s" % info['meta']['error_type']
        print "Error Message:%s" % info['meta']['error_message']
        print 'Error in meta code, search on https://httpstatuses.com/ for furthermore details'


# Function declaration to get your own info
def self_info():
    request_url = base_url + 'users/self/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % user_info['data']['username']
            print 'No. of Followers:%s' % user_info['data']['counts']['followed_by']
            print 'No. of people you follow:%s' % user_info['data']['counts']['follows']
            print 'No. of posts:%s' % user_info['data']['counts']['media']
        else:
            print 'You don\'t exist or not have signup on instagram or you don\'t have any data'
            print 'Link for signup : https://www.instagram.com'
    else:
        status_code_info(user_info['meta']['code'])


# Function declaration to get the ID of a user by username
def get_user_id(username):
    request_url = base_url + 'users/search/?q=%s&access_token=%s' % (username, token)
    print 'GET request url is %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            print 'User does not exist'
    else:
        status_code_info(user_info)


# Function declaration to get the info of a user by username
def get_user_info(username):
    user_id = get_user_id(username)

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
        status_code_info(user_info)


# Function declaration to get your recent post
def get_own_post():
    request_url = base_url + 'users/self/media/recent/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            img_name = media_info['data'][0]['id'] + '.png'
            img_url = media_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print 'Your image is downloaded'
        else:
            print 'Post does\'nt exist'
    else:
        status_code_info(media_info)


# function to get media info of user by username
def get_media_info_user(username):
    user_id = get_user_id(username)
    request_url = base_url + 'users/%s/media/recent/?access_token=%s' % (user_id, token)
    print 'GET request url : %s' % request_url
    media_info = requests.get(request_url).json()
    return media_info


# Function declaration to get the ID of the recent post of a user by username
def get_post_id(username):
    media_info = get_media_info_user(username)

    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            return media_info['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
    else:
        status_code_info(media_info)


# Function declaration to download the recent post of a user by username
def get_user_post(username):
    media_info = get_media_info_user(username)
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            img_name = media_info['data'][0]['id'] + '.png'
            img_url = media_info['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print 'Image of %s is downloaded' % username
        else:
            print 'Post does\'nt exist'
    else:
        status_code_info(media_info)


# a function declaration to get the recent media liked by the user.
def recent_media_liked():
    request_url = base_url + 'users/self/media/liked/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            for x in range(len(media_info['data'])):
                print 'ID of post liked: %s' % media_info['data'][x]['id']
                print '%s has liked your post' % media_info['data'][x]['user']['username']
        else:
            print 'You have not liked any post, you are just too picky!!'
    else:
        status_code_info(media_info)


# function to get the list of likes on a "particular post" of the username you entered
# either u can enter name of access token owner or sandbox user
# only the likes sandbox users and access token owner will be shown
def get_like_list(username):
    media_id = get_post_id(username)
    request_url = base_url + 'media/%s/likes?access_token=%s' % (media_id, token)
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()
    for x in range(user_media['data']):
        print '%d.Username:%s' % (x, user_media['data'][x]['username']),
        print '  Full name:%s' % user_media['data'][x]['full_name']


# Function declaration to like the recent post of a username provided
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
    comment = raw_input("Enter the comment you want to make on post:")
    payload = {"access_token": token, "text": comment}
    print 'POST request url : %s' % request_url
    like = requests.post(request_url, payload).json()
    if like['meta']['code'] == 200:
        print 'your comment was successful'
    else:
        print 'Your comment was unsuccessful please try again'


# function to get list of comments made on post
# if you use app in sandbox mode then only sandbox users and ADMIN comments will be listed
def get_comment_list(username):
    media_id = get_post_id(username)
    request_url = base_url + 'media/%s/comments?access_token=%s' % (media_id, token)
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()
    if user_media['data']:
        for x in range(user_media['data']):
            print '%d.Username:%s' % (x, user_media['data'][x]['from']['username']),
            print '  Comment:%s' % user_media['data'][x]['text']
        print 'Successfully fetching the list of comments'
    else:
        print 'There is no comment on the post'


# Function declaration to make delete negative comments from the recent post
def delete_negative_comment(username):
    media_id = get_post_id(username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, token)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                check_comment = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer()).sentiment
                if check_comment.p_neg > check_comment.p_pos :
                    print "Negative comment : %s" % comment_text
                    delete_url = base_url + '/media/%s/comments/%s?access_token=%s' % (media_id, comment_id, token)
                    print 'DELETE request url: %s' % delete_url
                    delete_info = requests.delete(request_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Post was deleted successfully'
                    else:
                        print 'Post was not deleted, status code other than 200'
                else:
                    print 'Positive comment: %s' % comment_text
        else:
            print 'There is no comment in your post'
    else:
        print 'Status code other than 200'


def likes_info(media_info):
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            # list of no. of likes on recent media
            likes = []
            for x in range(len(media_info['data'])):
                likes.append(media_info['data'][x]['likes']['count'])
            return likes
        else:
            print 'Post does\'nt exist'
    else:
        status_code_info(media_info)


# function to download post with minimum no. of likes
def down_min(likes, media_info):
    # variable to calculate the no. of downloads
    count = 0
    # min() calculates the min value in the list
    min_likes = min(likes)
    for x in range(len(media_info['data'])):
        if min_likes == media_info['data'][x]['likes']['count']:
            img_name = media_info['data'][x]['id'] + '.png'
            img_url = media_info['data'][x]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            count += 1
    if count > 0:
        print '%d post download' % count
    else:
        print 'No post downloaded, some kind of error'


# function to download post with minimum no. of likes
def down_max(likes, media_info):
    # variable to calculate the no. of downloads
    count = 0
    # max() calculates the max value in the list
    max_likes = max(likes)
    for x in range(len(media_info['data'])):
        if max_likes == media_info['data'][x]['likes']['count']:
            img_name = media_info['data'][x]['id'] + '.png'
            img_url = media_info['data'][x]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            count += 1
    if count > 0:
        print '%d post download' % count
    else:
        print 'No post downloaded, some kind of error'


# function to download post with something special
def download_post():
    print 'Select:'
    print '1.Download your own post'
    print '2.Download post of another user(must be sandbox user)'
    select = int(raw_input("Enter choice:"))
    if select == 1:
        request_url = base_url + 'users/self/media/recent/?access_token=%s' % token
        media_info = requests.get(request_url).json()
        likes = likes_info(media_info)
        print 'What specifics do you want:'
        print '1.Download the post with minimum no. of likes'
        print '2.Download the post with maximum no. of likes'
        print '3.Go to previous menu'
        option = int(raw_input("Enter option:"))
        if option == 1:
            down_min(likes, media_info)
        elif option == 2:
            down_max(likes, media_info)
        elif option == 3:
            download_post()
        else:
            print 'Invalid choice'
    elif select == 2:
        username = raw_input("Enter the username of person")
        media_info = get_media_info_user(username)
        likes = likes_info(media_info)
        print 'What specifics do you want:'
        print '1.Download the post with minimum no. of likes'
        print '2.Download the post with maximum no. of likes'
        print '3.Go to previous menu'
        option = int(raw_input("Enter option:"))
        if option == 1:
            down_min(likes, media_info)
        elif option == 2:
            down_max(likes, media_info)
        elif option == 3:
            download_post()
        else:
            print 'Invalid choice'


print '\nWelcome to instaBot'


# Function to initiate instaBot
def init_bot():
    while True:
        print '\nMENU OPTIONS:'
        print '1.Get your own details of insta account'
        print '2.Get a friend\'s details of insta account'
        print '3.Get your own recent post'
        print '4.Download the recent post of a user by username'
        print '5.Get a list of people who have liked the recent post of a user'
        print '6.Like the recent post of a user'
        print '7.Get the list of media liked by user'
        print '8.Get a list of comments on the recent post of a user'
        print '9.Make a comment on the recent post of a user'
        print '10.Delete negative comments from the recent post of a user'
        print '11.Download post with something special'
        print '0.Exit'

        choice = raw_input("\nSelect any option:")
        if choice == 1:
            self_info()
        elif choice == 2:
            username = raw_input("Enter the username of person")
            get_user_info(username)
        elif choice == 3:
            get_own_post()
        elif choice == 4:
            username = raw_input("Enter the username of person you want to download post")
            get_user_post(username)
        elif choice == 5:
            username = raw_input("Enter the username of person")
            get_like_list(username)
        elif choice == 6:
            username = raw_input("Enter the username of person")
            like_a_post(username)
        elif choice == 7:
            recent_media_liked()
        elif choice == 8:
            username = raw_input("Enter the username of person")
            get_comment_list(username)
        elif choice == 9:
            username = raw_input("Enter the username of person")
            comment_a_post(username)
        elif choice == 10:
            username = raw_input("Enter the username of person")
            delete_negative_comment(username)
        elif choice == 11:
            download_post()
        elif choice == 0:
            exit(1)
        else:
            print 'Wrong! Choice'

init_bot()