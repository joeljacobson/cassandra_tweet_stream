from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra.query import SimpleStatement
import json

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS twitter_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
        """
)

session.execute(
        """
         CREATE TABLE IF NOT EXISTS twitter_data.tweets ( user_id bigint, user_name text, tweet text, location text, PRIMARY KEY ((user_id), user_name));
        """
)

session.execute(
        """
        CREATE INDEX IF NOT EXISTS ON twitter_data.tweets (user_name);
       """
)

class ImportToCassandra:
    def process_tweet_list(self, list):
        
        batch = BatchStatement()
        
        for data in (list):
                try:
                    data = json.loads(data)
                    user_id = data['user']['id']
                    user_name = data['user']['screen_name']
                    tweet = data['text']
                    location = data['user']['location']
                    batch.add(SimpleStatement("INSERT INTO twitter_data.tweets (user_id, user_name, tweet, location) VALUES (%s, %s, %s, %s)"), (user_id, user_name, tweet, location)) 
                except:
                    pass
        
        session.execute(batch) 


        
    
        
    
    
