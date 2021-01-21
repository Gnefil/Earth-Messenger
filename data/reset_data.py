import json

data = {"level": 1,
        "leader_board": [],
        "initial_hint": True,
        "fall_speed": "medium",
        "enemy": True,
        "numbers_shown": False
        }

for i in range(10):
    data['leader_board'].append({"name": "Anonymus", "lv": 1, "time": 30})


with open("data.json", "w") as f:
    f.truncate()
    json.dump(data, f, indent=2)
    f.close()

with open("data.json") as f:
    d = json.load(f)
    f.close()

print(d)
