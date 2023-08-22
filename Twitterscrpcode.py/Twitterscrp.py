import pandas as pd
import snscrape.modules.twitter as snx
import json
from pymongo import MongoClient
import datetime
import base64
import streamlit as st

#--------------------------Extracting data from twitter using snscrape-------------------------------------
tweet_list = []
def scrape_twitterdata(search_term, start_time, end_time, tweets_count):
    for i, tweet in enumerate(snx.TwitterSearchScraper(f"{search_term} since:{start_time} until:{end_time}").get_items):
        if i > tweets_count:
            break
        tweet.append([tweet.id, tweet.date, tweet.content, tweet.user.username, tweet.retweetcount, tweet.likecount])
    # Appending the extracted values into emply list which already created in dictonary form
    tweet_list.append({'id':str(tweet.id),
                       'data':str(tweet.date),
                       'content': tweet.content,
                       'uswername': tweet.user.username,
                       'retweets': tweet.retweetcount,
                        'likes': tweet.likecount
                    })
    return json.dump(tweet_list)

    # The extracted tweets data inserted into mongodb using function

def insert_into_mongodb(scrape_term, tweets):
    connect = MongoClient("mongodb://localhost:27017")
    db = connect['Twitter_scrape']
    data = db['Tweets']

    data.insert_one({"scrape word": scrape_term,
                      "scraped date": datetime.today(),
                      "scraped data": [tweets]})
    
    # The tweet converted into CSV using function
    
def convert_into_csv(json_tweet):
    df_tweet = pd.read_json(json_tweet)
    csv_file = pd.to_csv(df_tweet)
    return csv_file
    
    # The tweets converted into json using fuction
def convert_into_json(json_tweet):
    df_tweet = pd.read_json(json_tweet)
    st.dataframe(df_tweet)
    

def main():
    
    st.title(":yellow[Twitter Scraping]")
    st.write("Enter a search term & date range & tweet_limit to scrape data from Twitter")

    # Get the input from user
    search_term = st.text_input('Search term')
    start_time = st.date_input("Start time")
    end_time = st.date_input('End time')
    tweet_count = st.number_input('Tweet limit', min_value=1, max_value=6000, value=100)

    if st.button("scrape"):
       json_tweet = scrape_twitterdata(search_term, start_time.strftime('%y-%m-%d', end_time.strftime('%y-%m-%d', tweet_count)))
       df_tweet = pd.read_json(json_tweet)
       st.dataframe(df_tweet)

    if st.button("upload to Mongodb"):
       json_tweet = scrape_twitterdata(search_term, start_time.strftime('%y-%m-%d', end_time.strftime('%y-%m-%d', tweet_count)))
       insert_into_mongodb(search_term, json_tweet)

    if st.button('uplode to CSV'):
       json_tweet = scrape_twitterdata(search_term, start_time.strftime('%y-%m-%d', end_time.strftime('%y-%m-%d', tweet_count)))
       convert_into_csv(json_tweet)

    if st.button('upload to json'):
       json_tweet = scrape_twitterdata(search_term, start_time.strftime('%y-%m-%d', end_time.strftime('%y-%m-%d', tweet_count)))
       convert_into_json(json_tweet)

main()

     