import os
import time
from slackclient import SlackClient
import praw
from random import randint
import mystuff


# constants
SLACK_BOT_TOKEN = mystuff.token
BOT_ID = mystuff.BOT_ID

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel, userid, joke_type):
    response = 'dummy'
    # add different response openers!!
    if joke_type is "dark":
        slack_client.api_call("chat.postMessage", channel=channel, text="you asked for it!", as_user=True)

        """
            Get a joke from reddit
        """
        reddit = praw.Reddit('test_bot')
        subreddit = reddit.subreddit("darkjokes")
        for submission in subreddit.top(limit=randint(1,50)):
            # print(submission.title.lower())
            # print(submission.selftext.lower())
            # if 'reddit' or 'AMA' or 'IAMA' or 'subreddit' or 'sub' or 'edit' in submission.title.lower():
            #     print "Here!"
            #     continue
            # elif 'reddit' or 'AMA' or 'IAMA' or 'subreddit' or 'sub' or 'edit' in submission.selftext.lower():
            #     print "Here!"
            #     continue
            response = submission.title + "\n" + submission.selftext
        time.sleep(2)
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)


    else:
        slack_client.api_call("chat.postMessage", channel=channel, text="joke time!", as_user=True)

        """
        	Get a joke from reddit
        """
        reddit = praw.Reddit('test_bot')
        subreddit = reddit.subreddit("cleanjokes")
        for submission in subreddit.hot(limit=randint(1,50)):
            # print(submission.title.lower())
            # print(submission.selftext.lower())
            # if 'reddit' or 'AMA' or 'IAMA' or 'subreddit' or 'sub' or 'edit' in submission.title.lower():
            #     print "Here!"
            #     continue
            # elif 'reddit' or 'AMA' or 'IAMA' or 'subreddit' or 'sub' or 'edit' in submission.selftext.lower():
            #     print "Here!"
            #     continue
            response = submission.title + "\n" + submission.selftext
        time.sleep(2)
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and BOT_ID not in output['user']:
                if 'joke' or 'jokes' in output['text'].lower():
                    if 'dark' or 'black' or 'racist' or 'bad' in output['text'].lower():
                        return output['text'].strip().lower(), \
                               output['channel'], \
                               output['user'], \
                               "dark"
                    else:
                        return output['text'].strip().lower(), \
                               output['channel'], \
                               output['user'], \
                               "clean"
            # elif output and 'text' in output and 'joke' in output['text'].lower() and BOT_ID not in output['user']:
            #     return output['text'].strip().lower(), \
            #            output['channel'], \
            #            output['user'], \
            #            "clean"
            # elif output and 'text' in output and 'jokes' in output['text'].lower() and BOT_ID not in output['user']:
            #     return output['text'].strip().lower(), \
            #            output['channel'], \
            #            output['user'], \
            #            "clean"
    return None, None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, userid, joke_type = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, userid, joke_type)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

