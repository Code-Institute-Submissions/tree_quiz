import unittest
from string import ascii_uppercase
import run
import os
import json
from flask import Flask, render_template, request, flash

class TestQuiz(unittest.TestCase):
    def test_get_q_data(self):
        """
        Test test_get_q_data(index). Gets the tree name and url of tree image
        for the next question
        """
        # Check if funciton gets the correct q data
        self.assertEquals(("arbutus", "/static/img/arbutus.jpg"), run.get_q_data(1))
        self.assertEquals(("holly", "/static/img/holly.jpg"), run.get_q_data(6))
        
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
        

