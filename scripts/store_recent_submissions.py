import praw
import datetime
import MySQLdb
import re

my_user_agent = 'Gafte'
my_client_id = 'IB4hdXbF1kcsWQ'
my_client_secret = '7uUB8oh9icfrneygPnJUMW1m6Xg'

# add subreddits to pull from here
subreddits = ['sweden']

# takes submission data and for all submissions,
# takes data on comments and users and stores
# all data in MySQL tables
def recent_submissions(subreddit_name):
    reddit = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret)

    recent_submissions = []
    recent_posts = []
    recent_users = []
    recent_comments = []
    subreddit_info = []
    moderators = []
    total_submissions = []

    start_time = 1481155200
    end_time = 1481158799

    subreddit_info = {
        'subredditName': subreddit_name,
        'subscribers': reddit.subreddit(subreddit_name).subscribers
    }

    # get moderators of subreddit
    for moderator in reddit.subreddit(subreddit_name).moderator.__iter__():
        moderator_data = {
            'subredditName': subreddit_name,
            'username': moderator.name
        }
        moderator_user_data = {
		'username': moderator.name,
		'karma': moderator.link_karma + moderator.comment_karma
        }
        moderators.append(moderator_data)
        recent_users.append(moderator_user_data)

    # Takes in submissions from each hour of 12/8/16 using unix epoch time boundaries
    for hour in range(0, 24):
        for submission in (reddit.subreddit(subreddit_name).submissions(start=start_time, end=end_time)):
            total_submissions.append(submission)
        start_time = end_time + 1
        end_time += 3600
        print(hour, total_submissions.__len__())

    for submission in total_submissions:
        ratio = reddit.submission(id=submission.id, url=None).upvote_ratio
        ups = round((ratio * submission.score) / (2 * ratio - 1)) if ratio != 0.5 else round(submission.score / 2)
        downs = ups - submission.score

        if submission.is_self:
            post_type = 'text'
            post_type_value = 1
            post_data = {
                'postid': submission.id,
                'contents': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", submission.selftext)
            }
        else:
            post_type = 'link'
            post_type_value = 0
            post_data = {
                'postid': submission.id,
                'contents': submission.url
            }

        user = reddit.redditor(submission.author.name)
        user_data = {
            'username': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", user.name),
            'karma': user.link_karma + user.comment_karma
        }

        submission_data = {
            'postid': submission.id,
            'username': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", submission.author.name),
            'title': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", submission.title),
            'subredditName': subreddit_name,
            'upvotes': ups,
            'downvotes': downs,
            'postType': post_type_value,
            'timeSubmitted': datetime.datetime.utcfromtimestamp(submission.created_utc)
        }
        print(submission_data)

        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            if hasattr(comment, 'author.name'):  # catch deleted comments
                comment_data = {
                    'cid': comment.id,
                    'p_cid': submission.id,
                    'postid': submission.id,
                    'text': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", comment.body),
                    'username': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", comment.author.name),
                    'score': comment.ups,
                    'commentType': 1,  # comment IS a top-level root comment
                    'timeSubmitted': datetime.datetime.utcfromtimestamp(comment.created_utc)
                }
                recent_comments.append(comment_data)
            for reply in comment.replies:
                recent_comments.extend(comment_parser(reply, comment.id, submission.id))

        recent_submissions.append(submission_data)
        recent_posts.append(post_data)
        recent_users.append(user_data)

    # Create connection
    connection = MySQLdb.connect("127.0.0.1", "root", "yahoo321", "RDB")
    cursor = connection.cursor()

    #stores user info
    for user in recent_users:
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_user (username, karma) VALUES (%s, %s)")
        # execute sql statement
        cursor.execute(sql, (user['username'],
                             user['karma']))

    #stores submission info
    for submission in recent_submissions:
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_submission VALUES (%s, %s, %s, %s, %s, %s, %s)")
        # execute sql statement
        cursor.execute(sql, (submission['postid'],
                             submission['username'],
                             submission['title'],
                             submission['upvotes'],
                             submission['downvotes'],
                             submission['postType'],
                            submission['timeSubmitted']))
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_submission_hasa_subreddit VALUES (%s, %s)")
        # execute sql statement
        cursor.execute(sql, (submission['postid'],
                             submission['subredditName']))

    #stores post info
    for post in recent_posts:
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_" + post_type + "post VALUES (%s, %s)")
        # execute sql statement
        cursor.execute(sql, (post['postid'],
                             post['contents']))

    # stores comment info and comment_hasa info
    for comment in recent_comments:
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_Comment VALUES (%s, %s, %s, %s, %s, %s, %s)")
        # execute sql statement
        cursor.execute(sql, (comment['cid'],
                             comment['p_cid'],
                             comment['postid'],
                             comment['text'],
                             comment['score'],
                             comment['commentType'],
                             comment['timeSubmitted']))
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_Comment_hasa_user VALUES (%s, %s)")
        # execute sql statement
        cursor.execute(sql, (comment['cid'],
                             comment['username']))

    # stores subreddit_has info
    for moderator in moderators:
        # create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_subreddit_hasa_user VALUES (%s, %s)")
        # execute sql statement
        cursor.execute(sql, (moderator['subredditName'],
                             moderator['username']))

    # create sql statement
    sql = ("INSERT IGNORE INTO reddatabase_subreddit VALUES (%s, %s)")
    # execute sql statement
    cursor.execute(sql, (subreddit_info['subredditName'],
                         subreddit_info['subscribers']))

    connection.commit()
    cursor.close()
    connection.close()


# Helper method for parsing through chains of comments
def comment_parser(root_comment, parent_comment_id, submission_id):
    comment_list = []
    if hasattr(root_comment, 'author.name'):  # catch deleted comments
        comment_data = {
            'cid': root_comment.id,
            'p_cid': parent_comment_id,
            'postid': submission_id,
            'text': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", root_comment.body),
            'username': re.sub("[^a-zA-z0-9!@#,/.,#!$%^&*;:{}=-_`~() /]+", "", root_comment.author.name),
            'score': root_comment.ups,
            'commentType': 0,  # comment is NOT a top level root comment
            'timeSubmitted': datetime.datetime.utcfromtimestamp(root_comment.created_utc)
        }
        comment_list.append(comment_data)
    for comment in root_comment.replies:
        comment_list.extend(comment_parser(comment, root_comment.id, submission_id))

    return comment_list


# iterates through list of requested subreddits
# and puts data on submissions, comments, and
# users into MySQL tables
def start_script():
    for subreddit in subreddits:
        print(subreddit)
        recent_submissions(subreddit)


start_script()