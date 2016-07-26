from flask import Flask
from flask_cassandra import CassandraCluster
from flask import jsonify
from cassandra.query import SimpleStatement
from flask import request
from flask import render_template
import solr

app = Flask(__name__)

cassandra = CassandraCluster()

app.config['CASSANDRA_NODES'] = ['127.0.0.1']  # can be a string or list of nodes

solr = solr.Solr('http://127.0.0.1:8983/solr/twitter_data.tweets/')

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/api/tweets")
def cassandra_test():
    session = cassandra.connect()
    session.set_keyspace("twitter_data")
    query = "SELECT user_id, user_name, location, tweet FROM tweets"
    statement = SimpleStatement(query, fetch_size=10)
    rows = session.execute(statement)

    list = []

    for row in rows:
        list.append({'user_id': row[0], 'user_name': row[1], 'location': row[2], 'tweet': row[3]})
    return jsonify(list)

@app.route("/api/search")
def search_tweets():
    response = solr.select(request.args.get('q'))

    list = []

    for hit in response.results:
        list.append(hit)
    return jsonify(list)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


if __name__ == '__main__':
    app.run()
