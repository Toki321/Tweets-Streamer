import requests, os, tweepy
from helpers.tweepyClient import getTweepyClient
from helpers.top100coins import get_top_100_cryptos
from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy as db
from models import models



class TweetPrinterV2(tweepy.StreamingClient):

  top_100_coins_dict = get_top_100_cryptos()
  CHAT_ID = os.getenv("CHAT_TEST_ID")
  client = getTweepyClient()

  def on_tweet(self, tweet):
    tickers = self.getTickers(tweet.text)

    url = f"https://twitter.com/{tweet.author_id}/status/{tweet.id}"

    if tickers:
      userObject = self.client.get_user(id=tweet.author_id)

      username = userObject[0]["username"]
      fullName = userObject[0]["name"]

      tickerString = ""
      for ticker in tickers:
        tickerString += "$" + ticker + ", "
        
      MESSAGE = f"{fullName} (@{username}) has tweeted ${tickerString}\n\n{url}"
      self.postUrlToTelegram(MESSAGE)
     
      engine = db.create_engine('sqlite:///app.db', echo = True)
      tweet_id = 0
      twitter_user_found = None
      with Session(engine) as session:
        naratives = session.scalars(select(models.Narative).order_by(models.Narative.id)).all()
        print(naratives)
        for narative in naratives:
          # narative = session.execute(select(models.Narative).filter_by(title=narative)).scalar_one()
          id = self.checkForSingleNarrative(tweet.text, narative)
          if id:
            try:  
              twitter_user_found = session.execute(select(models.TwitterUser).filter_by(user_twitter_id=tweet.author_id)).scalar_one()
            except:
              print("Add this user")

            tweet_to_make = models.Tweet(twitter_user_id=twitter_user_found.id, narative_id=id, twitter_tweet_id=tweet.id)
            session.add(tweet_to_make)
            session.commit()
            tweet_id = tweet_to_make.id
            break
          
      for ticker in tickers:   
        with Session(engine) as session:
          ticker_found = None
          try:
            ticker_found = session.execute(select(models.Ticker).filter_by(ticker=ticker)).scalar_one()
          except:
            pass

          if not ticker_found:
            ticker_found = models.Ticker(ticker=ticker)
            session.add(ticker_found)
            session.commit()
            

          relation = models.TweetsAndTickers(tweet_id=tweet_id, ticker_id=ticker_found.id)
          session.add(relation)
          session.commit()
           
        
    else:
      print("no ticker:", tweet.text, " ", url)


  def postUrlToTelegram(self, MESSAGE):
    TOKEN = os.getenv("TELEGRAM_GHOUL_TOKEN")
    print("sending tweet to tg: ", MESSAGE)
    call = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={MESSAGE}"
    requests.get(call).json()


  def getTickers(self, text):
    tickers = []
    for word in text.split(" "):
        if word.startswith("$") and not word[1:].isdigit():
            ticker = word[1:].upper()
            if len(ticker) == 3 or len(ticker) == 4:
                threeLetters = ticker[:3]
                if not self.isInTop100(threeLetters):
                    tickers.append(ticker)
    return tickers


  def isInTop100(self, threeLetteres):
    try:
      get = self.top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
      return False
    return True


  # def checkForEachNarrative(self, text, narratives): 
  #   for narrative in narratives:
  #       # keywords =  query for keywords for each narrative
  #       self.checkForSingleNarrative(text, narrative)

  def checkForSingleNarrative(self, text, narrative):
    text = text.lower()
    print("narative: ",narrative, " type: ", type(narrative))
    for keyword in narrative.keywords:
        if keyword.keyword.lower() in text:
          return narrative.id
    return 0
        
  def on_connect(self):
    print("connected")
