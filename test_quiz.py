import unittest
from string import ascii_uppercase
import run
import os
import json
from flask import Flask, render_template, request, flash

class TestQuiz(unittest.TestCase):
    
    def test_get_cur_player_data(self):
        """
        If the username has been used before returns the user info,
        else adds the new new users info to the all_player_data list
        """
        # Check: Empty player data, add user
        all_player_data_old = []
        cur_player_data = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        all_player_data_new = [{"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}]
        self.assertEqual((cur_player_data, all_player_data_new), run.get_cur_player_data("name1", all_player_data_old))
        
        # Check: 2 players, user new played
        all_player_data_old = [{"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}, {"name": "name2","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name3","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        all_player_data_new = [{"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}, {"name": "name2","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}, {"name": "name3","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}]
        self.assertEqual((cur_player_data, all_player_data_new), run.get_cur_player_data("name3", all_player_data_old))
        # Check: 3 players, user has played before
        all_player_data_old = [{"name": "name1","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}, {"name": "name2","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}, {"name": "name3","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name1","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}
        all_player_data_new = all_player_data_old
        self.assertEqual((cur_player_data, all_player_data_new), run.get_cur_player_data("name1", all_player_data_old))
        # Check: Username not case sensitive
        all_player_data_old = [{"name": "name1","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}, {"name": "name2","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}, {"name": "name3","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 90}]
        cur_player_data = {"name": "name1","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 100}
        all_player_data_new = all_player_data_old
        self.assertEqual((cur_player_data, all_player_data_new), run.get_cur_player_data("NamE1", all_player_data_old))
        
    def test_get_q_data(self):
        """
        Test test_get_q_data(index). Gets the tree name and url of tree image
        for the next question
        """
        # Check if funciton gets the correct q data
        self.assertEqual(("arbutus", "/static/img/arbutus.jpg"), run.get_q_data(1))
        self.assertEqual(("holly", "/static/img/holly.jpg"), run.get_q_data(6))
        
    def test_check_answer(self):
        "Test check_answer(index, answer), returns True or False"
        # Check for all right answers
        self.assertTrue(run.check_answer(1,"arbutus"))
        self.assertTrue(run.check_answer(2,"ash"))
        self.assertTrue(run.check_answer(3,"birch"))
        self.assertTrue(run.check_answer(4,"hawthorn"))
        self.assertTrue(run.check_answer(5,"hazel"))
        self.assertTrue(run.check_answer(6,"holly"))
        self.assertTrue(run.check_answer(7,"oak"))
        self.assertTrue(run.check_answer(8,"pine"))
        self.assertTrue(run.check_answer(9,"willow"))
        self.assertTrue(run.check_answer(10,"yew"))
        # Check for wrong answer
        self.assertFalse(run.check_answer(2,"arbutus"))
        # Check accepts captialized
        self.assertTrue(run.check_answer(1,"ArbuTus"))
    
    def test_add_to_score(self):
        """
        Test if first attemp current score gets incremented by 10, else
        gets incremented by 5
        """
        # Check current score incrented by 10 if attempt = 1
        cur_player_data = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        new_cur_player_data = run.add_to_score(cur_player_data)
        self.assertEqual(new_cur_player_data["cur_score"], 10)
        # Check current score incrented by 5 if attempt > 1
        cur_player_data = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 2, "cur_score": 10, "high_score": 0}
        new_cur_player_data = run.add_to_score(cur_player_data)
        self.assertEqual(new_cur_player_data["cur_score"], 15)
        
    def test_add_to_leaderboard(self):
        """
        Testing of add_to_leader_board(). Checks all possible scenario of leaderboard and final scores. 
        """
        
        # Test first player, empty leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name1", "cur_question": 0, "high_score": 10, "game_num": 0}
        leader=[]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, ["name1", 10, 0])
        self.assertTrue(made_leader)
        
        # Test second player, leaderboard not full, score higher than current high score
        user_info = {"cur_score": 0, "attempt": 1, "name": "name3", "cur_question": 0, "high_score": 30, "game_num": 2}
        leader=["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name3", 30, 2,"name1", 20, 0, "name2", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)
        
        # Test second player, leaderboard not full, score between scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name3", "cur_question": 0, "high_score": 15, "game_num": 2}
        leader=["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name1", 20, 0, "name3", 15, 2, "name2", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)
        
        # Test third player, leaderboard not full, score less than scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name3", "cur_question": 0, "high_score": 5, "game_num": 2}
        leader=["name1", 20, 0, "name2", 10, 0]
        leader_new = ["name1", 20, 0, "name2", 10, 0, "name3", 5, 2]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)
        
        # Test sixed player, leaderboard full, score between scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6", "cur_question": 0, "high_score": 30, "game_num": 2}
        leader=["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name6", 30, 2, "name3", 30, 0, "name4", 20, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)
        
        # Test sixed player, leaderboard full, score same as lowest score on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6", "cur_question": 0, "high_score": 10, "game_num": 2}
        leader=["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name6", 10, 2]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertTrue(made_leader)
        
        # Test sixed player, leaderboard full, score less than scores on leaderboard
        user_info = {"cur_score": 0, "attempt": 1, "name": "name6", "cur_question": 0, "high_score": 5, "game_num": 2}
        leader=["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        leader_new = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        made_leader, leader = run.add_to_leaderboard(user_info, leader)
        self.assertEqual(leader, leader_new)
        self.assertFalse(made_leader)
        
    def test_evaluate_result(self):

        # Check: Player scores 0
        cur_player_data_old = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 0, "high_score": 0}
        leader_old = []
        expected_msg = "You can do better than 0. You should try again, I'm sure you have learned from your mistakes." 
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, cur_player_data_old)
        self.assertEqual(leader_new, leader_old)
        
        # Check: Players first game, gets 100/100
        cur_player_data_old = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 100, "high_score": 0}
        leader_old = []
        expected_msg = "Congradulations! You got top marks on your first game. Check out the leaderboard." 
        expected_cur_player_data = {"name": "name1","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 100, "high_score": 100}
        expected_leader = ['name1', 100, 0]    
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)
        
        # Check: Players first game, gets on leaderboard
        cur_player_data_old = {"name": "name6","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 10, "high_score": 0}
        leader_old =["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        expected_msg = "Excelent! First game and you made it on the leaderboard." 
        expected_cur_player_data = {"name": "name6","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 10, "high_score": 10}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name6", 10, 0]
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)
        
        # Check: Players first game, did not make it on leaderboard
        cur_player_data_old = {"name": "name6","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 0}
        leader_old =["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        expected_msg = "Good first try. Have another game and try to make it onto leaderboard."
        expected_cur_player_data = {"name": "name6","game_num": 0, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 5}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)
        
        # Check: Players before, scored personnel best, but did not make leaderboard
        cur_player_data_old = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 0}
        leader_old =["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        expected_msg = "You are improving. Keep trying to get top marks."
        expected_cur_player_data = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 5}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)
        
        # Check: Players before, scored personnel best, made it on leaderboard
        cur_player_data_old = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 10, "high_score": 5}
        leader_old =["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        expected_msg = "Excelent! You made it onto the leaderboard with this new personnel best."
        expected_cur_player_data = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 10, "high_score": 10}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name6", 10, 1]
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)
        
        # Check: Players before, score less than high score
        cur_player_data_old = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 10}
        leader_old =["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        expected_msg = "Good job, but you didn't beat your own top score of 10"
        expected_cur_player_data = {"name": "name6","game_num": 1, 
            "cur_question": 0, "attempt": 1, "cur_score": 5, "high_score": 10}
        expected_leader = ["name1", 100, 0, "name2", 90, 0, "name3", 30, 0, "name4", 20, 0, "name5", 10, 0]
        
        result_msg, cur_player_data_new, leader_new = run.evaluate_result( 
                                                          cur_player_data_old, leader_old)
        self.assertEqual(result_msg, expected_msg)
        self.assertEqual(cur_player_data_new, expected_cur_player_data)
        self.assertEqual(leader_new, expected_leader)

