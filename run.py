import os
import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)

def access_user_data(username):
    """
    Module takes in username as input, checks players.json database to see
    the username has been used before. Either increments the number of games
    played or adds a new username to the players database.
    Requires player.json file to contain list, either empty or occupied.
    """
    global all_players_data
    global cur_player_data
    
    username = username.lower()
    past_player = False
    
    with open("data/players.json", "r") as json_player_data:
        all_players_data = json.load(json_player_data)
        

        for obj in all_players_data:
            if obj["name"] == username:
                past_player = True
                cur_player_data = obj
                
        if past_player == False:
            cur_player_data = {"name": username,"game_num": 0, "cur_question": 1, "attempt": 1, "cur_score": 0, "high_score": 0}
            all_players_data.append(cur_player_data)
    
    dump_all_player_data ()
    
def dump_all_player_data (): 
    """
    Dumps the player data back into players.json
    """
    with open("data/players.json", "w") as json_player_data:           
        json.dump(all_players_data, json_player_data)
        
def get_img(index):
    """
    Get the image address for the current question
    """
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        

        for obj in quiz_data:
            if obj["index"] == index:  

                tree_image = obj["tree_image"]

    return tree_image

def get_name(index):
    """
    Get the answer for the current question
    """
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        

        for obj in quiz_data:
            if obj["index"] == index:  

                tree_name = obj["tree_name"]

    return tree_name
    
def check_answer(index, answer):
    """
    Checks if the answer submited is correct
    """
    answer = answer.lower()
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        

        for obj in quiz_data:
            if obj["index"] == index and obj["tree_name"] == answer:
                return True
            elif obj["index"] == index and obj["tree_name"] != answer:
                return False

def personal_best(final_score):
    """
    Checks if the final score of the game is greater than the users
    current high score, if yes replace
    """
    if final_score > cur_player_data["high_score"]:
        cur_player_data["high_score"] = final_score
        return True
    else:
        return False
        
@app.route('/')
def index():
    """
    Home page
    """
    # should make test for this
    return render_template("index.html")


@app.route('/start/', methods=['GET', 'POST'])
def start():
    """
    Accepts username entry, accesses/ creates the user info and 
    initiates quiz
    """
    username = request.form["username"]
    if request.method == "POST" and username != "":
        
        # If new user creates info space
        # If returning user access info
        access_user_data(username)
        cur_question = cur_player_data["cur_question"]
        
        # Gather the starting quiz info
        tree_name = get_name(cur_question)
        tree_image = get_img(cur_question)

        message = "Hello " + username + " do you know the name of this tree?"
        return render_template("quiz.html", tree_image=tree_image, tree_name=tree_name, 
            message=message, cur_score=cur_player_data["cur_score"],  attempt=cur_player_data["attempt"], cur_question=cur_player_data["cur_question"], max_score=0)
        
        
    else:    
        return render_template("index.html")   
        
        
@app.route('/submit_answer/', methods=['GET', 'POST'])
def submit():
    """
    Submits the answer to the current question.Submits
    If correct moves onto next question
    If wrong allows second attempt before moving onto next question
    """
    cur_question = cur_player_data["cur_question"]
    
    if request.method == "POST":
        answer = request.form["answer"]
        
        # If correct there are more questions
        if cur_question < 10:
            # If correct answer move on to next question
            if check_answer(cur_question, answer) == True:
                
                # Add to the running score, half points for second attempt
                if cur_player_data["attempt"] == 1:
                    cur_player_data["cur_score"] += 10
                else:
                    cur_player_data["cur_score"] += 5
                
                # Set up the next question     
                message = "Good job! You were correct the last tree was a " + answer + ". How about this one?"    
                cur_player_data["cur_question"] += 1
                cur_player_data["attempt"] = 1
                cur_question = cur_player_data["cur_question"]
                tree_name = get_name(cur_question)
                tree_image = get_img(cur_question)
                max_score = (cur_player_data["cur_question"] - 1)*10
                dump_all_player_data ()
                return render_template("quiz.html", tree_image=tree_image, tree_name=tree_name, 
                    message=message, cur_score=cur_player_data["cur_score"], attempt=cur_player_data["attempt"], cur_question=cur_player_data["cur_question"], max_score=max_score)
            
            # If wrong on first attempt, give second attempt
            elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! Sorry that is not a " + answer + ". How about another guess?"
                cur_player_data["attempt"] = 2
                cur_question = cur_player_data["cur_question"]
                tree_name = get_name(cur_question)
                tree_image = get_img(cur_question)
                max_score = (cur_player_data["cur_question"] - 1)*10
                dump_all_player_data ()
                return render_template("quiz.html", tree_image=tree_image, tree_name=tree_name, 
                    message=message, cur_score=cur_player_data["cur_score"], attempt=cur_player_data["attempt"], cur_question=cur_player_data["cur_question"], max_score=max_score)
            
            # If wrong on second attempt, move onto next question
            else:
                message = "Nope it was not a " + answer + " either. Might have better look with this one?"
                cur_player_data["attempt"] = 1
                cur_player_data["cur_question"] += 1
                cur_question = cur_player_data["cur_question"]
                tree_name = get_name(cur_question)
                tree_image = get_img(cur_question)
                max_score = (cur_player_data["cur_question"] - 1)*10
                dump_all_player_data ()
                return render_template("quiz.html", tree_image=tree_image, tree_name=tree_name, 
                    message=message, cur_score=cur_player_data["cur_score"], attempt=cur_player_data["attempt"], cur_question=cur_player_data["cur_question"], max_score=max_score)
        
        # For the final question
        else:
           # If correct reset game, show Game Over page with appropriete message
           if check_answer(cur_question, answer) == True:
               
               # Add to the running score, half points for second attempt
               if cur_player_data["attempt"] == 1:
                   cur_player_data["cur_score"] += 10
               else:
                   cur_player_data["cur_score"] += 5
                
               # Set up the next question  
               
               final_score = str(cur_player_data["cur_score"])
               personal_best(final_score)
               end_message = "Good job! You were correct the last tree was a " + answer + ". That was the final question. You got " + final_score + "/100."
               # reset game
               cur_player_data["cur_score"] = 0
               cur_player_data["attempt"] = 1
               cur_player_data["cur_question"] = 1
               cur_player_data["game_num"] += 1
               dump_all_player_data ()
               return render_template("game_over.html", end_message=end_message)
               
           # If wrong on first attempt, give second attempt
           elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! Sorry that is not a " + answer + ". How about another guess?"
                cur_player_data["attempt"] = 2
                cur_question = cur_player_data["cur_question"]
                tree_name = get_name(cur_question)
                tree_image = get_img(cur_question)
                max_score = (cur_player_data["cur_question"] - 1)*10
                dump_all_player_data ()
                return render_template("quiz.html", tree_image=tree_image, tree_name=tree_name, 
                    message=message, cur_score=cur_player_data["cur_score"], attempt=cur_player_data["attempt"], cur_question=cur_player_data["cur_question"], max_score=max_score)
                
           # If wrong on second attempt, reset game, show Game Over page with appropriete message 
           else:
                final_score = str(cur_player_data["cur_score"])
                personal_best(final_score)
                end_message = "Nope it was a " + answer + " either. The game is over the your score was " + final_score + "/100."
                # reset game
                cur_player_data["cur_score"] = 0
                cur_player_data["attempt"] = 1
                cur_player_data["cur_question"] = 1

                
                dump_all_player_data ()
                return render_template("game_over.html", end_message=end_message)
            

@app.route('/home/', methods=['GET', 'POST'])
def go_home(): 
    """
    Redirects to home page
    """
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)