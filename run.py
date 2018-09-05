import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)
user_info = {"name": "","game_num": 0}
data = []


@app.route('/', methods=["GET", "POST"])
def index():
    """Home page, accepts username, writes to players.json"""
    # should make test for this
    if request.method == "POST":
        username = request.form["username"].lower()
        
        
        with open("data/players.json", "r") as json_data:
            data = json.load(json_data)
            past_player = False
            
            for obj in data:
                if obj["name"] == username:
                    obj["game_num"] +=1
                    past_player = True
            if past_player == False:
                user_info = {"name": username,"game_num": 0}
                data.append(user_info)
        
        with open("data/players.json", "w") as json_data:           
            json.dump(data, json_data)
                        
            
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)