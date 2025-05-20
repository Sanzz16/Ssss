from flask import Flask, request, render_template, send_file
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

BASE_IMAGE_URL = "https://iili.io/39iE4rF.jpg"

API_KEYS = {
    "MARCOxIROTECH": True,
    "1DAY": True,
    "busy": False
}

def is_key_valid(api_key):
    return API_KEYS.get(api_key, False)

def fetch_data(region, uid):
    url = f"http://hyper-full-info-api.vercel.app/info?uid={uid}&region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def overlay_images(base_image, item_ids):
    base = Image.open(BytesIO(requests.get(base_image).content)).convert("RGBA")
    positions = [(485,473), (295,546), (290,40), (479,100), (550,280), (100,470)]
    sizes = [(130,130)] * 6

    for idx, item_id in enumerate(item_ids[:6]):
        item_url = f"https://pika-ffitmes-api.vercel.app/?item_id={item_id}&watermark=TaitanApi&key=PikaApis"
        item = Image.open(BytesIO(requests.get(item_url).content)).convert("RGBA")
        item = item.resize(sizes[idx], Image.LANCZOS)
        base.paste(item, positions[idx], item)

    return base

@app.route('/', methods=['GET', 'POST'])
def index():
    image_data = None
    error = None

    if request.method == 'POST':
        uid = request.form.get('uid')
        region = request.form.get('region')
        api_key = request.form.get('key')

        if not uid or not region or not api_key:
            error = "Semua field harus diisi ya!"
        elif not is_key_valid(api_key):
            error = "API key-nya salah atau nggak aktif!"
        else:
            data = fetch_data(region, uid)
            if not data or "AccountProfileInfo" not in data or "EquippedOutfit" not in data["AccountProfileInfo"]:
                error = "Data nggak ditemukan. Coba cek UID & region-nya ya!"
            else:
                item_ids = data["AccountProfileInfo"]["EquippedOutfit"]
                overlaid = overlay_images(BASE_IMAGE_URL, item_ids)
                img_io = BytesIO()
                overlaid.save(img_io, 'PNG')
                img_io.seek(0)
                return send_file(img_io, mimetype='image/png')

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
