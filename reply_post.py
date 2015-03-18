#!/usr/bin/python
import praw
import pdb
import re
import os
import time
import random
from config_bot import *
from comments import *

# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    exit(1)

WAIT = 10
USERNAME = REDDIT_USERNAME
PASS = REDDIT_PASS
user_agent = USER_AGENT

# Create the Reddit instance
r = praw.Reddit(user_agent=user_agent)
# and login
r.login(USERNAME, PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    already_done = []
# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        already_done = filter(None, posts_replied_to)
try:
    # Get the top 5 values from our subreddit
    subreddit = r.get_subreddit('testing5000')
    for comment in subreddit.get_comments():
        if comment.author.name != REDDIT_USERNAME:     
            if comment.id not in already_done:
                print 'Comment not done'  
                if comment.body.lower() == "i need a lawyer":
                    # Reply to the post
                    print 'Its a match!'
                    if len(quotes) > 0:
                        temp = random.randint(0, len([quotes]))
                        comment.reply(quotes[temp])
                    else:
                         comment.reply('Better Call Saul!')                   
                    already_done.append(comment.id)
                    print "Bot replying to : ", comment.id, " "
                else:
                    print 'Match failed'
        else: 
            print 'Cannot reply to self'
        print('Wait between each comment in %d seconds \n' % WAIT)
        time.sleep(WAIT)
except praw.errors.RateLimitExceeded as error:
    if error.sleep_time < 200:
        print '\tSleeping for %d seconds as runtime error ' % error.sleep_time
        time.sleep(error.sleep_time)
    else:
        print 'This is gunna be a long wait, %d seconds to be precise, ', error.sleep_time 
        userInput = input("You sure you want to wait? Y/N:")
        if userInput.lower() == 'y':
            time.sleep(error.sleep_time)
        elif userInput.lower() == 'n':
            exit(1)


# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in already_done:
        f.write(post_id + "\n")