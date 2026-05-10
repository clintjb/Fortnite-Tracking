import requests
import json
import random
from datetime import datetime
import os

SECRET = os.environ['ENV_SECRET']

def get_fortnite_data(api_key):
    url = "https://fortnite-api.com/v2/stats/br/v2"
    params = {
        "name": "PlasticVogel",
        "accountType": "psn",
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data")
    except requests.exceptions.RequestException as e:
        print("Error connecting to the API:", e)
        return None

def main():
    api_key = SECRET
    api_response = get_fortnite_data(api_key)

    if api_response:
        print("Full API response:")
        print(json.dumps(api_response, indent=2))

        try:
            level = api_response.get("battlePass", {}).get("level", 0)
            overall = api_response["stats"]["all"]["overall"]

            top1_sum     = overall.get("wins", 0)
            kills_sum    = overall.get("kills", 0)
            kd_average   = round(overall.get("kd", 0), 2)
            winrate_average = round(overall.get("winRate", 0) * 100, 2)

            return level, top1_sum, kd_average, winrate_average, kills_sum
        except KeyError as e:
            print(f"Unexpected response structure: {e}")
            return None, None, None, None, None
    else:
        print("Failed to fetch Fortnite data.")
        return None, None, None, None, None

if __name__ == "__main__":
    level, top1_sum, kd_average, winrate_average, kills_sum = main()

    if level is not None:
        print("Level:", level)
        print("Wins:", top1_sum)
        print("K/D:", kd_average)
        print("Win Rate:", winrate_average)
        print("Kills:", kills_sum)
    else:
        print("Failed to retrieve Fortnite data.")

skin = random.randint(1, 28)
today = datetime.today()
date = today.strftime("%A %d %B %Y")

html = """\
<html>
<head>
<link rel="stylesheet" href="fortnite.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
<div class="card">
  <div class="layered-image">
    <img class="image-base" src="images/background.avif" alt="" style="width:100%"/>
    <img class="image-overlay" src="images/{skin}.png" alt="JΛV0XX_06" style="width:100%"/>
  </div>
  <h1>PlasticVogel</h1>
  <p class="title"><i class="fab fa-playstation"></i> Current Level - {level}</p>
  <div style="margin: 24px 0; color: lightslategrey;">
    <p><i class="fas fa-trophy"></i> {top1_sum} Victories</p>
    <p><i class="fas fa-star-half-alt"></i> {winrate_average} % Win Ratio</p>
    <p><i class="fas fa-tachometer-alt"></i> {kd_average} K/D Ratio</p>
    <p><i class="fas fa-skull-crossbones"></i> {kills_sum} Kills</p>
  </div>
  <p><small><small><small>Updated {date}</small></small></small></p>
  <p><button onclick="document.location='https://fortnitetracker.com/profile/all/PlasticVogel'">Detailed Stats</button></p>
</div>
</body>
</html>
""".format(**locals())

with open("fortnite.html", "w") as file:
    file.write(html)
