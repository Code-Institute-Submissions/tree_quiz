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
            cur_player_data = {"name": username,"game_num": 0, 
                "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
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
        
def add_to_score():
    """
    Increases the current score by 10 if correct on attempt 1
    Increases the current score by 5 if correct on attemp 2
    """
    if cur_player_data["attempt"] == 1:
       cur_player_data["cur_score"] += 10
    else:
       cur_player_data["cur_score"] += 5 
    return cur_player_data["cur_score"]
       
def prep_next_q(start, correct, message):
    """
    Prepares the first/ next question. Pulls in data from tree_lib.json
    based on information from players.json
    """
    if start == True:
        if cur_player_data["cur_question"] == 0:
            cur_player_data["cur_question"] = 1
    else:
        if not correct and cur_player_data["attempt"] == 1:
          cur_player_data["attempt"] = 2
          
        else:
          cur_player_data["cur_question"] += 1
          cur_player_data["attempt"] = 1
       
    cur_question = cur_player_data["cur_question"]
    max_score = (cur_player_data["cur_question"] - 1)*10
    tree_name = get_name(cur_question)
    tree_image = get_img(cur_question)
    cur_score=cur_player_data["cur_score"]
    attempt=cur_player_data["attempt"]
    dump_all_player_data ()
    return render_template("quiz.html", tree_image=tree_image, 
        tree_name=tree_name, message=message, cur_score=cur_score, 
        attempt=attempt, cur_question=cur_question, max_score=max_score)
       
def reset_game():
    """
    Resets the the user game data after final question, 
    Current question set to 1 once game begins
    """
    cur_player_data["cur_score"] = 0
    cur_player_data["attempt"] = 1
    cur_player_data["cur_question"] = 0
    cur_player_data["game_num"] += 1
    dump_all_player_data ()

"""    
def add_to_leader_board(name, score, game_num):
"""
"""
    The leader board will show the top 5 players. This function fills the the 
    top 5 slots and saves them in leader_board.json. 
    """
"""
    made_leader = False
    
    with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
        
    len_leader = len(leader)
    
    # Leader board empty
    if len_leader < 3:
        leader.append(name)
        leader.append(score)
        leader.append(game_num)
        made_leader = True
    # Leader board not full    
    elif len_leader <  15:
        # Score not greater than other scores, append to end
        if score < int(min(leader)):
            leader.append(name)
            leader.append(score)
            leader.append(game_num)
            made_leader = True
        # Score greater than score on board
        else:
            for n in range(1, len_leader, 3):
                if score > int(leader[n]):
                    leader.insert(n-1,game_num)
                    leader.insert(n-1, score)
                    leader.insert(n-1, name)
                    made_leader = True
                    break
    
    # Leader board full and score is knocking someone out of the board
    elif score > int(min(leader)):
        del leader[len_leader-3:len_leader]
        # Working from highest to lowest, what is the highest rank can be put in
        for n in range(1, len_leader-3, 3):
            if score > int(leader[n]):
                print(n)
                leader.insert(n-1,game_num)
                leader.insert(n-1, score)
                leader.insert(n-1, name)
                made_leader = True
                break
    
    with open("data/leader_board.json", "w") as json_leader_board:           
            json.dump(leader, json_leader_board)
            
    return made_leader, leader
    """
def add_to_leader_board(name, score, game_num, leader):
    """
    The leader board will show the top 5 players. This function fills the the 
    top 5 slots and saves them in leader_board.json. 
    """
    made_leader = False
    len_leader = len(leader)
    leader_scores=[]
    
    # Create a list of the scores on the leaderboard
    for n in range(1, len(leader),3):
        leader_scores.append(leader[n])

    # Leader board empty
    # Add user to leaderboard
    if len_leader < 3:
        leader.append(name)
        leader.append(score)
        leader.append(game_num)
        made_leader = True
    # Leaderboard not full    
    elif len_leader <  15:
        # Score not greater than other scores
        # Add user to end of leaderboard
        if score < int(min(leader_scores)):
            leader.append(name)
            leader.append(score)
            leader.append(game_num)
            made_leader = True
        # Score greater than score on leaderboard
        # Working from highest to lowest, insert player into highest rank
        else:
            for n in range(len_leader-2, 0, -3):
                if score >= int(leader[n]):
                    print(n)
                    leader.insert(n+2, game_num)
                    leader.insert(n+2, score)
                    leader.insert(n+2, name)
                    made_leader = True
                    break
            
    # Leaderboard full, but final score made it onto leaderboard
    # Working from highest to lowest, insert player into highest rank
    elif score >= min(leader_scores):
        del leader[0:3]
        len_leader=len(leader)
        for n in range(len_leader-2, 0, -3):
            if score >= int(leader[n]):
                
                leader.insert(n+2,game_num)
                leader.insert(n+2, score)
                leader.insert(n+2, name)
                made_leader = True
                break
    
    return made_leader, leader
    
def evaluate_result(final_score,user_info):
    
    # Read in leaderboard
    with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
    # Scored 0   
    if final_score ==0:
        leader = leader
        result_msg = "You can do better than 0. Try again. Takes a few goes to get them right."
    # First game, full marks
    elif user_info["game_num"] == 0 and final_score == 100:
        user_info["high_score"] = final_score
        made_leader, leader = add_to_leader_board(user_info["name"], final_score, user_info["game_num"], leader)
        result_msg = "Congradulations! You got top marks on your first game. You are on the leaderboard"
    # First game, scored between 0 and 100
    elif user_info["game_num"] == 0 and final_score < 100:
        user_info["high_score"] = final_score
        made_leader, leader = add_to_leader_board(user_info["name"], final_score, user_info["game_num"], leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = "Excelent! First game and you made it on the leaderboard."
        # Score did not make it onto leaderboard
        else:
            result_msg = "Good first try. Have another game and try to make it onto leaderboard."
    # Played before, personnel best
    elif final_score > user_info["high_score"]:
        user_info["high_score"] = final_score
        made_leader, leader = add_to_leader_board(user_info["name"], final_score, user_info["game_num"], leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = "Excelent! That is a personnel best and you made it to leaderboard"
        # Score did not make it onto leaderboard
        else:
            result_msg = "You are improving. Keep trying to get top marks."
    else:
        # Scored less than personnel high score
        leader = leader
        result_msg = "Good job, but you didn't beat your own top score of " + str(user_info["high_score"])
    
    with open("data/leader_board.json", "w") as json_leader_board:           
        json.dump(leader, json_leader_board)
    return result_msg, leader
    
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
        # Assign appropriete welcome message
        
        if cur_player_data["cur_question"] != 0:
            message = ("Welcome back " + username 
                + ". Looks like you left us mid game. Play on or click Home below to enter another user name")
        elif cur_player_data["game_num"] != 0:
            message = ("Welcome back " + username 
                + ". Looks like you've played this game before. Best of luck this time around.")
        else:
            message = "Hello " + username + " do you know the name of this tree?"
        return prep_next_q(True, True, message)
        
    else:    
        return render_template("index.html")   
        
        
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    """
    Submits the answer to the current question.Submits
    If correct moves onto next question
    If wrong allows second attempt before moving onto next question
    """
    cur_question = cur_player_data["cur_question"]
    answer = request.form["answer"]
    if request.method == "POST":
        # If correct there are more questions
        if cur_question < 10:
            # If correct answer move on to next question
            if check_answer(cur_question, answer) == True:
                # Increase current score approprietly 
                add_to_score()
                # Set up the next question     
                message = ("Good job! " + answer.title() 
                    + " was the correct answer. How about this one?")    
                return prep_next_q(False, True, message)
                
            # If wrong on first attempt, give second attempt
            elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! " + answer.title()  + " was not correct. How about another guess?"
                return prep_next_q(False, False, message)
            # If wrong on second attempt, move onto next question
            else:
                tree_name = get_name(cur_question)
                message = (answer.title()  + " was not correct. The correct answer was " 
                    + tree_name + ". Might have better look with this one?")
                return prep_next_q(False, False, message)
        
        # For the final question
        else:
           # If correct reset game, show Game Over page with appropriete message
           if check_answer(cur_question, answer) == True:
               # Increase current score approprietly 
               add_to_score()
               final_score = cur_player_data["cur_score"]
               final_score_str = str(cur_player_data["cur_score"])
               message = ("Good job! " + answer.title() 
                + " was the correct answer. That was the final question.")
               result_msg, leader = evaluate_result(final_score, cur_player_data)
               
               # reset game
               reset_game()
               with open("data/leader_board.json", "r") as json_leader_board:
                    leader = json.load(json_leader_board)
               return render_template("game_over.html", message=message, final_score_str=final_score_str, result_msg=result_msg, leader=leader, page_title="Game_Over")
               
           # If wrong on first attempt, give second attempt
           elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! " + answer.title()  + " was not correct. How about another guess?"
                return prep_next_q(False, False, message)
           # If wrong on second attempt, reset game, show Game Over page with appropriete message 
           else:
                final_score = cur_player_data["cur_score"]
                final_score_str = str(cur_player_data["cur_score"])
                tree_name = get_name(cur_question)
                message = (answer.title()  + " was not correct. The correct answer was " 
                    + tree_name + ". That was the final qustion.")
                
                result_msg, leader = evaluate_result(final_score, cur_player_data)
             
                # reset game
                reset_game()
                with open("data/leader_board.json", "r") as json_leader_board:
                    leader = json.load(json_leader_board)
                return render_template("game_over.html", message=message,  final_score_str=final_score_str, result_msg=result_msg, leader=leader, page_title="Game_Over")

    
@app.route('/leader', methods=['GET', 'POST'])
def leader(): 
    """
    Redirects to leader_board
    """
    with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
    return render_template("leader.html", leader=leader, page_title="Leaderboard")
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)