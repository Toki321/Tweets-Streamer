import requests, os, tweepy
from helpers.tweepyClient import getTweepyClient
from helpers.top100coins import get_top_100_cryptos


class TweetPrinterV2(tweepy.StreamingClient):

  top_100_coins_dict = get_top_100_cryptos()
  CHAT_ID = os.getenv("CHAT_TWEET_ID")
  client = getTweepyClient()

  def on_tweet(self, tweet):
    ticker = self.isCorrect(tweet.text)
    url = f"https://twitter.com/{tweet.author_id}/status/{tweet.id}"
    if ticker != False:
      userObject = self.client.get_user(id=tweet.author_id)
      username = userObject[0]["username"]
      fullName = userObject[0]["name"]
      MESSAGE = f"{fullName} (@{username}) has tweeted ${ticker}\n\n{url}"
      self.postUrlToTelegram(MESSAGE)
      self.check_keywords(tweet.text, ticker, url, userObject)
    else:
      print("no ticker:", tweet.text, " ", url)

  def postUrlToTelegram(self, MESSAGE):
    TOKEN = os.getenv("TELEGRAM_GHOUL_TOKEN")
    print("sending tweet to tg: ", MESSAGE)
    call = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={MESSAGE}"
    requests.get(call).json()

  def isCorrect(self, text):
    tickerExists = False
    for word in text.split():
      if word.startswith("$"):
        ticker = word[1:].upper()
        if len(ticker) == 3 or len(ticker) == 4:
          tickerExists = True
          break
    if tickerExists:
      threeLetters = ticker[:3]
      if not self.isInTop100(threeLetters):
        return ticker
    return False

  def isInTop100(self, threeLetteres):
    try:
      get = self.top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
      return False
    return True

  def check_keywords(self, text, ticker, url, userObject):
    username = userObject[0]["username"]
    fullName = userObject[0]["name"]
    keywords = [
      "zk", "arbitrum", "optimism", "ai", "nftfi", "metaverse", "chinese",
      "perps", "bsc", "solidly"
    ]
    flag = False
    for keyword in keywords:
      if keyword.lower() in text.lower():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir,
                                 "../narratives/" + keyword.lower() + ".txt")
        with open(file_path, "a") as f:
          f.write(f"${ticker} - {fullName}({username}) - {url}\n")
        flag = True
    if not flag:
      script_dir = os.path.dirname(os.path.abspath(__file__))
      file_path = os.path.join(script_dir, "../narratives/unknown" + ".txt")
      with open(file_path, "a") as f:
        f.write(f"${ticker} - {fullName}({username}) - {url}\n")

  # def isCorrect(self, charArr):
  #     # if 3 letters and space
  #     if (
  #         charArr[0].isalpha() == True
  #         and charArr[1].isalpha() == True
  #         and charArr[2].isalpha() == True
  #     ):
  #         try:
  #             if charArr[3].isalpha() == False or charArr[4].isalpha() == False:
  #                 return True
  #         except:
  #             return True
  #     return False

  # def isTick(self, text):
  #     try:
  #         index = text.index("$")
  #     except:
  #         print("no ticker: ", text)
  #         return
  #     threeLetters = text[index + 1 : index + 3]
  #     if self.isInTop100(threeLetters) == True:
  #         return False
  #     else:
  #         substring = text[index + 1 : index + 6]
  #         return self.isCorrect(substring)

  def on_connect(self):
    print("connected")
