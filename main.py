import requests
from PIL import Image
from datetime import datetime
import hashlib
import vdf
import os
import random

gameid = 1222670
screenshots_path = f"output/remote/{gameid}/screenshots/"
vdf_path = "output/screenshots.vdf"

start_date = "2025-02-03"
end_date = "2025-04-26"

def download_image(url, img_name):
    
    output_path = screenshots_path + img_name
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(output_path, "wb") as img:
        for chunk in response.iter_content():
            if chunk:
                img.write(chunk)


def create_thumbnail(img_name):
    previews_dir = screenshots_path + "thumbnails/"
    
    # Open, resize, and save
    with Image.open(screenshots_path + img_name) as img:
        thumb = img.resize((200, 112), Image.LANCZOS)
        thumb_path = previews_dir + img_name
        thumb.save(thumb_path)


def write_screenshots_vdf():

    images = []

    for img_file in os.listdir(screenshots_path):
        if not img_file.endswith(".jpg"):
            continue
            
        time_format = "%Y-%m-%d"
        start_ts  = int(datetime.strptime(start_date, time_format).timestamp())
        end_ts    = int(datetime.strptime(end_date, time_format).timestamp())
        
        creation = str(random.randint(start_ts, end_ts))
        
        
        img = Image.open(screenshots_path + img_file)
        width, height = img.size
        img.close()
        images.append({
            "type":        "1",
            "filename":    f"{gameid}/screenshots/{img_file}",
            "thumbnail":   f"{gameid}/screenshots/thumbnails/{img_file}",
            "imported":    "0",
            "width":       str(width),
            "height":      str(height),
            "gameid":      gameid,
            "creation":    creation,
            "Permissions": "2",
        })
        

    data = {
        "screenshots": {
            gameid: { str(idx): shot for idx, shot in enumerate(images)},
            "shortcutnames": {}
        }
    }
    
    with open(vdf_path, "w") as f:
        vdf.dump(data, f)


with open("urls.txt","r") as url_file:

    
    os.makedirs(screenshots_path, exist_ok=True)
    os.makedirs(screenshots_path + "thumbnails/", exist_ok=True)
    
    counter = 1
    total = sum(1 for line in url_file)
    url_file.seek(0)
    
    for line in url_file:
        img_name = hashlib.blake2s(line.encode(), digest_size=4).hexdigest() + ".jpg"
        
        print(f"[{counter}/{total}]" + img_name)
        download_image(line, img_name)
        create_thumbnail(img_name)
        counter += 1
    write_screenshots_vdf()
        
    print("Done")
