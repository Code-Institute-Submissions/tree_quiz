import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def read_json_data(json_file):
    """
    Read data from json file
    """
    with open(json_file, "r") as json_data:
            data = json.load(json_data)
    return data


def write_json_data(data, json_file):
    """
    Write data to json file
    """
    with open(json_file, "w") as json_data:
        json.dump(data, json_data)


def update_all_players_data(cur_player_data, all_players_data):
    """
    Updates all_players_data with cur_player_data
    """
    for obj in all_players_data:
        if obj["name"] == cur_player_data["name"]:
            index = all_players_data.index(obj)
            all_players_data[index] = cur_player_data
            break
    return all_players_data


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

    if not past_player:
        cur_player_data = {"name": username, "game_num": 1,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        all_players_data.append(cur_player_data)

    return cur_player_data, all_players_data


def get_welcome_msg(cur_player_data):
    """
    Module returns the welcome message based on he users playing history.
    """
    if cur_player_data["cur_question"] > 1:
        welcome_msg = ("Welcome back {}. Looks like you left us mid game." +
                       " You are currently on question {}.") \
                       .format(cur_player_data["name"],
                               str(cur_player_data["cur_question"]))
    elif cur_player_data["game_num"] != 1:
        welcome_msg = ("Welcome back {}." +
                       " You have played this game {} times before.") \
                       .format(cur_player_data["name"],
                               str(cur_player_data["game_num"] - 1))
    else:
        welcome_msg = "Welcome {}. This looks like your first game." \
                      .format(cur_player_data["name"])

    return welcome_msg, cur_player_data


def get_q_data(cur_question):
    """
    Module returns the tree name, url of tree image
    and max possible score for a given question number.
    """
    quiz_data = read_json_data("data/tree_lib.json")
    max_score = cur_question*10
    for obj in quiz_data:
        if obj["question"] == cur_question:
            tree_name = obj["tree_name"]
            tree_image = obj["tree_image"]

    return tree_name, tree_image, max_score


def add_to_score(cur_player_data):
    """
    Module increments the users score by 10
    if user answers question correctly on first attempt, or
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
    and returns feedback message and whether to allow access to
    next question button.
    """
    if answer == tree_name:
        cur_player_data = add_to_score(cur_player_data)
        cur_player_data["cur_question"] += 1
        feedback_msg = "{} is the correct answer!" \
                       .format(tree_name.title())
        hide_next_btn = False
        answer_state = 1
    elif answer != tree_name and cur_player_data["attempt"] == 1:
        cur_player_data["attempt"] = 2
        feedback_msg = "{} is not correct, but you still have a second try." \
                       .format(answer.title())
        hide_next_btn = True
        answer_state = 2
    else:
        cur_player_data["cur_question"] += 1
        feedback_msg = "Wrong again! {} is the correct answer." \
                       .format(tree_name.title())
        hide_next_btn = False
        answer_state = 2

    return feedback_msg, hide_next_btn, cur_player_data, answer_state


def add_to_leaderboard(cur_player_data, leader):
    """
    Modules checks if the users current score is a personnel best
    and if that personnel best makes it onto a 5 person leaderboard.
    """
    made_leader = False
    len_leader = len(leader)
    leader_scores = []

    name = cur_player_data["name"]
    score = cur_player_data["high_score"]
    game_num = cur_player_data["game_num"]

    # Create a list of the scores on the leaderboard
    for n in range(1, len(leader), 3):
        leader_scores.append(leader[n])

    # Leader board empty
    # Add user to leaderboard
    if len_leader < 3:
        made_leader = True
        leader.append(name)
        leader.append(score)
        leader.append(game_num)

    # Leaderboard not full
    elif len_leader < 15:
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
        len_leader = len(leader)
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
    Module compares the user's final result against their past scores
    and the leaderboard, returns appropriate message.
    """
    score = cur_player_data["cur_score"]
    # Scored 0
    if score == 0:
        leader = leader
        result_msg = ("You can do better than 0. You should try again," +
                      " I'm sure you have learned from your mistakes.")
    # First game, full marks
    elif cur_player_data["game_num"] == 1 and score == 100:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        result_msg = ("Congratulations!" +
                      " You got top marks on your first game." +
                      " Check out the leaderboard.")
    # First game, scored between 0 and 100
    elif cur_player_data["game_num"] == 1 and score < 100:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = ("Excellent!" +
                          " First game and you made it on the leaderboard.")
        # Score did not make it onto leaderboard
        else:
            result_msg = ("Good first try." +
                          " Have another game and try to" +
                          " make it onto leaderboard.")
    # Played before, personnel best
    elif score > cur_player_data["high_score"]:
        cur_player_data["high_score"] = score
        made_leader, leader = add_to_leaderboard(cur_player_data, leader)
        # Score made it onto leaderboard
        if made_leader:
            result_msg = ("Excellent!" +
                          " You made it onto the leaderboard" +
                          " with this new personal best.")
        # Score did not make it onto leaderboard
        else:
            result_msg = "You are improving. Keep trying to get top marks."
    else:
        # Scored less than personnel high score
        leader = leader
        result_msg = "Good job, but you didn't beat your own top score of {}" \
                     .format(str(cur_player_data["high_score"]))

    return result_msg, cur_player_data, leader


@app.route('/')
def index():
    """
    Home page
    """
    return render_template("index.html",
                           welcome_msg="",
                           hide_start_btn=True,
                           username="",
                           title="Sign In")


@app.route('/check_username', methods=['GET', 'POST'])
def check_username():
    """
    Module accepts POST of username from index.html and return index.html
    displaying appropriate welcome message and the next question button when
    required.
    """

    if request.method == "POST":
        username = request.form["username"]
        all_players_data = read_json_data("data/players.json")
        cur_player_data, \
            all_players_data = get_cur_player_data(username, all_players_data)
        write_json_data(all_players_data, "data/players.json")
        welcome_msg, cur_player_data = get_welcome_msg(cur_player_data)

        return render_template("index.html",
                               welcome_msg=welcome_msg,
                               hide_start_btn=False,
                               username=username,
                               title="Welcome")


@app.route('/question/<username>', methods=['GET', 'POST'])
def question(username):
    """
    Module returns either the next question or answer feedback
    displayed on quiz.html if the current question is less
    than 10 or game_over.html current question is 10.
    """
    all_players_data = read_json_data("data/players.json")
    cur_player_data, \
        all_players_data = get_cur_player_data(username, all_players_data)
    title = "Question " + str(cur_player_data["cur_question"])

    # For submitting answer
    if request.method == "POST":
        answer = request.form["answer"].lower()
        tree_name, tree_image, \
            max_score = get_q_data(cur_player_data["cur_question"])
        cur_question = cur_player_data["cur_question"]
        # Process_answer() returns cur_player_data for the next question
        message, hide_next_btn, \
            cur_player_data, answer_state = process_answer(answer,
                                                           tree_name,
                                                           cur_player_data)
        # Update players.json
        all_players_data = read_json_data("data/players.json")
        all_players_data = update_all_players_data(cur_player_data,
                                                   all_players_data)
        write_json_data(all_players_data, "data/players.json")

        return render_template("quiz.html",
                               tree_image=tree_image,
                               cur_score=cur_player_data["cur_score"],
                               attempt=cur_player_data["attempt"],
                               cur_question=cur_question,
                               max_score=max_score,
                               message=message,
                               hide_next_btn=hide_next_btn,
                               answer_state=answer_state,
                               username=username,
                               title=title)

    # For next question
    elif request.method == "GET" and cur_player_data["cur_question"] <= 10:
        cur_player_data["attempt"] = 1
        tree_name, tree_image, \
            max_score = get_q_data(cur_player_data["cur_question"])
        # Update players.json
        all_players_data = read_json_data("data/players.json")
        all_players_data = update_all_players_data(cur_player_data,
                                                   all_players_data)
        write_json_data(all_players_data, "data/players.json")

        return render_template("quiz.html",
                               tree_image=tree_image,
                               cur_score=cur_player_data["cur_score"],
                               attempt=cur_player_data["attempt"],
                               cur_question=cur_player_data["cur_question"],
                               max_score=max_score,
                               message="What is the name of this tree?",
                               hide_next_btn=True,
                               answer_state=0,
                               username=username,
                               title=title)

    # For game over
    elif request.method == "GET" and cur_player_data["cur_question"] > 10:
        all_players_data = read_json_data("data/players.json")
        cur_player_data, \
            all_players_data = get_cur_player_data(username,
                                                   all_players_data)
        leader = read_json_data("data/leaderboard.json")
        result_msg, cur_player_data, \
            leader = evaluate_result(cur_player_data, leader)
        write_json_data(leader, "data/leaderboard.json")
        score_str = str(cur_player_data["cur_score"])
        # Reset game
        cur_player_data["cur_score"] = 0
        cur_player_data["attempt"] = 1
        cur_player_data["cur_question"] = 1
        cur_player_data["game_num"] += 1
        # Update players.json
        all_players_data = read_json_data("data/players.json")
        all_players_data = update_all_players_data(cur_player_data,
                                                   all_players_data)
        write_json_data(all_players_data, "data/players.json")

        return render_template("game_over.html",
                               score_str=score_str,
                               result_msg=result_msg,
                               leader=leader,
                               username=username,
                               title="Game Over")
    return redirect('/')


@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    """
    Module returns leaderboard.html.
    """
    leaderboard = read_json_data("data/leaderboard.json")

    return render_template("leaderboard.html",
                           leaderboard=leaderboard,
                           title="Leaderboard")


@app.route('/instructions/')
def instructions():
    """
    Module returns instructions.html.
    """
    return render_template("instructions.html",
                           title="Instructions")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
