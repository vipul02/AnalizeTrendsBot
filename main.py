# requests library send request to api to get the access to particular data
import requests
# for retrieving the image
import urllib
# for retrieving the video
import urllib2
# This is NLP-Natural Language Processing, included to check if there is negative comments on post
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# this plots graph
from matplotlib import pyplot

# storing access token to app in a variable, token have the following scopes: basic, public_content, likes, comments.
token = '3516265067.a606bd5.6ac0cfccc602439c9551e758fbc87212'
# sandbox admin:im_vipul
# sandbox users:priyanka_verma96(use this) and royalmohit(this is private acc. so not much access)

# this is the base url to access data from insta
base_url = 'https://api.instagram.com/v1/'


# function to give status code info
# this prints status code, error type, error message
def status_code_info(info):
        print "Status Code:%s" % info['meta']['code']
        print "Error Type:%s" % info['meta']['error_type']
        print "Error Message:%s" % info['meta']['error_message']
        print 'Error in meta code, search on https://httpstatuses.com/ for furthermore details'


# Function declaration to get your own info
def self_info():
    # stores the url to request and get info using access token
    request_url = base_url + 'users/self/?access_token=%s' % token
    # printing the request url
    print 'GET request url is %s' % request_url
    # storing the info fetched by the request url
    user_info = requests.get(request_url).json()
    # checking if the status code is 200 or success or accepted ok
    if user_info['meta']['code'] == 200:
        # checking if there is data present
        if len(user_info['data']):
            print 'Username:%s' % user_info['data']['username']
            print 'No. of followers:%s' % user_info['data']['counts']['followed_by']
            print 'No. of followings:%s' % user_info['data']['counts']['follows']
            print 'No. of posts:%s' % user_info['data']['counts']['media']
        else:
            print 'You don\'t exist or not have signup on instagram or you don\'t have any data'
            print 'Link for signup : https://www.instagram.com'
    else:
        # calling function to get more info on status code
        status_code_info(user_info['meta']['code'])


# Function declaration to get the ID of a user by username
def get_user_id(username):
    # request url to search the username
    request_url = base_url + 'users/search/?q=%s&access_token=%s' % (username, token)
    print 'GET request url is %s' % request_url
    # storing the info fetched by the request url
    user_info = requests.get(request_url).json()
    # checking if the status code is 200 or success or accepted ok
    if user_info['meta']['code'] == 200:
        # checking if there is nay data present
        if len(user_info['data']):
            # returning the id of the zeroth element of data
            return user_info['data'][0]['id']
        else:
            print 'User does not exist or you not have access to that person'
    else:
        # calling function to get more info on status code
        status_code_info(user_info)


# Function declaration to get the info of a user by username
def get_user_info(username):
    # calling function to get user id
    user_id = get_user_id(username)
    # request url to get info of other user
    request_url = base_url + 'users/%s/?access_token=%s' % (user_id, token)
    print 'GET request url is %s' % request_url
    user_info = requests.get(request_url).json()
    # checking if the status code is 200 or success or accepted ok
    if user_info['meta']['code'] == 200:
        # checking if there is data present
        if len(user_info['data']):
            print 'Username:%s' % user_info['data']['username']
            print 'No. of followers:%s' % user_info['data']['counts']['followed_by']
            print 'No. of followings:%s' % user_info['data']['counts']['follows']
            print 'No. of posts:%s' % user_info['data']['counts']['media']
        else:
            print 'There is no data for user'
    else:
        status_code_info(user_info)


# function to download post by media info
def down_func(media_info):
    # list to take the indexes which are to be downloaded
    index = []
    # variable to calculate the no. of downloads
    count = 0
    # checking if there is success code from server
    if media_info['meta']['code'] == 200:
        # checking if there is data present
        if len(media_info['data']):
            # getting the response from user whether user want to download the most recent or the other post
            response = raw_input('Do u want to download the most recent post(r for this)'
                                 ' or want to download post with something specific(s for this):')
            # checking if user has entered r, upper() converts the char to uppercase
            if response.upper() == 'R':
                # this appends the 0 in the index list
                index.append(0)
                # this increases the count by one stating that there is one downloading post
                count += 1
            elif response.upper() == 'S':
                print 'What specifics do you want:'
                print '1.Download the post with minimum no. of likes'
                print '2.Download the post with maximum no. of likes'
                print '3.Download the post with a particular hash tag'
                # getting the option from user, input takes input in integer form
                specific = input("Select any option:")
                if specific == 1:
                    # list of no. of likes on recent media
                    likes = []
                    # loop runs the time the length of media_info['data'] list
                    for x in range(len(media_info['data'])):
                        # appends the count to the likes list
                        likes.append(media_info['data'][x]['likes']['count'])
                    # min() calculates the min value in the list
                    min_likes = min(likes)
                    for x in range(len(media_info['data'])):
                        # checks to how many and which post has minimum likes
                        if min_likes == media_info['data'][x]['likes']['count']:
                            # this appends the index no. of post having minimum likes to index
                            index.append(x)
                            # increase count by stating that there is one more post to download
                            count += 1
                elif specific == 2:
                    # list of no. of likes on recent media
                    likes = []
                    # loop runs the time the length of media_info['data'] list
                    for x in range(len(media_info['data'])):
                        # appends the count to the likes list
                        likes.append(media_info['data'][x]['likes']['count'])
                    # max() calculates the min value in the list
                    max_likes = max(likes)
                    for x in range(len(media_info['data'])):
                        # checks to how many and which post has maximum likes
                        if max_likes == media_info['data'][x]['likes']['count']:
                            # this appends the index no. of post having maximum likes to index
                            index.append(x)
                            # increase count by stating that there is one more post to download
                            count += 1
                elif specific == 3:
                    hash_tag = raw_input("Enter the hash tag:")
                    # loop runs the time the length of media_info['data'] list
                    for x in range(len(media_info['data'])):
                        # loop runs the time the length of media_info['data'][x]['tags'] list
                        for y in range(len(media_info['data'][x]['tags'])):
                            # checks if the post has the hash tag given by user
                            if hash_tag == media_info['data'][x]['tags'][y]:
                                # this appends the index no. of post having maximum likes to index
                                index.append(x)
                                # increase count by stating that there is one more post to download
                                count += 1
                else:
                    print 'Wrong choice'
            # runs loop in index list over each element x of index list
            for x in index:
                # storing id of image in img_name variable with extension .png, image will be downloaded by this name
                img_name = media_info['data'][x]['id'] + '.png'
                # storing image url in img_url variable
                img_url = media_info['data'][x]['images']['standard_resolution']['url']
                # this downloads the image
                urllib.urlretrieve(img_url, img_name)
                print 'Image downloaded'
                # checks if the data type of post is video
                if media_info['data'][x]['type'] == 'video':
                    # asks the user if they want to download the post
                    q_video = raw_input('Type of media is video,do u want to download the video(y/n):')
                    if q_video.upper() == 'Y':
                        # storing video name as id with extension .mp4
                        video_name = media_info['data'][x]['id'] + '.mp4'
                        video_url = media_info['data'][x]['videos']['standard_resolution']['url']
                        # this downloads the video
                        with open(video_name, 'wb') as f:
                            f.write(urllib2.urlopen(video_url).read())
                        print 'Video downloaded'
                        # increase count by stating that there is one more post to download
                        count += 1
                    else:
                        pass
                else:
                    pass
            if count > 0:
                print 'Number of post downloaded:%d' % count
            else:
                print 'No post downloaded, some kind of error'
        else:
            print 'Post does\'nt exist'
    else:
        # gets info about status code
        status_code_info(media_info)


# Function declaration to download your post
def down_own_post():
    request_url = base_url + 'users/self/media/recent/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    media_info = requests.get(request_url).json()
    down_func(media_info)


# function to get media info of user by username
def get_media_info_user(username):
    user_id = get_user_id(username)
    request_url = base_url + 'users/%s/media/recent/?access_token=%s' % (user_id, token)
    print 'GET request url : %s' % request_url
    media_info = requests.get(request_url).json()
    return media_info


# Function declaration to download the post of a user by username
def down_user_post(username):
    # gets info of other user by passing username to it
    media_info = get_media_info_user(username)
    down_func(media_info)


# Function declaration to get the ID of the recent post of a user by username
def get_post_id(username):
    # to get the list of all media ids
    media_id = []
    # gets info of other user by passing username to it
    media_info = get_media_info_user(username)
    # checking if the status code is 200 or success or accepted ok
    if media_info['meta']['code'] == 200:
        # checking if there is data present
        if len(media_info['data']):
            for x in range(len(media_info['data'])):
                # it appends each and every id of media of user to media_id list
                media_id.append(media_info['data'][x]['id'])
            # returns media id list
            return media_id
        else:
            print 'There is no recent post of the user!'
    else:
        status_code_info(media_info)


# function to get the list of likes on a "particular post or media" of the username you entered
# either u can enter name of access token owner or sandbox user
# only the likes sandbox users and access token owner will be shown
def get_like_list(username):
    # counts the no. of comments fetched
    count = 0
    # stores the list of media ids
    media_id = get_post_id(username)
    for x in range(len(media_id)):
        request_url = base_url + 'media/%s/likes?access_token=%s' % (media_id[x], token)
        print 'GET request url : %s' % request_url
        like_info = requests.get(request_url).json()
        if len(like_info['data']):
            print 'ID of post liked:%s' % media_id[x]
            for y in range(len(like_info['data'])):
                print 'Liked by:%s' % like_info['data'][y]['username']
                count += 1
        else:
            print 'No data found'
    if count > 0:
        print 'Successfully fetching the list of likes'
    else:
        print 'There is no like on the post'


# Function declaration to like the post of a username provided
def like_a_post(username):
    # stores the ids list of media
    media_id = get_post_id(username)
    for x in range(len(media_id)):
        # prints the media id from latest to old(max 20 will be print in sandbox mode)
        print '%d.Media id:%s' % (x+1, media_id[x])
    # this gets the index of id which is to be downloaded
    index = input("Select any one to like(one on the top is most recent):")
    # id to which like is to be made
    # here index-1 is hoax, when user enter 0 index turns to -1 which means first from last
    # so to take care of this logical error
    if index != 0:
        get_id = media_id[index-1]
        request_url = base_url + 'media/%s/likes' % get_id
        # payload is body of request url in POST type
        payload = {"access_token": token}
        print 'POST request url : %s' % request_url
        # this is post type request url which has body rather the\an get which has all info in url itself
        like = requests.post(request_url, payload).json()
        # checking if the status code is 200 or success or accepted ok
        if like['meta']['code'] == 200:
            print 'Your like was successful'
        else:
            print 'Your like was unsuccessful please try again'
    else:
        print 'Wrong choice'


# a function declaration to get the recent media liked by the user and all the sandbox users.
def recent_media_liked():
    request_url = base_url + 'users/self/media/liked/?access_token=%s' % token
    print 'GET request url is %s' % request_url
    # fetching the ifo using GET url
    media_info = requests.get(request_url).json()
    # checking if the status code is 200 or success or accepted ok
    if media_info['meta']['code'] == 200:
        # checking if there is data present
        if len(media_info['data']):
            for x in range(len(media_info['data'])):
                print 'ID of post liked: %s' % media_info['data'][x]['id']
                print '%s has liked the post' % media_info['data'][x]['user']['username']
        else:
            print 'You have not liked any post, you are just too picky!!'
    else:
        status_code_info(media_info)


# function to get list of comments made on post
# if you use app in sandbox mode then only sandbox users and ADMIN comments will be listed
def get_comment_list(username):
    # counts the no. of comments fetched
    count = 0
    # stores the media ids list
    media_id = get_post_id(username)
    for x in range(len(media_id)):
        request_url = base_url + 'media/%s/comments?access_token=%s' % (media_id[x], token)
        print 'GET request url : %s' % request_url
        comment_info = requests.get(request_url).json()
        if len(comment_info['data']):
            print 'ID of post:%s' % media_id[x]
            for y in range(len(comment_info['data'])):
                print '%d.Username:%s' % (y+1, comment_info['data'][y]['from']['username'])
                print '  Comment:%s' % comment_info['data'][y]['text']
                count += 1
        else:
            print 'No data found'
    if count > 0:
        print 'Successfully fetching the list of comments'
        print 'Number of comments fetched:%d' % count
    else:
        print 'There is no comment on the post'


# Function declaration to comment the recent post of a user
def comment_a_post(username):
    media_id = get_post_id(username)
    for x in range(len(media_id)):
        # list all the media ids
        print '%d.Media id:%s' % (x+1, media_id[x])
    # this gets the index of id which is to be downloaded
    index = input("Select any one to like(one on the top is most recent)")
    # this stores the id of media to make comment on
    get_id = media_id[index-1]
    request_url = base_url + 'media/%s/comments' % get_id
    comment = raw_input("Enter the comment you want to make on post:")
    # this the body of POST url
    payload = {"access_token": token, "text": comment}
    print 'POST request url : %s' % request_url
    comment = requests.post(request_url, payload).json()
    # checking if the status code is 200 or success or accepted ok
    if comment['meta']['code'] == 200:
        print 'Your comment was successful'
    else:
        print 'Your comment was unsuccessful please try again'


# Function declaration to make delete negative comments from all the recent posts(max 20 in sandbox mode)
def delete_negative_comment(username):
    # to count the no. of comments delete
    count = 0
    # get the list of media ids
    media_id = get_post_id(username)
    for x in range(len(media_id)):
        request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id[x], token)
        print 'GET request url : %s' % request_url
        # storing the comment info
        comment_info = requests.get(request_url).json()
        # checking if the status code is 200 or success or accepted ok
        if comment_info['meta']['code'] == 200:
            # checking if there is data present
            if len(comment_info['data']):
                # another loop runs over the comment_info['data'] list
                for y in range(len(comment_info['data'])):
                    # storing the id of comment
                    comment_id = comment_info['data'][y]['id']
                    # storing the comment
                    comment_text = comment_info['data'][y]['text']
                    # checking comment with NaiveBayesAnalyzer() that if the comment is negative
                    check_comment = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer()).sentiment
                    # if percentage of neg is greater than pos than delete
                    if check_comment.p_neg > check_comment.p_pos :
                        print "Negative comment : %s" % comment_text
                        delete_url = base_url + \
                            'media/%s/comments/%s?access_token=%s' % (media_id[x], comment_id, token)
                        # delete url request to delete comment
                        print 'DELETE request url: %s' % delete_url
                        delete_info = requests.delete(delete_url).json()
                        if delete_info['meta']['code'] == 200:
                            count += 1
                        else:
                            pass
                    else:
                        print 'Positive comment: %s' % comment_text
            else:
                print 'There is no comment in your post'
        else:
            print 'Status code other than 200'
    if count > 0:
        print 'Post was deleted successfully'
        print 'Number of post deleted:%d' % count
    else:
        print 'No negative comments so no post deketed'


# function to plot the graph of Trending Hash Tags
def plot_graph():
    x = []
    counts_of_hash_tag = []
    hash_tags = []
    num_hashtags = 0
    choice = raw_input('Do u want to enter your own hashtags or want predefined(y for your own/n for predefined):')
    # checks the choice by converting it to uppercase
    if choice.upper() == 'Y':
        num_hashtags = int(raw_input('Enter the no. of popular hashtags do you want to enter:'))
        print 'Enter %d hash tags:' % num_hashtags
        for i in range(num_hashtags):
            hash_tags.append(raw_input())
            x.append(i + 1)
    elif choice.upper() == 'N':
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        hash_tags = ['india', 'cool', 'paris', 'rain', 'snow', 'beauty', 'morning',
                     'anime', 'insta', 'cute']
        num_hashtags = 10
    else:
        print "Wrong choice"
        init_bot()
    # """LOVE""" is the most frequent hash tag around the globe
    for j in range(num_hashtags):
        request_url = base_url + 'tags/%s/?access_token=%s' % (hash_tags[j], token)
        print 'GET request url : %s' % request_url
        tag_info = requests.get(request_url).json()
        # checking if there is data present
        if len(tag_info['data']):
            counts_of_hash_tag.append(tag_info['data']['media_count'])
        else:
            print "#%s tag not found" % hash_tags[j]
            init_bot()
    pyplot.bar(x, counts_of_hash_tag, tick_label=hash_tags,
               color=['red', 'blue', 'orange', 'yellow', 'green'], width=0.8)
    pyplot.xlabel('<-----Names of hash tags----->')
    pyplot.ylabel('<-----No. of counts/occurrence of hash tags----->')
    pyplot.title('Frequency graph of occurrence of hash tags')
    pyplot.show()


print '\nWelcome to instaBot'


# Function to initiate instaBot
def init_bot():
    # to run the program infinite times till the user ends it
    while True:
        print '\nMENU OPTIONS:'
        print '1.Get your own details of insta account'
        print '2.Get a friend\'s details of insta account'
        print '3.Download your own post'
        print '4.Download the post of a user by username'
        print '5.Get a list of people who have liked the post of a user'
        print '6.Like the post of a user'
        print '7.Get the list of recent media liked by user or sandbox user'
        print '8.Get a list of comments on recent post of a user'
        print '9.Make a comment on the post of a user'
        print '10.Delete negative comments from all the post of a user'
        print '11.Plot the Bar graph of Trending Hash Tags'
        print '0.Exit'

        # we can't referenced object without declaration, it was referenced in except
        choice = None
        try:
            # taking input from user as string and converting it to integer
            choice = int(raw_input("\nSelect any option:"))
            # if elif else statement to run different functions based on user's choice
            if choice == 1:
                self_info()
            elif choice == 2:
                # taking the username from user in form of string
                username = raw_input("Enter the username of person:")
                get_user_info(username)
            elif choice == 3:
                down_own_post()
            elif choice == 4:
                username = raw_input("Enter the username of person:")
                down_user_post(username)
            # 5th and 7th choice are different, in 5th its give the list of username who have like that certain post
            # but in 7th it gives the list of post which user has liked
            elif choice == 5:
                username = raw_input("Enter the username of person:")
                get_like_list(username)
            elif choice == 6:
                username = raw_input("Enter the username of person:")
                like_a_post(username)
            elif choice == 7:
                recent_media_liked()
            elif choice == 8:
                username = raw_input("Enter the username of person:")
                get_comment_list(username)
            elif choice == 9:
                username = raw_input("Enter the username of person:")
                comment_a_post(username)
            elif choice == 10:
                username = raw_input("Enter the username of person:")
                delete_negative_comment(username)
            elif choice == 11:
                plot_graph()
            elif choice == 0:
                # if exit() is called inside try it forms infinite loop, and program never shuts
                # so here if user wants to exits raise statement is called and control shifts to except statement
                raise
            else:
                print 'Wrong! Choice'
        except:
            # now if user selects 0 then exit() is called, exit() works fine under except statement
            if choice == 0:
                exit(10)
            # if 0 is not entered then below will be printed
            print 'Error! Either u entered wrong data or invalid data type'


init_bot()
