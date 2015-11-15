import argparse
from pprint import pprint
import sys
import traceback

import tweepy

CONSUMER_KEY = 'sHMFd65BcXRN3ybBBy698HPzo'
CONSUMER_SECRET = 'SdA9D40qt6dMkZTfWv7z8ySOC9wWZcvL3ERO6LF58Pcu6ZTVwA'
ACCESS_TOKEN = '2332819196-DV9Ls6H8IYFlzzqf3kfcmozRvuCm3XmGFPshDMj'
ACCESS_TOKEN_SECRET = '30IFrMpnoeeiKsCa3epmeqwn7HRWOMUc29hr7ZNYkcYH7'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def GetTweepyAPIObject():
    '''The singleton tweepy API instance.'''
    if not hasattr(GetTweepyAPIObject, '_api'):
        GetTweepyAPIObject._api = tweepy.API(auth)
    return GetTweepyAPIObject._api

def configure_args():
    '''Configures the commandline arguments.'''
    parser = argparse.ArgumentParser(description='The interface for the twitter API.')
    parser.add_argument('username', help='Twitter handle to retrieve tweets for.')
    parser.add_argument('--max-count', type=int, help='The max number of tweets to retrieve.')
    return parser.parse_args()

def get_tweets_from_handle(handle, max_count=None):
    '''Retrieves all of the tweets for the given handle.'''
    api = GetTweepyAPIObject()

    cursor = tweepy.Cursor(api.user_timeline, screen_name=handle, wait_on_rate_limit=True)
    if max_count:
        iterator = cursor.items(max_count)
    else:
        iterator = cursor.items()

    for status in iterator:
        if 'media' in status.entities:
            continue
        elif len(status.text) < 30:
            continue
        elif 'RT' in status.text:
            continue
        yield status.text

def main():
    '''The main entry point for the program.'''
    args = configure_args()

    max_count = None
    if args.max_count:
        max_count = args.max_count

    for tweet in get_tweets_from_handle(args.username, max_count=max_count):
        print tweet

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        sys.exit(traceback.format_exc())
