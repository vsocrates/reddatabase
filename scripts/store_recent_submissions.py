import praw
import datetime
import MySQLdb

my_user_agent = 'Gafte'
my_client_id = 'IB4hdXbF1kcsWQ'
my_client_secret = '7uUB8oh9icfrneygPnJUMW1m6Xg'

#add subreddits to pull from here
subreddits = ['sweden']

def recent_submissions(subreddit_name):

    reddit = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret)

    recent_submissions = []
    recent_posts = []
    recent_users = []
    counter = 0

    for submission in reddit.subreddit(subreddit_name).submissions():
        ratio = reddit.submission(id=submission.id,url=None).upvote_ratio
        ups = round((ratio * submission.score) / (2 * ratio - 1)) if ratio != 0.5 else round(submission.score / 2)
        downs = ups - submission.score

        if submission.url:
            postType = 'link'
            post_data = {
                'postid': submission.id,
                'contents': submission.url
            }
        else:
            postType = 'text'
            post_data = {
                'postid': submission.id,
                'contents': submission.selftext
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

        recent_submissions.append(submission_data)
        recent_posts.append(post_data)
        recent_users.append(user_data)

        if counter == 100:
            break
        else:
            counter = counter + 1

    #Create connection
    connection = MySQLdb.connect(host="127.0.0.1:3306",user="root",passwd="reddatabase",db="RDB")
    print(connection.)
    for submission in recent_submissions:
        try:
            with connection.cursor() as cursor:
                #create sql statement
                sql = ("INSERT INTO reddatabase_submission VALUES (%s, %s, %s, %s, %s, %s)")
                #execute sql statement
                cursor.execute(sql, (submission['postid'],
                                    submission['username'],
                                    submission['title'],
                                    submission['subredditName'],
                                    submission['upvotes'],
                                    submission['downvotes'],
                                    submission['postType'],
                                    submission['timeSubmitted']))
        except:
            print("submissions", sys.exc_info()[0])
        finally:
            pass

    for post in recent_posts:
        try:
            with connection.cursor() as cursor:
                #create sql statement
                sql = ("INSERT INTO reddatabase_" + postType + " VALUES (%s, %s)")
                #execute sql statement
                cursor.execute(sql, (post['postid'],
                                    post['contents']))
        except:
            print("posts", sys.exc_info()[0])
        finally:
            pass

    for user in recent_users:
        try:
            with connection.cursor() as cursor:
                #create sql statement
                sql = ("INSERT INTO reddatabase_users VALUES (%s, %s)")
                #execute sql statement
                cursor.execute(sql, (user['username'],
                                    user['karma']))
        except:
            print("users", sys.exc_info()[0])
        finally:
            pass
        connection.close()

def start_script():
    for subreddit in subreddits:
        recent_submissions(subreddit)

start_script()
