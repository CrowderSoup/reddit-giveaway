"""
Reddit Giveaway Bot

Simple script that will monitor comments on a given submission, entering any
that match a pattern into a giveaway.
"""

import praw
from config import *


def has_matching_line(csv_file_name, name):
    matching_line = False

    with open(csv_file_name, 'r') as csv_file:
        matching_line = csv_file.read().find(comment.author.name)

    return matching_line != -1

def write_line(csv_file, name, permalink):
    """
    Write a line to a given csv
    """
    csv_file.write('"{0}", "{1}"\n'.format(name, permalink))

r = praw.Reddit(user_agent='Reddit Raspberry Pi Giveaway (by /u/IrishLadd)')
submission = r.get_submission(submission_id=SUBMISSION)

# Let's make sure we get ALL comments in the thread:
submission.replace_more_comments(limit=None, threshold=0)

for comment in submission.comments:
    #print(dir(comment))
    if(MATCH_TEXT.lower() in comment.body.lower() and comment.is_root):
        matching = has_matching_line('entries.csv', comment.author.name)
        if(not matching):
            print("Matching Entry by /u/{0}!".format(comment.author))
            with open("entries.csv", "a") as entries:
                write_line(entries, comment.author.name, comment.permalink)
    else:
        matching = has_matching_line('not_matching.csv', comment.author.name)
        if(not matching):
            print("Not a matching entry by /u/{0} :(".format(comment.author))
            with open("not_matching.csv", 'a') as not_matching:
                write_line(not_matching, comment.author.name, comment.permalink)
