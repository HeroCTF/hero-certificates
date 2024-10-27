from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, after_this_request, send_file
import requests
import os

def generate_certificate(template, username, team, rank, number_of_teams, filename):
    img = Image.open(template).convert("RGB")
    drawable = ImageDraw.Draw(img)

    username_position = (560, 650)
    ranking_position = (730, 850)
    
    text_color = (0, 255, 255)
    
    font_path = "resources/MarchRough.ttf"

    username_team = f"{username} from {team}"
    ranking = f"#{rank} / {number_of_teams}"
    
    for text, position, size in zip([username_team, ranking], [username_position, ranking_position], [(750, 100), (400, 100)]):

        rect_width, rect_height = size
        if len(text) > 24:
            rect_width += 300
            position = (position[0]-150, position[1])
        font_size = 300

        while True:
            font = ImageFont.truetype(font_path, font_size)
            
            text_bbox = drawable.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            if text_width <= rect_width and text_height <= rect_height:
                break
            font_size -= 1 

        x = position[0] + (rect_width - text_width) // 2
        y = position[1] + (rect_height - text_height) // 2
        
        drawable.text((x, y), text, fill=text_color, font=font)

    img.save(filename)


app = Flask(__name__, template_folder='.', static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form.get('token')
        if token:
            response = requests.get(f"https://ctf.heroctf.fr/api/v1/users/me", headers={"Authorization": f"Token {token}", "Content-Type": "application/json"})
            
            if response.status_code == 200:
                username = response.json()["data"]["name"]
                response = requests.get(f"https://ctf.heroctf.fr/api/v1/teams/me", headers={"Authorization": f"Token {token}", "Content-Type": "application/json"})
                
                if response.status_code == 200:
                    team_name = response.json()["data"]["name"]
                    score = response.json()["data"]["place"]
                    response = requests.get(f"https://ctf.heroctf.fr/api/v1/teams", headers={"Authorization": f"Token {token}", "Content-Type": "application/json"})
                    
                    if response.status_code == 200:
                        max_teams = response.json()["meta"]["pagination"]["total"]
                        
                        @after_this_request
                        def remove_file(response):
                            try:
                                os.remove(filename)
                            except:
                                pass
                            return response
                        
                        filename = f"certificates/{username}-hero-certif.pdf"
                        generate_certificate("resources/template.png", username, team_name, score, max_teams, filename)
                        return send_file(filename, as_attachment=True)
        
        return render_template('index.html', error="Could not authenticate to the CTFd instance.")
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('LISTEN_PORT', '80')), debug=True)