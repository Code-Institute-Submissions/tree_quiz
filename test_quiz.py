import unittest
import run
import os
import json
from flask import Flask, render_template, request


class TestQuiz(unittest.TestCase):

    def test_update_all_players_data(self):
        """
        Tests update_all_player_data(), which updates all_players_data with
        the cur_player_data. Does nothing if player not in all player data.
        """
        # Check: Updates players data in all players data
        all_players_data = [{"name": "name1", "game_num": 1,
                             "cur_question": 1, "attempt": 1,
                             "cur_score": 0, "high_score": 50},
                            {"name": "name2", "game_num": 1,
                             "cur_question": 1, "attempt": 1,
                             "cur_score": 0, "high_score": 0}]
        cur_player_data = {"name": "name2", "game_num": 2,
                           "cur_question": 5, "attempt": 2,
                           "cur_score": 50, "high_score": 100}
        expected_new_all_players_data = [{"name": "name1", "game_num": 1,
                                          "cur_question": 1, "attempt": 1,
                                          "cur_score": 0, "high_score": 50},
                                         {"name": "name2", "game_num": 2,
                                          "cur_question": 5, "attempt": 2,
                                          "cur_score": 50, "high_score": 100}]
        new_all_players_data = run.update_all_players_data(cur_player_data,
                                                           all_players_data)
        self.assertEqual(expected_new_all_players_data, new_all_players_data)
        # Check: Does nothing if players name not in all players data
        all_players_data = [{"name": "name1", "game_num": 1,
                             "cur_question": 1, "attempt": 1,
                             "cur_score": 0, "high_score": 50},
                            {"name": "name2", "game_num": 1,
                             "cur_question": 1, "attempt": 1,
                             "cur_score": 0, "high_score": 0}]
        cur_player_data = {"name": "name3", "game_num": 2,
                           "cur_question": 5, "attempt": 2,
                           "cur_score": 50, "high_score": 100}
        new_all_players_data = run.update_all_players_data(cur_player_data,
                                                           all_players_data)
        self.assertEqual(all_players_data, new_all_players_data)

    def test_get_cur_player_data(self):
        """
        Tests get_cur_player_data(), which checks if a username is in
        the player database, returns the users info or else creates user info
        for the new user.
        """
        # Check: Empty player data, add user
        all_player_data_old = []
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        all_player_data_new = [{"name": "name1", "game_num": 1,
                                "cur_question": 1, "attempt": 1,
                                "cur_score": 0, "high_score": 0}]
        self.assertEqual((cur_player_data, all_player_data_new),
                         run.get_cur_player_data("name1", all_player_data_old))

        # Check: 2 players, user new
        all_player_data_old = [{"name": "name1", "game_num": 1,
                                "cur_question": 1,
                                "attempt": 1, "cur_score": 0,
                                "high_score": 100},
                               {"name": "name2", "game_num": 1,
                                "cur_question": 1, "attempt": 1,
                                "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name3", "game_num": 1, "cur_question": 1,
                           "attempt": 1, "cur_score": 0, "high_score": 0}
        all_player_data_new = [{"name": "name1", "game_num": 1,
                                "cur_question": 1, "attempt": 1,
                                "cur_score": 0, "high_score": 100},
                               {"name": "name2", "game_num": 1,
                                "cur_question": 1, "attempt": 1,
                                "cur_score": 0, "high_score": 90},
                               {"name": "name3", "game_num": 1,
                                "cur_question": 1, "attempt": 1,
                                "cur_score": 0, "high_score": 0}]
        self.assertEqual((cur_player_data, all_player_data_new),
                         run.get_cur_player_data("name3", all_player_data_old))

        # Check: 3 players, user in database
        all_player_data_old = [{"name": "name1", "game_num": 1,
                                "cur_question": 0, "attempt": 1,
                                "cur_score": 0, "high_score": 100},
                               {"name": "name2", "game_num": 0,
                                "cur_question": 0, "attempt": 1,
                                "cur_score": 0, "high_score": 90},
                               {"name": "name3", "game_num": 0,
                                "cur_question": 0, "attempt": 1,
                                "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 0, "attempt": 1,
                           "cur_score": 0, "high_score": 100}
        all_player_data_new = all_player_data_old
        self.assertEqual((cur_player_data, all_player_data_new),
                         run.get_cur_player_data("name1", all_player_data_old))

        # Check: Username not case sensitive
        all_player_data_old = [{"name": "name1", "game_num": 1,
                                "cur_question": 0,
                                "attempt": 1, "cur_score": 0,
                                "high_score": 100},
                               {"name": "name2", "game_num": 0,
                                "cur_question": 0, "attempt": 1,
                                "cur_score": 0, "high_score": 90},
                               {"name": "name3", "game_num": 0,
                                "cur_question": 0, "attempt": 1,
                                "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 0,
                           "attempt": 1, "cur_score": 0, "high_score": 100}
        all_player_data_new = all_player_data_old
        self.assertEqual((cur_player_data, all_player_data_new),
                         run.get_cur_player_data("NamE1", all_player_data_old))

    def test_get_q_data(self):
        """
        Tests test_get_q_data(question), which returns the tree name,
        url of tree image and max possible score for a given question number.
        """
        # Check if function gets the correct q data
        self.assertEqual(("arbutus", "/static/img/arbutus.jpg", 10),
                         run.get_q_data(1))
        self.assertEqual(("ash", "/static/img/ash.jpg", 20),
                         run.get_q_data(2))
        self.assertEqual(("holly", "/static/img/holly.jpg", 60),
                         run.get_q_data(6))

    def test_add_to_score(self):
        """
        Tests add_to_score, which increments the users score by 10
        if user answers question correctly on first attempt, or
        by 5 if user answers correctly on second attempt
        """
        # Check current score increased by 10 if attempt = 1
        cur_player_data = {"name": "name1", "game_num": 0,
                           "cur_question": 0, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        new_cur_player_data = run.add_to_score(cur_player_data)
        self.assertEqual(new_cur_player_data["cur_score"], 10)
        # Check current score increased by 5 if attempt > 1
        cur_player_data = {"name": "name1", "game_num": 0,
                           "cur_question": 0, "attempt": 2,
                           "cur_score": 10, "high_score": 0}
        new_cur_player_data = run.add_to_score(cur_player_data)
        self.assertEqual(new_cur_player_data["cur_score"], 15)

    def test_process_answer(self):
        """
        Tests process_answer(), which checks if the users entered answer is
        correct, and returns appropriate feedback message and whether to allow
        access to next question button.
        """
        # Check: For correct answer, first attempt
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 2, "attempt": 1,
                                    "cur_score": 10, "high_score": 0}
        tree_name = "arbutus"
        answer = "arbutus"
        feedback_msg, \
            hide_next_btn, \
            cur_player_data, \
            answer_state = run.process_answer(answer,
                                              tree_name,
                                              cur_player_data)
        self.assertEqual(feedback_msg, "Arbutus is the correct answer!")
        self.assertFalse(hide_next_btn)
        self.assertEqual(cur_player_data, expected_cur_player_data)
        self.assertEqual(answer_state, 1)

        # Check: For correct answer, second attempt
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 2,
                           "cur_score": 0, "high_score": 0}
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 2, "attempt": 2,
                                    "cur_score": 5, "high_score": 0}
        tree_name = "arbutus"
        answer = "arbutus"
        feedback_msg, \
            hide_next_btn, \
            cur_player_data, \
            answer_state = run.process_answer(answer,
                                              tree_name,
                                              cur_player_data)
        self.assertEqual(feedback_msg, "Arbutus is the correct answer!")
        self.assertFalse(hide_next_btn)
        self.assertEqual(cur_player_data, expected_cur_player_data)
        self.assertEqual(answer_state, 1)

        # Check: For wrong answer, first attempt
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 1, "attempt": 2,
                                    "cur_score": 0, "high_score": 0}
        tree_name = "arbutus"
        answer = "birch"
        expected_feedback = ("Birch is not correct," +
                             " but you still have a second try.")
        feedback_msg, \
            hide_next_btn, \
            cur_player_data, \
            answer_state = run.process_answer(answer,
                                              tree_name,
                                              cur_player_data)
        self.assertEqual(feedback_msg, expected_feedback)
        self.assertTrue(hide_next_btn)
        self.assertEqual(cur_player_data, expected_cur_player_data)
        self.assertEqual(answer_state, 2)
        # Check: For wrong answer, first second attempt
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 2,
                           "cur_score": 0, "high_score": 0}
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 2, "attempt": 2,
                                    "cur_score": 0, "high_score": 0}
        tree_name = "arbutus"
        answer = "birch"
        feedback_msg, \
            hide_next_btn, \
            cur_player_data, \
            answer_state = run.process_answer(answer,
                                              tree_name,
                                              cur_player_data)
        self.assertEqual(feedback_msg,
                         "Wrong again! Arbutus is the correct answer.")
        self.assertFalse(hide_next_btn)
        self.assertEqual(cur_player_data, expected_cur_player_data)
        self.assertEqual(answer_state, 2)

    def test_add_to_leaderboard(self):
        """
        Testing of add_to_leader_board(), which checks if the users current
        score is a personnel best and if that personnel best makes it onto
        a 5 person leaderboard.
        """
        # Test first player, empty leaderboard
        user_info = {"cur_score": 0,
                     "attempt": 1,
                     "name": "name1",
                     "cur_question": 0,
                     "high_score": 10,
                     "game_num": 0}
        leader = []
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, ["name1", 10, 0])
        self.assertTrue(made_leader)

        # Test second player, leaderboard not full
        # score higher than current high score
        user_info = {"cur_score": 0,
                     "attempt": 1,
                     "name": "name3",
                     "cur_question": 0,
                     "high_score": 30,
                     "game_num": 2}
        leader = ["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name3", 30, 2, "name1", 20, 0, "name2", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)

        # Test second player, leaderboard not full
        # score between scores on leaderboard
        user_info = {"cur_score": 0,
                     "attempt": 1, "name":
                     "name3", "cur_question": 0,
                     "high_score": 15, "game_num": 2}
        leader = ["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name1", 20, 0, "name3", 15, 2, "name2", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)

        # Test third player, leaderboard not full
        # score less than scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name3",
                     "cur_question": 0, "high_score": 5, "game_num": 2}
        leader = ["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name1", 20, 0, "name2", 10, 0, "name3", 5, 2]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)

        # Test sixed player, leaderboard full
        # Score between scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6",
                     "cur_question": 0, "high_score": 30, "game_num": 2}
        leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                  "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name6", 30, 2,
                      "name3", 30, 0, "name4", 20, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)

        # Test sixed player, leaderboard full
        # score same as lowest score on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6",
                     "cur_question": 0, "high_score": 10, "game_num": 2}
        leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                  "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name6", 10, 2]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)

        # Test sixed player, leaderboard full
        # score less than scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6",
                     "cur_question": 0, "high_score": 5, "game_num": 2}
        leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                  "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name5", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertFalse(made_leader)

    def test_evaluate_result(self):
        """
        Tests evaluate_results(), which compares the users final result
        against their past scores and the leaderboard, returns message
        """
        # Check: Player scores 0
        cur_player_data_old = {"name": "name1", "game_num": 0,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 0, "high_score": 0}
        leader_old = []
        expected_msg = ("You can do better than 0. You should try again," +
                        " I'm sure you have learned from your mistakes.")
        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, cur_player_data_old)
        self.assertEqual(leader_new, leader_old)
        # Check: Players first game, gets 100/100
        cur_player_data_old = {"name": "name1", "game_num": 1,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 100, "high_score": 0}
        leader_old = []
        expected_msg = ("Congratulations! You got top marks on your" +
                        " first game. Check out the leaderboard.")
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 100, "high_score": 100}
        expected_leader = ['name1', 100, 1]
        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

        # Check: Players first game, gets on leaderboard
        cur_player_data_old = {"name": "name6", "game_num": 1,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 10, "high_score": 0}
        leader_old = ["name1", 100, 1, "name2", 90, 1, "name3", 30, 1,
                      "name4", 20, 1, "name5", 10, 0]
        expected_msg = ("Excellent! First game and you made" +
                        " it on the leaderboard.")
        expected_cur_player_data = {"name": "name6", "game_num": 1,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 10, "high_score": 10}
        expected_leader = ["name1", 100, 1, "name2", 90, 1, "name3", 30, 1,
                           "name4", 20, 1, "name6", 10, 1]

        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

        # Check: Players first game, did not make it on leaderboard
        cur_player_data_old = {"name": "name6", "game_num": 1,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 5, "high_score": 0}
        leader_old = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name5", 10, 0]
        expected_msg = ("Good first try. Have" +
                        " another game and try to make it onto leaderboard.")
        expected_cur_player_data = {"name": "name6", "game_num": 1,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 5, "high_score": 5}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                           "name4", 20, 0, "name5", 10, 0]

        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

        # Check: Players before, scored personnel best
        # but did not make leaderboard
        cur_player_data_old = {"name": "name6", "game_num": 2,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 5, "high_score": 0}
        leader_old = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name5", 10, 0]
        expected_msg = "You are improving. Keep trying to get top marks."
        expected_cur_player_data = {"name": "name6", "game_num": 2,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 5, "high_score": 5}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                           "name4", 20, 0, "name5", 10, 0]

        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

        # Check: Players before, scored personnel best, made it on leaderboard
        cur_player_data_old = {"name": "name6", "game_num": 2,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 10, "high_score": 5}
        leader_old = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name5", 10, 0]
        expected_msg = ("Excellent! You made it onto the leaderboard" +
                        " with this new personal best.")
        expected_cur_player_data = {"name": "name6", "game_num": 2,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 10, "high_score": 10}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                           "name4", 20, 0, "name6", 10, 2]

        result_msg, \
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

        # Check: Players before, score less than high score
        cur_player_data_old = {"name": "name6", "game_num": 2,
                               "cur_question": 0, "attempt": 1,
                               "cur_score": 5, "high_score": 10}
        leader_old = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                      "name4", 20, 0, "name5", 10, 0]
        expected_msg = "Good job, but you didn't beat your own top score of 10"
        expected_cur_player_data = {"name": "name6", "game_num": 2,
                                    "cur_question": 0, "attempt": 1,
                                    "cur_score": 5, "high_score": 10}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0,
                           "name4", 20, 0, "name5", 10, 0]

        result_msg,\
            cur_player_data_new, \
            leader_new = run.evaluate_result(cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

    def test_get_welcome_msg(self):
        """
        Tests get_welcome_msg(), which returns the appropriate welcome message
        based on the users playing history.
        """
        # New player
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        expected_welcome_msg = ("Welcome name1." +
                                " This looks like your first game.")
        expected_cur_player_data = {"name": "name1", "game_num": 0,
                                    "cur_question": 1, "attempt": 1,
                                    "cur_score": 0, "high_score": 0}
        welcome_msg, cur_player_data = run.get_welcome_msg(cur_player_data)
        self.assertEqual((welcome_msg, cur_player_data),
                         (expected_welcome_msg, cur_player_data))

        # Player mid-game
        cur_player_data = {"name": "name1", "game_num": 1,
                           "cur_question": 5, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        expected_welcome_msg = ("Welcome back name1." +
                                " Looks like you left us mid game." +
                                " You are currently on question 5.")
        expected_cur_player_data = {"name": "name1", "game_num": 1,
                                    "cur_question": 5, "attempt": 1,
                                    "cur_score": 0, "high_score": 0}
        welcome_msg, cur_player_data = run.get_welcome_msg(cur_player_data)

        self.assertEqual((welcome_msg, cur_player_data),
                         (expected_welcome_msg, expected_cur_player_data))

        # Player has played before, new game
        cur_player_data = {"name": "name1", "game_num": 2,
                           "cur_question": 1, "attempt": 1,
                           "cur_score": 0, "high_score": 0}
        expected_welcome_msg = ("Welcome back name1." +
                                " You have played this game 1 times before.")

        expected_cur_player_data = {"name": "name1", "game_num": 2,
                                    "cur_question": 1, "attempt": 1,
                                    "cur_score": 0, "high_score": 0}
        welcome_msg, cur_player_data = run.get_welcome_msg(cur_player_data)
        self.assertEqual((welcome_msg, cur_player_data),
                         (expected_welcome_msg, expected_cur_player_data))
