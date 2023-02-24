from helpers.top100coins import get_top_100_cryptos


top_100_coins_dict = get_top_100_cryptos()

def isInTop100(threeLetteres):
    try:
      get = top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
      return False
    return True

def getTickers(text):
    tickers = []
    for word in text.split(" "):
        if word.startswith("$") and not word[1:].isdigit():
            ticker = word[1:].upper()
            if len(ticker) == 3 or len(ticker) == 4:
                threeLetters = ticker[:3]
                if not isInTop100(threeLetters):
                    tickers.append(ticker)
    return tickers


text = "test fsdfds"

result = getTickers(text)

if result:
    print("empty")