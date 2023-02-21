import sys
import multiprocessing

sys.path.append("D:\\Coding Projects\\gemFinderNotifier\\tweet-notifier")

from streamTweets import streamTweets

if __name__ == "__main__":
    # Create two processes, one for each script
    p2 = multiprocessing.Process(target=streamTweets)

    # Start the processes
    p2.start()

    # Wait for the processes to finish
    p2.join()
