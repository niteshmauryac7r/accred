from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import qrcode

app = Flask(__name__)

def generate_qr_code(data):
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
        box_size=10,
        border=0,
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
    profilepicture = data.get("picture")
    food = data.get("food")

    # Load the ID card image
    card_image = Image.open("static/card_image/para_games.jpg")
    font_name = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-Medium.ttf", size=90)
    font_title = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-Medium.ttf", size=90)
    font_games = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-Medium.ttf", size=90)
    font_tier = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-ExtraBold.ttf", size=90)
    font_zone = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-ExtraBold.ttf", size=90)
    font_head = ImageFont.truetype("static/Saira_Condensed/SairaCondensed-Bold.ttf", size=90)

    keys_to_encode = ["name", "title", "kitd"]

    qrcode_image = generate_qr_code(keys_to_encode)

    # Create a drawing context
    draw = ImageDraw.Draw(card_image)

    # Calculate the size of the text
    text_width_name, text_height_name = draw.textsize(name, font_name)
    card_width,card_height = card_image.size
    x_center_name = (card_width - text_width_name) // 2
    x_coordinate_name = x_center_name
    y_coordinate_name = 1400
    draw.text((x_coordinate_name, y_coordinate_name), name, fill=(245, 149, 29), font=font_name)

    text_width_title, text_height_title = draw.textsize(title, font_title)
    x_center_title = (card_width - text_width_title) // 2
    x_title = x_center_title
    y_title = 1500
    draw.text((x_title, y_title), title, fill=(0, 0, 0), font=font_title)

    text_width_games, text_height_games = draw.textsize(games, font_games)
    x_center_games = (card_width - text_width_games) // 2
    x_games = x_center_games
    y_games = 1600
    draw.text((x_games, y_games), games, fill=(255, 255, 255), font=font_games)

    x_tier = 800
    y_tier = 2100
    draw.text((x_tier, y_tier), tier, fill=(255, 255, 255), font=font_tier)

    x_zone = 17
    y_zone = 1750
    draw.text((x_zone, y_zone), zone, fill=(255, 255, 255), font=font_zone)

    x_qrcode = 69
    y_qrcode = 1947
    qr_width = 350
    qr_height = 350

    qrcode_image = qrcode_image.resize((qr_width, qr_height))

    # Decode the Base64 string into an image
    profile_picture_data = base64.b64decode(profilepicture)
    profile_picture = Image.open(BytesIO(profile_picture_data))

    # Define the coordinates for pasting the profile picture
    x_profile_picture = 400
    y_profile_picture = 707
    profile_picture_width = 537
    profile_picture_height = 650

    profile_picture = profile_picture.resize((profile_picture_width, profile_picture_height))

    card_image.paste(profile_picture, (x_profile_picture, y_profile_picture))

    x_rectangle = 0  # X-coordinate of the top-left corner of the rectangle
    y_rectangle = 2360  # Y-coordinate of the top-left corner of the rectangle
    width_rectangle = 1350  # Width of the rectangle
    height_rectangle = 200  # Height of the rectangle

    # Draw a filled rectangle with the received color
    draw.rectangle(
        [x_rectangle, y_rectangle, x_rectangle + width_rectangle, y_rectangle + height_rectangle],
        fill=color,
    )

    text_width_head, text_height_head = draw.textsize(head, font_head)
    x_center_head = (card_width - text_width_head) // 2
    x_head = x_center_head
    y_head = 2360
    draw.text((x_head, y_head), head, fill=(255, 255, 255), font=font_head)

    # Decode the Base64 string into an image
    food_data = base64.b64decode(food)
    food = Image.open(BytesIO(food_data))

    # Define the coordinates for pasting the profile picture
    x_food = 510
    y_food = 2140
    food_width = 160
    food_height = 120

    food = food.resize((food_width, food_height))

    # Paste the profile picture onto the ID card image
    card_image.paste(food, (x_food, y_food))

    card_image.paste(qrcode_image, (x_qrcode, y_qrcode))

    card_image.show()



    # Save the modified image with the name in the center (or specified coordinates)
    card_image.save("id_card_with_name.jpg")

    return jsonify({"message": "ID card generated successfully"})


if __name__ == '__main__':
    app.run(debug=True)