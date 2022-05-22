'''To randomly followed twitter users with specific 
    interests using python Tweepy and Twitter API '''

import tweepy
import config
import json
import random
import time

# config.py has been created beforehand to store twitter API keys and tokens 

# part 1: to retrieve (volume) number of followers 
# from a username specified,
# save them into a json file

def get_to_follow_list(target_username, volume, filename):
    # only bearer_token is needed for getting tewwets and users info
    client = tweepy.Client(bearer_token=config.Bearer_token)

    # choose a username in the niche who has many followers
    user = client.get_user(username=target_username)
    user_id = user.data.id

    # If there are thousands of followers, use tweepy.Paginator to
    # set a bigger limit.
    followers = tweepy.Paginator(client.get_users_followers, id=user_id).flatten(limit=volume)
    followers = client.get_users_followers(user_id)

    # retrieve user data from the response
    list = [f for f in followers.data]
    # print(list) # output is a list of User objects
    '''[<User id=1326917137693364230 name=Susan Koo username=SusanKoo3>, 
    <User id=1388873538455670791 name=PoeticMetric username=PoeticMetricHQ>,...] ''' 

    # to reconstruct list into a list of dictionarie    
    # 
    users_dict = [ {"id":item.id, 'name':item.name, 'username':item.username} for item in list]
    # print(users_dict[:2])
    # output:
    # [{'id': 1326917137693364230, 'name': 'Susan Koo', 'username': 'SusanKoo3'}, 
    # {'id': 1388873538455670791, # 'name': 'PoeticMetric', 'username': 'PoeticMetricHQ'}]

    # save the new list as json file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(users_dict, file, indent=4)

    return users_dict

# create the first json file
username='remote_dev_jobs'
volume = 200
filename = 'to_follow_twitter.json'

dict = get_to_follow_list(username, volume, filename)

# PART 2: get your own 'following' users' ids
# Use the same method above, 
# except =>
# 1. change usename to yourself
# 2. only scrape id numbers and save them -> item.id
# 3. the volume is your account 'following' number
# 4. save ids to 'my_following_ids.json' file
# This part only needs to be done once


# PART 3: randomly pick some ids to follow using tweepy

def random_follow_twitter_account(database_filename, volume):
    # Access Token must be provided for OAuth 1.0a User Context
    # create a new client with 4 credentials for auth
    client= tweepy.Client(
        consumer_key=config.API_key,
        consumer_secret=config.API_key_secret,
        access_token=config.Access_token,
        access_token_secret=config.Access_token_secret
    )   

    # open file to get users' dictionary list
    with open(database_filename, 'r', encoding='utf-8') as file:
        users = json.load(file)

    # randomly choose (volume) ids
    # check if they are already being followed
    # only follow those not being followed yet

    # get all ids I am following
    with open('my_following_ids.json', 'r+', encoding='utf-8') as filehandle:
        ids = json.load(filehandle)

        for _ in range(volume):   

            #get random user: 
            user = random.choice(users)
            id = user['id'] 

            # check if already 'following' ids
            if not id in ids:
                # do the following
                client.follow_user(id)
                # update ids
                ids.append(id)
                time.sleep(3)
                print(f'Just followed {user["username"]}')
            else:
                print(f'{user["username"]} has been followed already.')

        # change the current file position to 0
        filehandle.seek(0)
        json.dump(ids, filehandle, indent=4)
    
random_follow_twitter_account('to_follow_twitter.json', 2)

    


