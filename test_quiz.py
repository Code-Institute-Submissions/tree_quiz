import unittest
from string import ascii_uppercase
import run
import os
import json
from flask import Flask, render_template, request, flash

class TestQuiz(unittest.TestCase):
    
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
        


        



            
    
    # Working from highest to lowest, insert player into highest rank

    
        
        