#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from import_to_cassandra import ImportToCassandra

#Variables that contains the user credentials to access Twitter API
access_token = "access_token"
access_token_secret = "access_token_secret"
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"        

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    tweet_list = []

    def on_data(self, data):
        self.tweet_list.append(data)
        if len(self.tweet_list) >= 10:
            self.process_tweet_list()
        return True

    def process_tweet_list(self):
        ImportToCassandra().process_tweet_list(self.tweet_list)
        self.tweet_list = []

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'

    stream.filter(track=['datastax', 'mongodb', 'couchbase', 'riak', 'redis', 'neo4j', 'titandb'])
