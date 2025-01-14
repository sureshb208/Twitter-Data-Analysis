import json
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    i = 0
    for tweets in open(json_file, "r"):
        i += 1
        tweets_data.append(json.loads(tweets))
        # if i == 100: 
            #'limit to 100'
            # break

    return len(tweets_data), tweets_data


[
    "created_at",
    "id",
    "id_str",
    "text",
    "truncated",
    "entities",
    "source",
    "in_reply_to_status_id",
    "in_reply_to_status_id_str",
    "in_reply_to_user_id",
    "in_reply_to_user_id_str",
    "in_reply_to_screen_name",
    "user",
    "geo",
    "coordinates",
    "place",
    "contributors",
    "retweeted_status",
    "is_quote_status",
    "retweet_count",
    "favorite_count",
    "favorited",
    "retweeted",
    "lang",
]

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        return [t['user']['statuses_count'] for t in self.tweets_list]

    def find_full_text(self)->list:
        return [t['text'] for t in self.tweets_list]


    def find_sentiments(self, text)->list:
        """
        this function will find the polarity and subjectivity of the tweet
        Args:
        -----
        text: list of tweets

        Returns
        -------
        list of polarity and subjectivity
        """
        polarity = []
        subjectivity = []
        for t in text:
            blob = TextBlob(t)
            polarity.append(blob.sentiment.polarity)
            subjectivity.append(blob.sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self)->list:
        return [t['created_at'] for t in self.tweets_list]

    def find_source(self)->list:
        return [t['source'] for t in self.tweets_list]

    def find_screen_name(self)->list:
        return [t['user']['screen_name'] for t in self.tweets_list]

    def find_followers_count(self)->list:
        return [t['user']['followers_count'] for t in self.tweets_list]

    def find_friends_count(self)->list:
        return [t['user']['friends_count'] for t in self.tweets_list]

    def find_lang(self)->list:
        return [t['lang'] for t in self.tweets_list]

    def is_sensitive(self)->list:
        lst = []
        for x in self.tweets_list:
            try:
                is_sensitive =  x['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            lst.append(is_sensitive)
        return lst

    def find_favourite_count(self)->list:
        return [t['favorite_count'] for t in self.tweets_list]


    def find_retweet_count(self)->list:
        return [t['retweet_count'] for t in self.tweets_list]

    def find_hashtags(self)->list:
        return [t['entities']['hashtags'] for t in self.tweets_list]

    def find_mentions(self)->list:
        return [t['entities']['user_mentions'] for t in self.tweets_list]


    def find_location(self)->list:
        locations = []
        for t in self.tweets_list:
            try:
                locations.append(t['user']['location'])
            except KeyError:
                locations.append('')
        return locations


    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count',
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = [
        "created_at",
        "source",
        "original_text",
        "clean_text",
        "sentiment",
        "polarity",
        "subjectivity",
        "lang",
        "favorite_count",
        "retweet_count",
        "original_author",
        "screen_count",
        "followers_count",
        "friends_count",
        "possibly_sensitive",
        "hashtags",
        "user_mentions",
        "place",
        "place_coord_boundaries",
    ]
    _, tweet_list = read_json("data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
