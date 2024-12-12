from flask_cors import CORS, cross_origin
from flask import request, jsonify, Flask
import psycopg2
from datetime import datetime, date
import json

con = psycopg2.connect(
    database="",
    user="postgres",
    password="7084",
    host="localhost",
    port='5432'
)

app = Flask(__name__)
cors = CORS(app)

@app.route("/database", methods=['GET'])
@cross_origin()
def get_max_score():
    try:
        cursor_obj = con.cursor()
        # Fetch all records from scores table
        cursor_obj.execute("SELECT score FROM public.scores;")
        result = cursor_obj.fetchall()
        
        max_score = 0
        scores = []
        for record in result:
            # Assuming record[1] is the 'score' column
            scores.append(record[0])
            if record[0] > max_score:
                max_score = record[0]

        max_scores = [max_score]
        return json.dumps(max_scores)

    except Exception as e:
        print("Error:", e)
        return json.dumps({"error": str(e)})


@app.route("/database/<score>", methods=['POST'])
@cross_origin()
def post_new_score(score=None):
    try:
        cursor_obj = con.cursor()
        # Fetch all existing scores to find the highest id
        cursor_obj.execute('SELECT * FROM public.scores;')
        result = cursor_obj.fetchall()

        latest_id = 0
        for record in result:
            if record[1] > latest_id:
                latest_id = record[1]

        post_return = [latest_id + 1, score]

        register_date_str = datetime.now().strftime("%Y-%m-%d")
        year, month, day = map(int, register_date_str.split('-'))
        register_date = date(year, month, day)

        # Insert new score record
        query = """
            INSERT INTO public.scores (id, score, date)
            VALUES (%s, %s, %s);
        """
        cursor_obj.execute(query, (latest_id + 1, score, register_date))
        con.commit()  # Make sure to commit the transaction

        return json.dumps(post_return), 201  # Return a 201 Created status

    except Exception as e:
        # Roll back on error and return an error message
        con.rollback()
        print("Error:", e)
        return json.dumps({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
