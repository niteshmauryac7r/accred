from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import qrcode

app = Flask(__name__)

def generate_qr_code(data, box_size=10, border=4):
    """
    Generate a QR code image from the given data.

    Parameters:
    - data: The data to be encoded in the QR code.
    - box_size: The size of each QR code block.
    - border: The border size around the QR code.

    Returns:
    - An instance of a PIL (Pillow) image representing the QR code.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image

@app.route('/generate_id_card', methods=['POST'])
def generate_id_card():
    data = request.get_json()  # Assuming you're sending JSON data in the POST request

    # Extract the name from the JSON data
    name = data.get("name").upper()
    title = data.get("title").upper()
    kitd = data.get("kitd")
    games = data.get("games").upper()
    tier = data.get("tier").upper()
    color = data.get("color")
    zone = data.get("zone").upper()
    head = data.get("head").upper()

    # Load the ID card image
    card_image = Image.open("static/card_image/para_games.jpg")
    font = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-Bold.ttf", size=90)

    keys_to_encode = ["name", "title", "kitd"]

    qrcode_image = generate_qr_code(keys_to_encode)

    # Create a drawing context
    draw = ImageDraw.Draw(card_image)

    # Calculate the size of the text
    text_width_name, text_height_name = draw.textsize(name, font)
    card_width,card_height = card_image.size
    x_center_name = (card_width - text_width_name) // 2
    x_coordinate_name = x_center_name
    y_coordinate_name = 1500
    draw.text((x_coordinate_name, y_coordinate_name), name, fill=(0, 0, 0), font=font)

    text_width_title, text_height_title = draw.textsize(title,font)
    x_center_title = (card_width - text_width_title) // 2
    x_title = x_center_title
    y_title = 1550
    draw.text((x_title, y_title), title, fill=(0, 0, 0), font=font)

    text_width_games, text_height_games = draw.textsize(games, font)
    x_center_games = (card_width - text_width_games) // 2
    x_games = x_center_games
    y_games = 1600
    draw.text((x_games, y_games), games, fill=(0, 0, 0), font=font)

    x_tier = 17
    y_tier = 1650
    draw.text((x_tier, y_tier), tier, fill=(0, 0, 0), font=font)

    x_zone = 17
    y_zone = 1750
    draw.text((x_zone, y_zone), zone, fill=(0, 0, 0), font=font)

    text_width_head, text_height_head = draw.textsize(head, font)
    x_center_head = (card_width - text_width_head) // 2
    x_head = x_center_head
    y_head = 1750
    draw.text((x_head, y_head), head, fill=(0, 0, 0), font=font)

    x_qrcode = 78
    y_qrcode = 1000

    card_image.paste(qrcode_image, (x_qrcode, y_qrcode))

    card_image.show()

    ghghgh

    # Save the modified image with the name in the center (or specified coordinates)
    card_image.save("id_card_with_name.jpg")

    return jsonify({"message": "ID card generated successfully"})


if __name__ == '__main__':
    app.run(debug=True)