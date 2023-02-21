import sys, os

sys.path.append("D:\\Coding Projects\\gemFinderNotifier\\tweet-notifier")

from classes.TweetStreamer import TweetStreamer
from helpers.idsToTrack import readIds


def streamTweets():
    # listAccounts = readIds()
    listAccounts1 = readIds('1')
    listAccounts2 = readIds('2')
    listAccounts3 = readIds('3')
    listAccounts4 = readIds('4')
    listAccounts1.append("2966287497")
    listAccounts1.append("1449328468227932163")

    BEARER_TOKEN = os.getenv("BEARER_TOKEN_1")

    streamerOne = TweetStreamer(listAccounts1, listAccounts2, listAccounts3, listAccounts4, BEARER_TOKEN)

    streamerOne.startStreaming()

streamTweets()