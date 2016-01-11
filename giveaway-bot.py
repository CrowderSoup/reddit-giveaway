"""
Reddit Giveaway Bot

Simple script that will monitor comments on a given submission, entering any
that match a pattern into a giveaway.
"""

import praw
from config import *

r = praw.Reddit(user_agent='Reddit Raspberry Pi Giveaway (by /u/IrishLadd)')
submission = r.get_submission(submission_id=SUBMISSION)

# Let's make sure we get ALL comments in the thread:
submission.replace_more_comments(limit=None, threshold=0)

for comment in submission.comments:
    #print(dir(comment))
    if(MATCH_TEXT in comment.body and comment.is_root):
        print("Matching Entry by /u/{0}!".format(comment.author))
        with open("entries.csv", "a") as entries:
            entries.write('"{0}", "{1}"'.format(comment.author, comment.permalink))
    else:
        print("Not a matching entry by /u/{0} :(".format(comment.author))
