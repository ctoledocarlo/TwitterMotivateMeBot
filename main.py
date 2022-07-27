import requests
import os
import tweepy
import time
import schedule
import json
import random
import textwrap

from PIL import Image, ImageEnhance
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO

from keepAlive import keep_alive


def getAPI():
    key = os.environ['apiKey']
    keySecret = os.environ['keySecret']
    accessToken = os.environ['accessToken']
    accessTokenSecret = os.environ['accessTokenSecret']

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(key, keySecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    # Create API object
    api = tweepy.API(auth)
    return api


def tweetText():
    api = getAPI()
    api.update_status(f'Tweeting')


def getQuote():
    quoteChoice = random.randint(1, 1643)

    response = requests.get("https://type.fit/api/quotes")
    json_data = json.loads(response.text)
    quote = json_data[quoteChoice]['text']
    author = json_data[quoteChoice]['author']

    return quote, author


def tweetPic():
    api = getAPI()

    url = "https://random.imagecdn.app/v1/image?width=1920&height=1080&category=buildings&format=png"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)

    quoteAuthor = getQuote()
    quote = quoteAuthor[0]
    author = quoteAuthor[1]

    draw = ImageDraw.Draw(img)
    quoteFont = ImageFont.truetype('ReallyFree-ALwl7.ttf', 200)
    authorFont = ImageFont.truetype('WhiteScratches-1GyOZ.ttf', 170)

    maxW = 1920
    height = 200
    quoteWrap = textwrap.wrap(quote, width=30)

    if len(quoteWrap) < 3:
        quoteFont = ImageFont.truetype('ReallyFree-ALwl7.ttf', 250)
        quoteWrap = textwrap.wrap(quote, width=20)
    if len(quoteWrap) == 4:
        quoteFont = ImageFont.truetype('ReallyFree-ALwl7.ttf', 150)
        quoteWrap = textwrap.wrap(quote, width=45)
    if len(quoteWrap) > 4:
        quoteFont = ImageFont.truetype('ReallyFree-ALwl7.ttf', 80)
        quoteWrap = textwrap.wrap(quote, width=60)
        height = 150

    current_h, pad = 100, 10
    for line in quoteWrap:
        w, h = draw.textlength(line, font=quoteFont), height
        draw.text(((maxW - w) / 2, current_h), line, font=quoteFont)
        current_h += h + pad

    try:
      w = draw.textlength(author, font=authorFont)
      draw.text(((maxW - w) / 2, 900), author, font=authorFont)
    except:
      author = 'Unknown Author'
      w = draw.textlength(author, font=authorFont)
      draw.text(((maxW - w) / 2, 900), author, font=authorFont)

    img.save('mediaFile.png')

    api.update_status_with_media(status='', filename='mediaFile.png')

    print(f'Status Updated! Lines: {len(quoteWrap)}')


def main():
  tweetPic()
  time.sleep(60)
  main()
    
keep_alive()
main()