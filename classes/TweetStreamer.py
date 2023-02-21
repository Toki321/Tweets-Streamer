import sys, os
sys.path.append("D:\\Coding Projects\\gemFinderNotifier\\tweet-notifier")
from tweepy import StreamingClient, StreamRule
from dotenv import load_dotenv

from classes.TweetPrinterV2 import TweetPrinterV2

load_dotenv()


class TweetStreamer:


    def __init__(self, list1, list2, list3, list4, BEARER_TOKEN):
        self.accountsList1 = list1
        self.accountsList2 = list2
        self.accountsList3 = list3
        self.accountsList4 = list4
        self.BEARER_TOKEN = BEARER_TOKEN
        self.tweetPrinter = TweetPrinterV2(BEARER_TOKEN)

    def cleanRules(self):
        ruleIds = []
        rules = self.tweetPrinter.get_rules()
        rulesArr = rules.data
        if rulesArr != None:
            for rule in rulesArr:
                print(f"rule marked to delete: {rule.id} - {rule.value}")
                ruleIds.append(rule.id)

            if len(ruleIds) > 0:
                self.tweetPrinter.delete_rules(ruleIds)
                self.tweetPrinter = TweetPrinterV2(self.BEARER_TOKEN)
            else:
                print("no rules to delete")

    def ruleString(self, flag):
        index = 0
        ruleString = ""
        if flag == 1:
            for account in self.accountsList1:
                ruleString += "from: " + account + " "
                if index != len(self.accountsList1) - 1:
                    ruleString += "OR "
                index += 1
        elif flag == 2:
            for account in self.accountsList2:
                ruleString += "from: " + account + " "
                if index != len(self.accountsList2) - 1:
                    ruleString += "OR "
                index += 1
        elif flag == 3:
            for account in self.accountsList3:
                ruleString += "from: " + account + " "
                if index != len(self.accountsList4) - 1:
                    ruleString += "OR "
        elif flag == 4:
            for account in self.accountsList4:
                ruleString += "from: " + account + " "
                if index != len(self.accountsList4) - 1:
                    ruleString += "OR "
        print()
        print(ruleString)
        print()
        return ruleString

    def startStreaming(self):
        self.cleanRules()
        rules = []
        rules.append(StreamRule(self.ruleString(1)))
        rules.append(StreamRule(self.ruleString(2)))
        # rules.append(StreamRule(self.ruleString(3)))
        # rules.append(StreamRule(self.ruleString(4)))
        print(rules)
        self.tweetPrinter.add_rules(rules)
        self.tweetPrinter.filter(expansions="author_id", media_fields="url")
