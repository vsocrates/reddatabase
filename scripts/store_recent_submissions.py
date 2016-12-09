import praw
import datetime
import MySQLdb

my_user_agent = 'Gafte'
my_client_id = 'IB4hdXbF1kcsWQ'
my_client_secret = '7uUB8oh9icfrneygPnJUMW1m6Xg'

#add subreddits to pull from here
subreddits = ['sweden']

#takes submission data and for all submissions,
#takes data on comments and users and stores
#all data in MySQL tables
def recent_submissions(subreddit_name):

    reddit = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret)

    recent_submissions = []
    recent_posts = []
    recent_users = []
    recent_comments = []
    counter = 0

    for submission in reddit.subreddit(subreddit_name).submissions():
        ratio = reddit.submission(id=submission.id,url=None).upvote_ratio
        ups = round((ratio * submission.score) / (2 * ratio - 1)) if ratio != 0.5 else round(submission.score / 2)
        downs = ups - submission.score

        if submission.selftext:
            postType = 'text'
            post_data = {
                'postid': submission.id,
                'contents': submission.selftext
            }
        else:
            postType = 'link'
            post_data = {
                'postid': submission.id,
                'contents': submission.url
            }

        user = reddit.redditor(submission.author.name)
        user_data = {
            'username': user.name,
            'karma': user.link_karma + user.comment_karma
        }

        submission_data = {
            'postid': submission.id, #unicode prefix 'u' may be issue? check database later
            'username': submission.author.name,
            'title': submission.title,
            'subredditName': subreddit_name,
            'upvotes': ups,
            'downvotes': downs,
            'postType': postType,
            'timeSubmitted': datetime.datetime.utcfromtimestamp(submission.created_utc)
        }
        print(submission_data)

        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            comment_data = {
                'cid': comment.id,
                'p_cid': submission.id,
                'postid': submission.id,
                'text': comment.body,
                'username': comment.author.name,
                'score': comment.ups,
                'commentType': "placeholder",
                'timeSubmitted': datetime.datetime.utcfromtimestamp(comment.created_utc)
            }
            recent_comments.append(comment_data)
            for reply in comment.replies:
                recent_comments.append(comment_parser(reply, comment.id, submission.id))

        recent_submissions.append(submission_data)
        recent_posts.append(post_data)
        recent_users.append(user_data)

        if counter == 100:
            break
        else:
            counter = counter + 1

    #Create connection
    connection = MySQLdb.connect("127.0.0.1","root","reddatabase","RDB")
    cursor = connection.cursor()

    for user in recent_users:
        #create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_user (username, karma) VALUES (%s, %s)")
        #execute sql statement
        cursor.execute(sql, (user['username'],
                            user['karma']))

    for submission in recent_submissions:
        #create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_submission VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        #execute sql statement
        cursor.execute(sql, (submission['postid'],
                            submission['username'],
                            submission['subredditName'],
                            submission['title'],
                            submission['upvotes'],
                            submission['downvotes'],
                            submission['postType'],
                            submission['timeSubmitted']))

    for post in recent_posts:
        #create sql statement
        sql = ("INSERT IGNORE INTO reddatabase_" + postType + "post VALUES (%s, %s)")
        #execute sql statement
        cursor.execute(sql, (post['postid'],
                            post['contents']))


    connection.commit()
    cursor.close()
    connection.close()

#Helper method for parsing through chains of comments
def comment_parser(root_comment, parent_comment_id, submission_id):

    comment_list = []
    if hasattr(root_comment, 'author.name'): #catch deleted comments
        comment_data = {
            'cid': root_comment.id,
            'p_cid': parent_comment_id,
            'postid': submission_id,
            'text': root_comment.body,
            'username': root_comment.author.name,
            'score': root_comment.ups,
            'commentType': "placeholder",
            'timeSubmitted': datetime.datetime.utcfromtimestamp(root_comment.created_utc)
        }
        comment_list.append(comment_data)
    for comment in root_comment.replies:
        comment_list.append(comment_parser(comment,root_comment.id,submission_id))

    return comment_list

#iterates through list of requested subreddits
# and puts data on submissions, comments, and
# users into MySQL tables
def start_script():
    for subreddit in subreddits:
        recent_submissions(subreddit)

start_script()
