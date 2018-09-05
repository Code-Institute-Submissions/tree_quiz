data = [ {"name": "dan","game_num": 0}, {"name": "col","game_num": 0}]
name = "danc"
user_info = {"name": name, "game_num": 0}
past_player = False

for obj in data:
    if obj["name"] == name:
        obj["game_num"] +=1
        past_player = True
if past_player == False:
    data.append(user_info)

print(data)