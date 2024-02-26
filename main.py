from flask import Flask, request, jsonify, Response
from ParseXml import extract_steps_from_xml
from CheckEquationType import getEquationType
from LinearEquation import solveLinearEquation
from ImageSegmentation import LineSegmentation, CharacterSegmentation
from PolynomialEquation import solvePolynomialEquation
from Utils import resize_pad
from model import predict_image
from PIL import Image
from matplotlib import pyplot as plt
from flask_cors import CORS
import os
import cv2
import numpy as np
import base64
import requests


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()

        equations = data['equation']

        finalEquationType = 0

        for equation in equations:
                equationType = getEquationType(equation)
                if(equationType == 0):
                    finalEquationType = 0
                elif(equationType > finalEquationType):
                    finalEquationType = equationType
        toPrint = ''
        if(finalEquationType == 1):
            result = solveLinearEquation(equations)
            print("result received")

            for values in result:
                toPrint = toPrint + values
        elif(finalEquationType == 2):
            result = solvePolynomialEquation(equations[0])
            toPrint = "The root is " + str(result)
        elif(finalEquationType == 3):
            equation = equations[0].replace('x', '*')
            print(equations)
            print(equation)
            result = eval(equation)
            toPrint = str(result)
        else:
            print(finalEquationType)
            print("error")
            # raise Exception()

        return jsonify({'result': toPrint})

    except Exception as e:
        app_id = 'HWRQK4-8L96HA9XVT'
        return jsonify({'error' : str(e)})

        # external_api_url = f'http://api.wolframalpha.com/v2/query?appid={app_id}&input=solve+{equations[0]}&podstate=Result__Step-by-step+solution&format=plaintext'
        #
        # response = requests.get(external_api_url)
        # print(f"api called {response.content}")
        #
        # if response.status_code == 200:
        #     return jsonify({'result' : extract_steps_from_xml(response.content)})
        # else:
        #     return jsonify({'error': f"Failed to make API call. Status code: {response.status_code}"})



@app.route('/generateEquation', methods=['POST'])
def generateEquation():
    try:
        #load image
        image_file = request.files['image']

        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, image_file.filename)
        image_file.save(image_path) #save the loaded image to upload directory

        img = cv2.imread(os.path.join(upload_folder, image_file.filename), cv2.IMREAD_GRAYSCALE)

        #perform thresholding
        thresholded_image = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51,
                                                  30)
        img = Image.fromarray(thresholded_image)
        print("reached before calling line seg")
        img.save(image_path) #save the thresholded image to the same directory

        saved_image = cv2.imread(os.path.join(upload_folder, image_file.filename))

        line_seg = LineSegmentation(saved_image)

        print(line_seg)

        equation_list = []

        for (x, y, w, h) in sorted(line_seg, key=lambda x: x[0]):
            single_equation_image = saved_image[y:y+h, x:x+w]
            temp_keep = CharacterSegmentation(saved_image, x, y, w, h)
            print(f"temp keep: {temp_keep}")
            equation = ''
            for (x, y, w, h) in sorted(temp_keep, key=lambda x: x[0]):
                single_character_image = single_equation_image[y:y + h, x:x + w]
                padded_img = resize_pad(single_character_image, (45, 45))
                predicted_character = predict_image(padded_img)
                equation = equation + predicted_character

            equation_list.append(equation)
            equation_list.reverse()

        return jsonify({'result': equation_list})

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
