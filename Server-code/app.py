from flask import Flask, request, jsonify, Response
import sqlite3



app = Flask(__name__)

@app.route("/register", methods=["POST"])
def new_user() -> Response:
    # Get the username sent inside a dictionary, json style
    data = request.get_json()
    username = data["username"] # Access the username given that data is a dictionary
    conn = sqlite3.connect("/Users/viniciusferrari/Documents/Richouse/Server-code/GlobalDatabase.db") # Connect with database
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user (username) VALUES (?)', (username,)) # Check with username already exist, as username is primary
                                                                              # key it will return error if already exist
        conn.commit()
        conn.close()
        return jsonify(success=True) # Return successful status
    except:
        conn.close() 
        return jsonify(success=False) # Return unsuccessful status
    
@app.route("/rank")
def ranking() -> Response:
    conn = sqlite3.connect("/Users/viniciusferrari/Documents/Richouse/Server-code/GlobalDatabase.db") # connect with databse
    cursor = conn.cursor()
    cursor.execute("SELECT user, time FROM results WHERE map = 'baker' ORDER BY time LIMIT 10") # Get the best 10 scorers in
                                                                                                       # Baker Avenue
    resultsBaker = cursor.fetchall()
    cursor.execute("SELECT user, time FROM results WHERE map = 'usbourne' ORDER BY time LIMIT 10") # Get the best 10 scorers in
                                                                                                       # Usbourne Way
    resultsUsbourne = cursor.fetchall()
    return jsonify({"Baker": resultsBaker, "Usbourne": resultsUsbourne}) # return both ranks in a json format
    
@app.route("/bestTime", methods=["POST"])
def best_time() -> None:
    data = request.get_json()
    bestTime = data["bestTime"]
    map = data["map"]
    user = data["username"]
    conn = sqlite3.connect("/Users/viniciusferrari/Documents/Richouse/Server-code/GlobalDatabase.db") # Connect with database
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO results(time, map, user) VALUES (?, ?, ?)", (bestTime, map, user))
    except:
        cursor.execute("UPDATE results SET time = ? WHERE map = ? AND user = ?", (bestTime, map, user))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)