
from flask import Flask, redirect, jsonify, render_template, request
from werkzeug.utils import secure_filename

from PIL import Image
import base64
from io import BytesIO


from model import (
    get_tensor_image_from_buf, classify_tensor_image,
    unpack_top_pred_name_score
)


allowed_exts = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}


DEFAULT_STATUS_MSG = "Upload an image to receive a classification"

DEFAULT_IMG = 'https://y.yarn.co/576daf10-927e-4d48-b257-04886400c7d2_text.gif'

DEFAULT_PRED_NAME = ''  #'dog'
DEFAULT_PRED_SCORE = ''  #100



application = Flask(__name__)


def is_json_request(request):
    if len(request.form) == 0:
        return True
    return False



def check_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


"""
def unpack_json():
    #json_payload = request.json
    tensor_image = get_tensor_image()
    return tensor_image

def unpack_form():
    #day = request.form.get("day")
    #total = request.form.get("total")
    tensor_image = get_tensor_image()
    return tensor_image
"""



@application.route("/",methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return render_template(
            'index.html',
            status_msg=DEFAULT_STATUS_MSG,
            pred_name=DEFAULT_PRED_NAME, pred_score=DEFAULT_PRED_SCORE,
            img_data=DEFAULT_IMG
        ), 200
    

    # POST
    if 'file' not in request.files:
        print('No file attached in request')
        return render_template(
            'index.html',
            status_msg="[!] File not attached in request",
            pred_name=DEFAULT_PRED_NAME, pred_score=DEFAULT_PRED_SCORE,
            img_data=DEFAULT_IMG
        ), 200

    file = request.files['file']
    if file.filename == '':
        print('No file selected')
        return render_template(
            'index.html',
            status_msg="[!] No file selected",
            pred_name=DEFAULT_PRED_NAME, pred_score=DEFAULT_PRED_SCORE,
            img_data=DEFAULT_IMG
        ), 200


    if check_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('filename:', filename)

        img = Image.open(file.stream)

        with BytesIO() as buf:
            img.save(buf, 'jpeg')
            image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()       

            tensor_image = get_tensor_image_from_buf(image_bytes)

        pred = classify_tensor_image(tensor_image)
        print(pred)
        pred_name, pred_score = unpack_top_pred_name_score(pred)

        pred_name = f"Prediction Class: {pred_name}"
        pred_score = f"Prediction Score: {pred_score}"

        img_data = f"data:image/jpeg;base64,{encoded_string}"
        return render_template(
            'index.html',
            status_msg=f"Successfully uploaded: `{filename}`",
            pred_name=pred_name, pred_score=pred_score,
            img_data=img_data
        ), 200
    
    print('Not allowed file:', file.filename)
    return redirect(request.url)
	


"""
@application.route("/")
def home():
    return render_template("index.html", img_data="")

@application.route("/predict", methods=["POST"])
def predict():

    prediction_text = 'hello testing'
    img_data = ""

    if is_json_request(request):
        return jsonify({"prediction": prediction_text})
    else:
        return render_template(
            "index.html",
            prediction_text=prediction_text,
            img_data=img_data
        )
"""


"""
@application.route("/predict", methods=["POST"])
def predict():
    if is_json_request(request):
        model_inputs = unpack_json()
    else:
        model_inputs = unpack_form()
    
    prediction_result = classify(model_inputs)
    prediction_text = unpack_top_pred_pretty_text(prediction_result)

    if is_json_request(request):
        return jsonify({"prediction": prediction_text})
    else:
        return render_template("index.html", prediction_text=prediction_text)
"""

if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8080, debug=True)
