import run
import json
from flask import Flask, render_template, request, flash
name = "ben"
score = 100
game_num = 2
"""
test_list = [10, 55]


print(score)
print(min(test_list))
if score > min(test_list):
    print("score > test list")
else:
    print("why not")

"""
with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)

print(leader)

print(score)


run.add_to_leader_board(name, score, game_num)

with open("data/leader_board.json", "r") as json_leader_board:
        leader = json.load(json_leader_board)

print(leader)

        