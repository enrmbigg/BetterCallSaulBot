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
#You may want to chnages these to match what you eg. username an password
Wait = WAIT
MAXCOMMENTS = MAXCOMMS
USERNAME = REDDIT_USERNAME
PASS = REDDIT_PASS
user_agent = USER_AGENT
TRIGGERS = PARENTSTRING
shouldLoop = LOOP

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

#Enter all comments into a log
while shouldLoop:
    try:
        with open("log.txt", "a") as f:
            print ('Bot Started  %s \n' % time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
            f.write("Bot Started at " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + "\n")
            print 'Loop is set to: ', shouldLoop
            f.write("Loop is set to: " + str(shouldLoop) + "\n")
            # Get the top 5 values from our subreddit
            subreddit = r.get_subreddit('testing5000')
            for comment in subreddit.get_comments(limit=MAXCOMMENTS):
                try:
                    print 'Checking Comment Body.......'
                    f.write("Checking Comment Body....... \n")
                    if any(key.lower() in comment.body.lower() for key in TRIGGERS):
                        print 'It\'s A Match!'
                        f.write("It\'s A Match! \n")
                        if comment.author.name != REDDIT_USERNAME:     
                            if comment.id not in already_done:
                                print 'Comment Not Replied Too, Replying.....' 
                                f.write("Comment Not Replied Too, Replying..... \n") 
                                if len(quotes) > 0:
                                    comment.reply(random.choice(quotes))
                                else:
                                     comment.reply('Better Call Saul!')                   
                                already_done.append(comment.id)
                                print "Bot Replied To : ", comment.id, ", ", comment.author.name
                                f.write("Bot Replied To : " + comment.id + ", " + comment.author.name + "\n") 
                            else:
                                print 'Comment Already Replied Too' 
                                f.write("Comment Already Replied Too \n") 
                        else: 
                            print 'Cannot Reply To Self, Comment Skipped'
                            f.write("Cannot Reply To Self, Comment Skipped \n") 
                    else:
                        print 'Match failed'
                        f.write("Match failed \n") 
                    print('Wait Between Each CommentCheck Is %d Seconds' % Wait)
                    print 'Waiting..........\n'
                    f.write("Wait Between Each CommentCheck Is %d Seconds \n" % Wait) 
                    f.write("Waiting.......... \n") 
                    time.sleep(Wait)
                except praw.errors.RateLimitExceeded as error:
                    if error.sleep_time < 200:
                        print '\tSleeping For %d Seconds As Runtime Error \n' % error.sleep_time
                        f.write("\tSleeping For %d Seconds As Runtime Error \n" % error.sleep_time) 
                        time.sleep(error.sleep_time)
                    else:
                        print 'Runtime Error, Rate Limit Exceeded'
                        print 'This Is Gunna Be A Long Wait, %d Seconds To Be Precise' % error.sleep_time 
                        print 'Sorry, Your Gunna Have To Wait, Tough Luck'
                        f.write("Runtime Error \n") 
                        f.write("This Is Gunna Be A Long Wait, %d Seconds To Be Precise \n" % error.sleep_time) 
                        f.write("Sorry, Your Gunna Have To Wait, Tough Luck \n") 
                        time.sleep(error.sleep_time)
            print 'Finshed All Comments Check'
            f.write('Finshed All Comments Check \n')
            # Write our updated list back to the file
            with open("posts_replied_to.txt", "w") as f:
                for post_id in already_done:
                    f.write(post_id + "\n")
            print 'Gathering More Comments'
    except Exception as e:
        print ('An error occured ', e)
        f.write("An error occured " + e + " \n")
    finally:
        with open("log.txt", "a") as f:
            print ('Bot Ended  %s \n' % time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
            f.write("Bot Ended at " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()) + "\n")
            f.write("\n")
