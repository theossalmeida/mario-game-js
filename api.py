from flask_cors import CORS, cross_origin
from flask import request, jsonify, Flask
import psycopg2
from datetime import datetime, date
import json


con = psycopg2.connect(
database="scores-database",
user="postgres",
password="7084",
host="localhost",
port= '5432'
)

app = Flask(__name__)
cors = CORS(app)

@app.route("/database", methods=['GET'])
@cross_origin()
def get_max_score():

    cursor_obj = con.cursor()
    result = cursor_obj.fetchall()
    max_score = 0
    scores = []
    for record in result:
        scores.append(record[1])
        if record[1] > max_score:
            max_score = record[1]
    max_scores = [max_score]
    
    return json.dumps(max_scores)

@app.route("/database/<score>", methods=['POST'])
@cross_origin()
def post_new_score(score=None):

    cursor_obj = con.cursor()
    cursor_obj.execute('SELECT * FROM scores')
    result = cursor_obj.fetchall()
    latest_id = 0
    for record in result:
        if record[0] > latest_id:
            latest_id = record[0]

    post_return = [latest_id + 1, score]

    register_date_str = datetime.now().strftime("%Y-%m-%d")
    year = int(register_date_str.split('-')[0])
    month = int(register_date_str.split('-')[1])
    day = int(register_date_str.split('-')[2])
    register_date = date(year, month, day)

    query = """INSERT INTO
    scores (id, score, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    cursor_obj.execute(query, (latest_id + 1, score, register_date))
    con.commit

    return json.dumps(post_return)

app.run()