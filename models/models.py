import sqlalchemy as db
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from typing import List

engine = db.create_engine('sqlite:///app.db', echo = True)
connection = engine.connect()
meta = db.MetaData()

class Base(DeclarativeBase):
     pass

class Narative(Base):
    __tablename__ = "narative"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))

    keywords: Mapped[List["Keyword"]] = relationship(
             backref="narative", cascade="all"
    )
    tweets: Mapped[List["Tweet"]] = relationship(
             backref="narative", cascade="all"
    )

    def __repr__(self) -> str:
        return f"{self.title!r}"
    
class Keyword(Base):
    __tablename__ = "keyword"

    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(30))

    narative_id: Mapped[int] = mapped_column(ForeignKey("narative.id"))

    def __repr__(self) -> str:
        return f"{self.keyword!r}"

class Ticker(Base):
    __tablename__ = "ticker"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"{self.ticker!r}"
    
class TwitterUser(Base):
    __tablename__ = "twitter_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    user_twitter_id : Mapped[int] = mapped_column(String(30))
    
    tweets: Mapped[List["Tweet"]] = relationship(
             backref="twitter_user", cascade="all"
    )
    
    def __repr__(self) -> str:
        return f"{self.username!r}"

class Tweet(Base):
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    twitter_user_id: Mapped[int] = mapped_column(ForeignKey("twitter_user.id"))
    narative_id: Mapped[int] = mapped_column(ForeignKey("narative.id"))

    twitter_tweet_id: Mapped[str] = mapped_column(String(30))
    # datetime_of_writing =  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def __repr__(self) -> str:
        return f"Tweet (id={self.id!r}, twitter_id={self.twitter_tweet_id!r}"
    
class TweetsAndTickers(Base):
    __tablename__ = "tweets_and_tickers"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    ticker_id: Mapped[int] = mapped_column(ForeignKey("ticker.id"))
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweet.id"))

    def __repr__(self):
        return f'<Relationship {self.ticker_id} : {self.tweet_id}>'



# with Session(engine) as session:

#     session.add(TwitterUser(username="_dushan_c", user_twitter_id=1593781370333061121))
#     session.commit()

    # naratives = ["zk", "solidly", "ai", "nftfi", "chinese alpha" ,"bsc" ,"perps" , "arbitrum" ,"optimism" ,"metaverse"]
    # keywords_arr = [
    #     ["zero knowledge",  "rollup", "zero-knowledge", "$fin", "$zkp", "$zks", "$zz", "$dusk", "$xft", "$cell", "$matic", "$fra", "$vcash"],
    #     ["solidly", "ve(3,3)", "ve",  "$solid", "$sliz", "$the", "$velo"],
    #     ["artificial intelligence", "ai"],
    #     ["nft-fi", "nftifi", "nft fi"],
    #     ["chinese", "china"],
    #     ["binance smart chain", "bsc", "bnb chain"],
    #     ["perp", "perps"],
    #     ["arbitrum"],
    #     ["optimism", "op"],
    #     ["metaverse"]
    # ]
   
    # i = 0
    # for narative in naratives:
    #     session.add(Narative(title=narative))
    #     session.commit()
    #     nar = session.execute(select(Narative).filter_by(title=narative)).scalar_one()
    #     for word in keywords_arr[i]:
    #         session.add(Keyword(keyword=word, narative_id=nar.id))
    #         session.commit()
    #     i+=1


#     twitter_user = Narative(title="china")
#     session.add(twitter_user)
#     session.commit()

    
    # with open("accountsForTracking4.txt", 'r') as f:
    #     string = f.readlines()
    #     for line in string:
    #         line.strip()
    #         line = line.split(' ')
    #         twitter_user = TwitterUser(username=line[0], user_twitter_id = line[1])
    #         session.add(twitter_user)
    #         session.commit()

    # narative = Narative(title="china")
    # keyword = Keyword(keyword="buy", narative_id = 1)
    # ticker = Ticker(ticker="$BUSDT")
    # twitter_user = TwitterUser(username="toki", user_twitter_id = 1223, full_twitter_name="tokisan")
    # tweet = Tweet(ticker_id = 1, twitter_user_id = 1, narative_id = 1, twitter_tweet_id = 123)
    
    # session.add(narative)
    # session.add(keyword)
    # session.add(ticker)
    # session.add(twitter_user)
    # session.add(tweet)
    # session.commit()
    # tweet = session.execute(select(Tweet).filter_by(twitter_tweet_id=123)).scalar_one()

    # print(tweet.narative.keywords)
# narative = db.Table('narative', meta,  autoload_with=engine)
# keyword = db.Table('keyword', meta,  autoload_with=engine)
# ticker = db.Table('ticker', meta,  autoload_with=engine)
# twitter_user = db.Table('twitter_user', meta,  autoload_with=engine)
# tweet = db.Table('tweet', meta,  autoload_with=engine)


