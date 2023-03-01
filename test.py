from helpers.top100coins import get_top_100_cryptos
import os

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



    # for keyword in keywords:
    #   if keyword.lower() in text.lower():
    #     script_dir = os.path.dirname(os.path.abspath(__file__))
    #     file_path = os.path.join(script_dir,
    #                              "../narratives/" + keyword.lower() + ".txt")
    #     with open(file_path, "a") as f:
    #       f.write(f"${ticker} - {fullName}({username}) - {url}\n")
    #     flag = True
    # if not flag:
    #   script_dir = os.path.dirname(os.path.abspath(__file__))
    #   file_path = os.path.join(script_dir, "../narratives/unknown" + ".txt")
    #   with open(file_path, "a") as f:
    #     f.write(f"${ticker} - {fullName}({username}) - {url}\n")


text = "test fsdfds"

result = getTickers(text)

if result:
    print("empty")