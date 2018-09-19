import os
import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)

# Tested
def get_cur_player_data(username, all_players_data):
    """
    Module checks if username has been used before. If Yes then returns the user info,
    if No adds the new new users info to the all_players_data list
    """
    username = username.lower()
    past_player = False
    
    for obj in all_players_data:
        if obj["name"] == username:
            past_player = True
            cur_player_data = obj
       
    if past_player == False:
        cur_player_data = {"name": username,"game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        all_players_data.append(cur_player_data)
    
    return cur_player_data, all_players_data
    
# little point in testing

def get_all_players_data():
    """
    Gets player all player data players.json
    """
    with open("data/players.json", "r") as json_players_data:
            all_players_data = json.load(json_players_data)
    return all_players_data

# little point in testing   
def dump_all_players_data (all_players_data): 
    """
    Dumps the player data back into players.json
    """
    with open("data/players.json", "w") as json_player_data:           
        json.dump(all_players_data, json_player_data)

def update_players_json(cur_player_data):
    """
    Updates players.json file with cur_player_data
    """
    all_players_data = get_all_players_data()
    print(all_players_data)
    print(cur_player_data)
    for obj in all_players_data:
        if obj["name"] == cur_player_data["name"]:
            obj["game_num"] = cur_player_data["game_num"]
            obj["cur_question"] = cur_player_data["cur_question"]
            obj["attempt"] = cur_player_data["attempt"]
            obj["cur_score"] = cur_player_data["cur_score"]
            obj["high_score"] = cur_player_data["high_score"]
            
    dump_all_players_data(all_players_data)
    
# little point in testing
def get_leader_data():
    """
    Gets player all player data players.json
    """
    with open("data/leaderboard.json", "r") as json_leader_data:
            leader_data = json.load(json_leader_data)
    return leader_data

# little point in testing   
def dump_leader_data(leader_data): 
    """
    Dumps the player data back into leaderboard.json
    """
    with open("data/leaderboard.json", "w") as json_leader_data:           
        json.dump(leader_data, json_leader_data)

def get_welcome_msg(cur_player_data):
        
    if cur_player_data["cur_question"] != 0:
        welcome_msg = ("Welcome back " + cur_player_data["name"]
            + ". Looks like you left us mid game. You are currently on question " 
            + str(cur_player_data["cur_question"]) + ".")
            
        cur_player_data["cur_question"] -= 1
        hide_start_btn = False
    elif cur_player_data["game_num"] != 1:
        welcome_msg = ("Welcome back " + cur_player_data["name"] 
            + ". You have played this game " 
            + str(cur_player_data["game_num"]) 
            + " times before.")
        hide_start_btn = False
    else:
        welcome_msg = "Welcome " + cur_player_data["name"] + ". This looks like your first game."
        hide_start_btn = False
        
    return welcome_msg, hide_start_btn, cur_player_data
 
            
# tested
def get_q_data(index):
    """
    Gets the tree name and image address for the current question
    """
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        
        max_score = (index)*10
        for obj in quiz_data:
            if obj["index"] == index:  
                tree_name = obj["tree_name"]
                tree_image = obj["tree_image"]
        
        return tree_name, tree_image, max_score

def prep_next_question(cur_player_data):
    
    cur_player_data["cur_question"] += 1
    cur_player_data["attempt"] = 1
    tree_name, tree_image, max_score = get_q_data(cur_player_data["cur_question"])
            
    return tree_name, tree_image, max_score, cur_player_data 
    
# tested   
def check_answer(index, answer):
    """
    Checks if the answer submited is correct. Returns True or False
    """
    answer = answer.lower()
    tree_name, tree_image, max_score = get_q_data(index)
    if answer == tree_name:
        return True, tree_name
    else:
        return False, tree_name

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
       
def reset_game(cur_player_data):
    """
    Resets the the user game data after final question, 
    Current question set to 1 once game begins
    """
    cur_player_data["cur_score"] = 0
    cur_player_data["attempt"] = 1
    cur_player_data["cur_question"] = 0
    cur_player_data["game_num"] += 1
    update_players_json(cur_player_data)

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
   
# tested 
def evaluate_result(cur_player_data, leader):
    """
    Updates high score and leaderboard where required based on current score.
    Returns appropriete message to be disaplayed on game over screen.
    """
    score = cur_player_data["cur_score"]
    # Scored 0   
    if score ==0:
        leader = leader
        result_msg = "You can do better than 0. You should try again, I'm sure you have learned from your mistakes."
    # First game, full marks
    elif cur_player_data["game_num"] == 1 and score == 100:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        result_msg = "Congradulations! You got top marks on your first game. Check out the leaderboard."
    # First game, scored between 0 and 100
    elif cur_player_data["game_num"] == 1 and score < 100:
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
    return render_template("index.html", welcome_msg="", 
                                         hide_start_btn = True)

@app.route('/check_name/', methods=['GET', 'POST'])
def check_name():
    """
    Accepts username entry, accesses/ creates the user info and 
    initiates quiz
    """
    global glob_all_players_data
    global glob_cur_player_data
    username = request.form["username"]
    if request.method == "POST":
        
        if username =="":
            welcome_msg = "Can not accept blank username. Please enter a valid username."
            hide_start_btn = True
        else:
            all_players_data = get_all_players_data()
            cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
            welcome_msg, hide_start_btn, cur_player_data = get_welcome_msg(cur_player_data)
            glob_cur_player_data = cur_player_data

        return render_template("index.html", welcome_msg=welcome_msg, 
                                             hide_start_btn = hide_start_btn)
        
        
@app.route('/next_q/', methods=['GET', 'POST'])
def load_question():
    global glob_cur_player_data
    cur_player_data = glob_cur_player_data
    tree_name, tree_image, max_score, cur_player_data = prep_next_question(cur_player_data)
    glob_cur_player_data = cur_player_data

    return render_template("quiz.html", tree_image=tree_image, 
                                    cur_score=cur_player_data["cur_score"], 
                                    attempt=cur_player_data["attempt"], 
                                    cur_question=cur_player_data["cur_question"], 
                                    max_score=max_score,
                                    message="What is the name of this tree?",
                                    feedback_msg = "Temp Feedback Msg",
                                    hide_next_btn=True)
    
@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    global glob_cur_player_data
    
    cur_player_data = glob_cur_player_data
    answer = request.form["answer"]
    if request.method == "POST":
        if answer == "":
            feedback_msg = "You can not submit a blank entry!"
            hide_next_btn = True
        else:    
            correct, tree_name = check_answer(cur_player_data["cur_question"], answer)
            if correct:
                cur_player_data = add_to_score(cur_player_data)
                feedback_msg = "Good job! This is a " + tree_name + " tree."
                hide_next_btn = False
            elif not correct and cur_player_data["attempt"] < 2:
                feedback_msg = answer.title() + " is not correct, but you still have a second try."
                hide_next_btn = True
                cur_player_data["attempt"] += 1
            else:
                feedback_msg = answer.title() + " is not correct. This is a " + tree_name
                hide_next_btn = False
        tree_name, tree_image, max_score = get_q_data(cur_player_data["cur_question"])
        glob_cur_player_data = cur_player_data
        update_players_json(cur_player_data)
        return render_template("quiz.html", tree_image=tree_image, 
                                            cur_score=cur_player_data["cur_score"], 
                                            attempt=cur_player_data["attempt"], 
                                            cur_question=cur_player_data["cur_question"], 
                                            max_score=max_score,
                                            message=feedback_msg,
                                            feedback_msg = feedback_msg,
                                            hide_next_btn=hide_next_btn)
                                            
@app.route('/finsh_game/', methods=['GET', 'POST'])                                            
def finsh_game():
    """
    Redirects to game over page
    """
    global glob_cur_player_data
    cur_player_data = glob_cur_player_data
    
    # Read in leaderboard
    leader = get_leader_data()
    # Compare final score to users past high scores and the leaderboard
    result_msg, cur_player_data, leader = evaluate_result(cur_player_data, leader)
    # Write to leaderboard
    dump_leader_data(leader)
    score_str=str(cur_player_data["cur_score"])
    # Reset game
    reset_game(cur_player_data)

    return render_template("game_over.html", score_str=score_str, 
                                             result_msg=result_msg, 
                                             leader=leader, 
                                             page_title="Game_Over")
    
@app.route('/leader', methods=['GET', 'POST'])
def leader(): 
    """
    Redirects to leader_board
    """
    with open("data/leaderboard.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
    return render_template("leader.html", leader=leader, 
                                          page_title="Leaderboard")

@app.route('/instructions/')
def instructions(): 
    return render_template("instructions.html", page_title="Instructions") 
                                          
   
# Main will only run wen run is exicuted from command line not if imported to nother program i.e. get_dictionary    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)