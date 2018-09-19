import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# not tested
def read_json_data(json_file):
    """
    Read data from json file
    """
    with open(json_file, "r") as json_data:
            data = json.load(json_data)
    return data
# not tested    
def write_json_data(data, json_file):
    """
    Write data to json file
    """
    with open(json_file, "w") as json_data:           
        json.dump(data, json_data)
# not tested        
def update_players_json(cur_player_data):
    """
    Updates players.json file with cur_player_data
    """
    all_players_data = read_json_data("data/players.json")
    for obj in all_players_data:
        if obj["name"] == cur_player_data["name"]:
            obj["game_num"] = cur_player_data["game_num"]
            obj["cur_question"] = cur_player_data["cur_question"]
            obj["attempt"] = cur_player_data["attempt"]
            obj["cur_score"] = cur_player_data["cur_score"]
            obj["high_score"] = cur_player_data["high_score"]
            
    write_json_data(all_players_data,"data/players.json")

def get_cur_player_data(username, all_players_data):
    """
    Module checks if a username is in the player database, 
    returns the users info or else creates user info for the new user.
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
    
def get_welcome_msg(cur_player_data):
    """
    Module returns the appropriete welcome message based on he users playing history.
    """    
    if cur_player_data["cur_question"] != 0:
        welcome_msg = ("Welcome back " + cur_player_data["name"]
            + ". Looks like you left us mid game. You are currently on question " 
            + str(cur_player_data["cur_question"]) + ".")
        # Reduce cur_question by 1, load question automaticaly increases by one later   
        cur_player_data["cur_question"] -= 1
    elif cur_player_data["game_num"] != 1:
        welcome_msg = ("Welcome back " + cur_player_data["name"] 
            + ". You have played this game " 
            + str(cur_player_data["game_num"]-1) 
            + " times before.")
    else:
        welcome_msg = "Welcome " + cur_player_data["name"] + ". This looks like your first game."
        
    return welcome_msg, cur_player_data
 
def get_q_data(index):
    """
    Module returns the tree name, url of tree image
    and max possible score for a given question number.
    """
    with open("data/tree_lib.json", "r") as json_quiz_data:
        quiz_data = json.load(json_quiz_data)
        
        max_score = index*10
        for obj in quiz_data:
            if obj["index"] == index:  
                tree_name = obj["tree_name"]
                tree_image = obj["tree_image"]
        
        return tree_name, tree_image, max_score

def add_to_score(cur_player_data):
    """
    Module increments the users score by 10
    if user answers question correctly on first attemp, or 
    by 5 if user answers correctly on second attempt
    """
    if cur_player_data["attempt"] == 1:
       cur_player_data["cur_score"] += 10
    else:
       cur_player_data["cur_score"] += 5 
    return cur_player_data

def process_answer(answer, tree_name, cur_player_data):
    """
    Module checks if the users entered answer is correct,
    and returns appropriete feedback message and whether to allow access to 
    next question button.
    """
    if answer == tree_name:
        cur_player_data = add_to_score(cur_player_data)
        feedback_msg = tree_name.title() + " is the correct answer!"
        hide_next_btn = False
    elif answer != tree_name and cur_player_data["attempt"] < 2:
        feedback_msg = answer.title() + " is not correct, but you still have a second try."
        hide_next_btn = True
        cur_player_data["attempt"] += 1
    else:
        feedback_msg = "Wrong again! " + tree_name.title() +" is the correct answer."
        hide_next_btn = False

    return feedback_msg, hide_next_btn, cur_player_data
        
def add_to_leaderboard(cur_player_data, leader):
    """
    Modules checks if the users current score is a personnel best 
    and if that personnel best makes it onto a 5 person leaderboard.
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
    """
    Module compares the users final result against there past scores
    and the leaderboard, returns appropriete message.
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
                                         hide_start_btn = True,
                                         username="",
                                         title="Sign In")

@app.route('/check_username', methods=['GET', 'POST'])
def check_username():
    """
    Module accepts POST of username from index.html and return index.html 
    displaying appropriete welcome message and the next question button when
    required.
    """

    username = request.form["username"]
    if request.method == "POST":
        
        all_players_data = read_json_data("data/players.json")
        cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
        welcome_msg, cur_player_data = get_welcome_msg(cur_player_data)
        update_players_json(cur_player_data)
        hide_start_btn = False

        return render_template("index.html", welcome_msg=welcome_msg, 
                                             hide_start_btn=hide_start_btn, 
                                             username=username,
                                             title="Welcome")
        
@app.route('/question/<username>', methods=['GET', 'POST'])
def question(username):
    """
    Module returns quiz.html with the next question in the quiz, based on
    cur_player_data.
    """

    all_players_data = read_json_data("data/players.json")
    cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
    cur_player_data["cur_question"] += 1
    cur_player_data["attempt"] = 1
    tree_name, tree_image, max_score = get_q_data(cur_player_data["cur_question"])
    update_players_json(cur_player_data)
    title = "Question " + str(cur_player_data["cur_question"])
    return render_template("quiz.html", tree_image=tree_image, 
                                    cur_score=cur_player_data["cur_score"], 
                                    attempt=cur_player_data["attempt"], 
                                    cur_question=cur_player_data["cur_question"], 
                                    max_score=max_score,
                                    message="What is the name of this tree?",
                                    feedback_msg = "Temp Feedback Msg",
                                    hide_next_btn=True,
                                    username=username,
                                    title=title)
    
@app.route('/submit/<username>', methods=['GET', 'POST'])
def submit(username):
    """
    Module process the user inputed answer, checks if its correct, and 
    displays appropriete feedback message and shows the next question button when
    required.
    """    
    all_players_data = read_json_data("data/players.json")
    cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
    answer = request.form["answer"]
    answer = answer.lower()
    if request.method == "POST":
        tree_name, tree_image, max_score = get_q_data(cur_player_data["cur_question"])
        feedback_msg, hide_next_btn, cur_player_data = process_answer(answer, tree_name, cur_player_data)
        update_players_json(cur_player_data)
        title = "Q." + str(cur_player_data["cur_question"])
        return render_template("quiz.html", tree_image=tree_image, 
                                            cur_score=cur_player_data["cur_score"], 
                                            attempt=cur_player_data["attempt"], 
                                            cur_question=cur_player_data["cur_question"], 
                                            max_score=max_score,
                                            message=feedback_msg,
                                            feedback_msg = feedback_msg,
                                            hide_next_btn=hide_next_btn,
                                            username=username,
                                            title=title)
                                            
@app.route('/game_over/<username>', methods=['GET', 'POST'])                                            
def game_over(username):
    """
    Module renders game_over.html with updated leaderboard and 
    appropriete final message.
    """  
    all_players_data = read_json_data("data/players.json")
    cur_player_data, all_players_data = get_cur_player_data(username, all_players_data)
    # Read in leaderboard
    leader = read_json_data("data/leaderboard.json")
    # Compare final score to users past high scores and the leaderboard
    result_msg, cur_player_data, leader = evaluate_result(cur_player_data, leader)
    # Write to leaderboard
    write_json_data(leader, "data/leaderboard.json")
    score_str=str(cur_player_data["cur_score"])
    # Reset game
    cur_player_data["cur_score"] = 0
    cur_player_data["attempt"] = 1
    cur_player_data["cur_question"] = 0
    cur_player_data["game_num"] += 1
    # Update players.json
    update_players_json(cur_player_data)
    return render_template("game_over.html", score_str=score_str, 
                                             result_msg=result_msg, 
                                             leader=leader, 
                                             username=username,
                                             title="Game Over",)
    
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard(): 
    """
    Module returns leaderboard.html.
    """
    with open("data/leaderboard.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)
    return render_template("leaderboard.html", leader=leader, 
                                          title="Leaderboard")

@app.route('/instructions/')
def instructions(): 
    """
    Module returns instructions.html.
    """    
    return render_template("instructions.html", title="Instructions") 
                                          
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)