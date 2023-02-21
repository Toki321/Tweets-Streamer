import sys

sys.path.append("D:\\Coding Projects\\gemFinderNotifier\\tweet-notifier")

import os.path


def readIds(accountsToTrackListNumber):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "../accountsToTrack/accountsForTracking" +  accountsToTrackListNumber  + ".txt")

    with open(file_path, "r") as f:
        lines = f.readlines()
        toTrackIdList = []
        for line in lines:
            line = line.strip()
            try:
                toTrackIdList.append(line.split(" ")[1])
            except IndexError:
                print(line)

        return toTrackIdList



