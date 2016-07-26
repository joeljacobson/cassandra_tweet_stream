from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("Tweet Analyser")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
sqlContext.read.format("org.apache.spark.sql.cassandra").options(table="tweets", keyspace="twitter_data").load().show()
