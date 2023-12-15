from flask import Flask, request, jsonify
from ParseXml import extract_steps_from_xml
from PIL import Image
import os
import cv2
import numpy as np
import base64
import requests

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        equation = data['equation']

        equation_query = equation

        app_id = 'HWRQK4-8L96HA9XVT'

        external_api_url = f'http://api.wolframalpha.com/v2/query?appid={app_id}&input=solve+{equation_query}&podstate=Result__Step-by-step+solution&format=plaintext'

        response = requests.get(external_api_url)

        if response.status_code == 200:
            result = extract_steps_from_xml(response.content)
        else:
            return jsonify({'error': f"Failed to make API call. Status code: {response.status_code}"})

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/generateEquation', methods=['POST'])
def generateEquation():
    try:
        image_file = request.files['image']

        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, image_file.filename)
        image_file.save(image_path)

        img = cv2.imread(os.path.join(upload_folder, image_file.filename))
        # Convert the processed image to bytes
        # _, buffer = cv2.imencode('.jpg', img)
        # img_bytes = buffer.tobytes()

        # if img is None:
        #     return jsonify({'error': 'Unable to read the image'}), 400
        # Return the processed image as base64
        # img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # return jsonify({'image': img_base64})


        return jsonify({'result': "3x-7=2"})

    except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, send_file
#
# app = Flask(__name__)
#
# def generate_image():
#     """
#     Generate a placeholder image (solid color) and save it to a file.
#
#     Returns:
#     - str: The filename of the generated image.
#     """
#     # Placeholder: Create an image (e.g., solid blue)
#     # In a real scenario, you might generate or retrieve an actual image
#     image_filename = "placeholder_image.png"
#     # This code uses the Pillow library to create a simple blue image
#     from PIL import Image
#     img = Image.new('RGB', (300, 300), color='blue')
#     img.save(image_filename)
#     return image_filename
#
# @app.route('/get_image', methods=['GET'])
# def get_image():
#     try:
#         # Generate the image
#         image_filename = generate_image()
#
#         # Send the image file in the response without treating it as an attachment
#         return send_file(image_filename, mimetype='image/png')
#
#     except Exception as e:
#         return jsonify({'error': str(e)})
#
# if __name__ == '__main__':
#     app.run(debug=True)
