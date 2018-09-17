import os
import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)

# Tested
def get_cur_player_data(username, all_players_data):
    """
    Module checks if username has been used before. If Yes then returns the user info,
    if No adds the new new users info to the all_player_data list
    """
    username = username.lower()
    past_player = False
    
    for obj in all_players_data:
        if obj["name"] == username:
            past_player = True
            cur_player_data = obj
            
    if past_player == False:
        cur_player_data = {"name": username,"game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        all_players_data.append(cur_player_data)
    
    return cur_player_data, all_players_data
    
# little point in testing
def get_all_player_data():
    """
    Gets player all player data players.json
    """
    with open("data/players.json", "r") as json_player_data:
            all_players_data = json.load(json_player_data)
    return all_player_data

# little point in testing   
def dump_all_player_data (all_players_data): 
    """
    Dumps the player data back into players.json
    """
    with open("data/players.json", "w") as json_player_data:           
        json.dump(all_players_data, json_player_data)
        
# little point in testing
def get_leader_data():
    """
    Gets player all player data players.json
    """
    with open("data/leaderboard.json", "r") as json_leader_data:
            leader_data = json.load(json_leader_data)
    return leader_data

# little point in testing   
def dump_leader_data (leader): 
    """
    Dumps the player data back into leaderboard.json
    """
    with open("data/leaderboard.json", "w") as json_leader_data:           
        json.dump(leader_data, json_leader_data)
        
# tested
def get_q_data(index):
    """
    Gets the tree name and image address for the current question
    """
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        

        for obj in quiz_data:
            if obj["index"] == index:  
                
                tree_name = obj["tree_name"]
                tree_image = obj["tree_image"]
                
        return tree_name, tree_image

# tested   
def check_answer(index, answer):
    """
    Checks if the answer submited is correct. Returns True or False
    """
    answer = answer.lower()
    tree_name, tree_image = get_q_data(index)
    if answer == tree_name:
        return True
    else:
        return False

# tested        
def add_to_score(cur_player_data):
    """
    Increases the current score by 10 if correct on attempt 1
    Increases the current score by 5 if correct on attemp 2
    """
    if cur_player_data["attempt"] == 1:
       cur_player_data["cur_score"] += 10
    else:
       cur_player_data["cur_score"] += 5 
    return cur_player_data

# HOW to test if return is rendering a website    
def prep_next_q(start, correct, message, cur_player_data):
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
    tree_name, tree_image = get_q_data(cur_question)
    cur_score=cur_player_data["cur_score"]
    attempt=cur_player_data["attempt"]
    dump_all_player_data ()
    return render_template("quiz.html", tree_image=tree_image, 
        tree_name=tree_name, message=message, cur_score=cur_score, 
        attempt=attempt, cur_question=cur_question, max_score=max_score)
       
def reset_game(cur_player_data):
    """
    Resets the the user game data after final question, 
    Current question set to 1 once game begins
    """
    cur_player_data["cur_score"] = 0
    cur_player_data["attempt"] = 1
    cur_player_data["cur_question"] = 0
    cur_player_data["game_num"] += 1
    glob_cur_player_data = cur_player_data
    dump_all_player_data ()

# tested
def add_to_leaderboard(cur_player_data, leader):
    """
    The leader board will show the top 5 players. This function fills the the 
    top 5 slots and saves them in leader_board.json. 
    """
    made_leader = False
    len_leader = len(leader)
    leader_scores=[]
    
    name = cur_player_data["name"]
    score = cur_player_data["high_score"]
    game_num = cur_player_data["game_num"]
    
    # Create a list of the scores on the leaderboard
    for n in range(1, len(leader),3):
        leader_scores.append(leader[n])

    # Leader board empty
    # Add user to leaderboard
    if len_leader < 3:
        made_leader = True
        leader.append(name)
        leader.append(score)
        leader.append(game_num)
        
    # Leaderboard not full    
    elif len_leader <  15:
        made_leader = True
        # Score less than scores on leaderboard
        # Add user to end of leaderboard
        if score < int(min(leader_scores)):
            leader.append(name)
            leader.append(score)
            leader.append(game_num)
            
        # Score greater than scores on leaderboard
        # Working from highest to lowest, insert player into highest rank
        else:
            for n in range(1, len_leader-1, 3):
                if score >= int(leader[n]):
                    
                    leader.insert(n-1, game_num)
                    leader.insert(n-1, score)
                    leader.insert(n-1, name)

                    break
            
    # Leaderboard full, but final score made it onto leaderboard
    # Working from highest to lowest, insert player into highest rank
    elif score >= min(leader_scores):
        made_leader = True
        del leader[len_leader-3:len_leader]
        len_leader=len(leader)
        # Score is equal to the lowest score on leaderboard
        if score == min(leader_scores):
                leader.append(name)
                leader.append(score)
                leader.append(game_num)
        # Score between scores on leaderboard
        else:
            for n in range(1, len_leader, 3):
                if score >= int(leader[n]):
                    
                    leader.insert(n-1, game_num)
                    leader.insert(n-1, score)
                    leader.insert(n-1, name)
    
                    break

    return made_leader, leader
    
def evaluate_result(cur_player_data, leader):
    score = cur_player_data["cur_score"]
    # Scored 0   
    if score ==0:
        leader = leader
        result_msg = "You can do better than 0. You should try again, I'm sure you have learned from your mistakes."
    # First game, full marks
    elif cur_player_data["game_num"] == 0 and score == 100:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        result_msg = "Congradulations! You got top marks on your first game. Check out the leaderboard."
    # First game, scored between 0 and 100
    elif cur_player_data["game_num"] == 0 and score < 100:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = "Excelent! First game and you made it on the leaderboard."
        # Score did not make it onto leaderboard
        else:
            result_msg = "Good first try. Have another game and try to make it onto leaderboard."
    # Played before, personnel best
    elif score > cur_player_data["high_score"]:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = "Excelent! You made it onto the leaderboard with this new personnel best."
        # Score did not make it onto leaderboard
        else:
            result_msg = "You are improving. Keep trying to get top marks."
    else:
        # Scored less than personnel high score
        leader = leader
        result_msg = "Good job, but you didn't beat your own top score of " + str(cur_player_data["high_score"])
    
    return result_msg, cur_player_data, leader
    
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
    global glob_all_players_data
    global glob_cur_player_data
    
    username = request.form["username"]
    if request.method == "POST" and username != "":
        
        # If new user creates info space
        # If returning user access info
        all_players_data = get_all_player_data()

        cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
        glob_all_player_data = all_players_data
        glob_cur_player_data = cur_player_data
        
        dump_all_player_data(all_players_data)
        
        # Assign appropriete welcome message
        
        if cur_player_data["cur_question"] != 0:
            message = ("Welcome back " + username 
                + ". Looks like you left us mid game. Play on or click Home below to enter another user name")
        elif cur_player_data["game_num"] != 0:
            message = ("Welcome back " + username 
                + ". Looks like you've played this game before. Best of luck this time around.")
        else:
            message = "Hello " + username + " do you know the name of this tree?"
        return prep_next_q(True, True, message, glob_cur_player_data)
        
    else:    
        return render_template("index.html")   
        
        
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    """
    Submits the answer to the current question.Submits
    If correct moves onto next question
    If wrong allows second attempt before moving onto next question
    """
    cur_player_data = glob_cur_player_data
    cur_question = cur_player_data["cur_question"]
    answer = request.form["answer"]
    if request.method == "POST":
        # If correct there are more questions
        if cur_question < 10:
            # If correct answer move on to next question
            if check_answer(cur_question, answer) == True:
                # Increase current score approprietly 
                cur_player_data = add_to_score(cur_player_data)
                # Set up the next question     
                message = ("Good job! " + answer.title() 
                    + " was the correct answer. How about this one?")    
                return prep_next_q(False, True, message, cur_player_data)
                
            # If wrong on first attempt, give second attempt
            elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! " + answer.title()  + " was not correct. How about another guess?"
                return prep_next_q(False, False, message, cur_player_data)
            # If wrong on second attempt, move onto next question
            else:
                tree_name, tree_image = get_q_data(cur_question)
                message = (answer.title()  + " was not correct. The correct answer was " 
                    + tree_name + ". Might have better look with this one?")
                return prep_next_q(False, False, message, cur_player_data)
        
        # For the final question
        else:
           # If correct reset game, show Game Over page with appropriete message
           if check_answer(cur_question, answer) == True:
               # Increase current score approprietly 
               cur_player_data = add_to_score(cur_player_data)
               score = cur_player_data["cur_score"]
               score_str = str(cur_player_data["cur_score"])
               message = ("Good job! " + answer.title() 
                + " was the correct answer. That was the final question.")
               
               # Read in leaderboard

               leader = get_leader_data()
                   
               # Compare final score to users past high scores and the leaderboard
               result_msg, cur_player_data, leader = evaluate_result(cur_player_data, leader)
               
               # Write to leaderboard
               dump_leader_data(leader)
               
               # reset game
               reset_game(cur_player_data)

               return render_template("game_over.html", message=message, score_str=score_str, result_msg=result_msg, leader=leader, page_title="Game_Over")
               
           # If wrong on first attempt, give second attempt
           elif check_answer(cur_question, answer) == False and cur_player_data["attempt"] == 1:
                message = "Ooops! " + answer.title()  + " was not correct. How about another guess?"
                return prep_next_q(False, False, message, cur_player_data)
           # If wrong on second attempt, reset game, show Game Over page with appropriete message 
           else:
                score = cur_player_data["cur_score"]
                score_str = str(cur_player_data["cur_score"])
                tree_name, tree_image = get_q_data(cur_question)
                message = (answer.title()  + " was not correct. The correct answer was " 
                    + tree_name + ". That was the final qustion.")
                
                # Read in leaderboard
                leader = get_leader_data()
                
                # Compare final score to users past high scores and the leaderboard    
                result_msg, cur_player_data, leader = evaluate_result(cur_player_data, leader)
                
                # Write to leaderboard
                dump_leader_data()
             
                # reset game
                reset_game(cur_player_data)
                
                return render_template("game_over.html", message=message,  score_str=score_str, result_msg=result_msg, leader=leader, page_title="Game_Over")

    
@app.route('/leader', methods=['GET', 'POST'])
def leader(): 
    """
    Redirects to leader_board
    """
    with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
    return render_template("leader.html", leader=leader, page_title="Leaderboard")
    
# Main will only run wen boogle is exicuted from command line not if imported to nother program i.e. get_dictionary    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)