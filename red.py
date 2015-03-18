import praw
user_agent = ("PyTest Bot 0.1")
r = praw.Reddit("learnpython")
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("learnpython")

for submission in subreddit.get_hot(limit = 5):
	print "title: ", submission.title
	print "Text: ", submission.selftext
	print "Score:", submission.score
	print "=====================\n"

	
