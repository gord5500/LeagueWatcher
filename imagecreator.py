from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
import json

def create(match, champions):

    game_id = match["gameId"]
    participants = match["participants"]
    img = Image.open("background.jpg")
    font = ImageFont.truetype('arial.ttf', 20)
    img.thumbnail((img.size[0] / 2, img.size[1] / 2))
    draw = ImageDraw.Draw(img)
    x, y = 90, 110
    box_x, box_y = 40, 50
    count = 0

    title_font = ImageFont.truetype("arial.ttf", 40)
    draw.text((85, 10), get_queue_type(match["gameQueueConfigId"]), (0, 0, 0), title_font)

    for player in participants:
        #print(player["teamId"], player["championId"], player["summonerName"])
        #print(box_x + ((player["teamId"] / 100 - 1) * 50))
        draw.rectangle([box_x + ((player["teamId"] / 100 - 1) * 275), box_y + 50,
                        box_x + ((player["teamId"] / 100 - 1) * 275) + 250, box_y + 50 + 40], outline=(0, 0, 0),
                       fill=(255, 255, 255))
        draw.text((x + ((player["teamId"] / 100 - 1) * 275), y), player["summonerName"], (0, 0, 0), font)

        icon = get_icon(champions["{}".format(player["championId"])])
        img.paste(icon, (x - 50 + (int(player["teamId"] / 100 - 1) * 275), y - 10))
        y = y + 50
        box_y = (box_y % 250) + 50

        count += 1
        if count == 5:
            y = 110

    return img


def get_icon(name):

    formats = ["https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square.{0}.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square_0.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square_0.{0}.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square_0.s_yordle.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/{0}_square.ruinedking.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/oriana_square.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/cryophoenix_square.png",
               "https://raw.communitydragon.org/latest/game/assets/characters/{0}/hud/chronokeeper_square.png"]

    response = requests.get(formats[0].format(name.lower()))
    i = 1

    while response.status_code == 404 and i < len(formats):
        response = requests.get(formats[i].format(name.lower()))
        i += 1

    #print(name)
    img = Image.open(BytesIO(response.content))
    img.thumbnail([40, 40])
    return img

def get_queue_type(id):

    response = requests.get("https://static.developer.riotgames.com/docs/lol/queues.json")
    queues = json.loads(json.dumps(response.json()))

    for queue in queues:
        if queue["queueId"] == id:
            return queue["description"]

    return "Unknown Game Mode"