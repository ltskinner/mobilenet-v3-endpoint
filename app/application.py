
from flask import Flask, jsonify, render_template, request

from model import get_tensor_image, classify, unpack_top_pred_pretty_text


application = Flask(__name__)



def unpack_json():
    #json_payload = request.json
    tensor_image = get_tensor_image()
    return tensor_image

def unpack_form():
    #day = request.form.get("day")
    #total = request.form.get("total")
    tensor_image = get_tensor_image()
    return tensor_image

def is_json_request():
    if len(request.form) == 0:
        return True
    return False



@application.route("/")
def home():
    return render_template("index.html")


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


if __name__ == "__main__":
    application.run(host="127.0.0.1", port=8080, debug=True)
