import requests
import json
import random

SECRET = os.environ['SECRET']

def get_fortnite_data(api_key):
    url = "https://fortniteapi.io/v1/stats?account=5afc257cdbf8408ebebcf241a681a1e9"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error connecting to the API:", e)
        return None

def main():
    api_key = SECRET

    # Fetch Fortnite data
    api_response = get_fortnite_data(api_key)

    if api_response:
        # Store top level values for processing in HTML
        level = api_response["account"]["level"]
        top1_sum = sum([mode_stats["placetop1"] for mode_stats in api_response["global_stats"].values()])
        kd_average = round(sum([mode_stats["kd"] for mode_stats in api_response["global_stats"].values()]) / len(api_response["global_stats"]), 2)
        winrate_average = round((sum([mode_stats["winrate"] for mode_stats in api_response["global_stats"].values()]) / len(api_response["global_stats"])) * 100, 2)
        kills_sum = sum([mode_stats["kills"] for mode_stats in api_response["global_stats"].values()])

        # Additional processing with api_response

        # Return all variables
        return level, top1_sum, kd_average, winrate_average, kills_sum

    else:
        print("Failed to fetch Fortnite data.")
        return None, None, None, None, None

if __name__ == "__main__":
    level, top1_sum, kd_average, winrate_average, kills_sum = main()

    if level is not None:
        print("Level value:", level)
        print("Sum of all 'placetop1':", top1_sum)
        print("Average of all 'kd':", kd_average)
        print("Average of all 'winrate':", winrate_average)
        print("Sum of all 'kills':", kills_sum)
    else:
        print("Failed to retrieve Fortnite data.")

skin = (random.randint(1, 20))

html = """\
<html>
<head>
<link rel="stylesheet" href="fortnite.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
<div class="card">
  <div class="layered-image">
    <img class="image-base" src="https://clintbird.com/images/posts/2024/fortnite_skins/background.avif" alt="" style="width:100%"/>
    <img class="image-overlay" src="https://clintbird.com/images/posts/2024/fortnite_skins/{skin}.png" alt="IronVogel" style="width:100%"/>
  </div>
  <h1>IronVogel</h1>
  <p class="title"><i class="fab fa-playstation"  ></i> Current Level - {level}</p>
  <div style="margin: 24px 0;  color: lightslategrey;">
    <p><i class="fas fa-trophy"></i> {top1_sum} Victories</p>
    <p><i class="fas fa-star-half-alt"></i> {winrate_average} % Win Ratio</p>
    <p><i class="fas fa-tachometer-alt"></i> {kd_average} K/D Ratio</p>
    <p><i class="fas fa-skull-crossbones"></i> {kills_sum} Kills</p>
  </div>
  <p><button onclick="document.location='https://fortnitetracker.com/profile/all/IronVogel'">Detailed Stats</button></p>
</div>
</body>
</html>
""".format(**locals())

# Output to HTML file
with open("fortnite.html", "w") as file:
    file.write(html)