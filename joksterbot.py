import os
import time
from slackclient import SlackClient
import praw
from random import randint

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
# AT_BOT = "<@" + BOT_ID + ">"
# EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel, userid):
    
    slack_client.api_call("chat.postMessage", channel=channel, text="someone said joke?!", as_user=True)

    """
    	Get a joke from reddit
    """
    reddit = praw.Reddit('test_bot')
    subreddit = reddit.subreddit("jokes")
    for submission in subreddit.top(limit=randint(1,100)):
    	response = submission.title + ", " + submission.selftext
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
            if output and 'text' in output and 'joke' in output['text'] and BOT_ID not in output['user']:
                return output['text'].strip().lower(), \
                       output['channel'], \
                       output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, userid = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, userid)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")