import base64
from io import BytesIO

from flask import Flask, jsonify, redirect, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename

from .model import (
    classify_tensor_image,
    get_model_metadata,
    get_tensor_image_from_buf,
    unpack_top_pred_name_score,
)

allowed_exts = {"jpg", "jpeg", "png", "JPG", "JPEG", "PNG"}


DEFAULT_STATUS_MSG = "Upload an image to receive a classification"

DEFAULT_IMG = "https://y.yarn.co/576daf10-927e-4d48-b257-04886400c7d2_text.gif"

DEFAULT_PRED_NAME = ""  # 'dog'
DEFAULT_PRED_SCORE = ""  # 100


application = Flask(__name__)


def is_json_request(request):
    if len(request.form) == 0:
        return True
    return False


def check_allowed_file(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    return "." in filename and ext in allowed_exts


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        return (
            render_template(
                "index.html",
                status_msg=DEFAULT_STATUS_MSG,
                pred_name=DEFAULT_PRED_NAME,
                pred_score=DEFAULT_PRED_SCORE,
                img_data=DEFAULT_IMG,
            ),
            200,
        )

    # POST
    if "file" not in request.files:
        print("No file attached in request")
        return (
            render_template(
                "index.html",
                status_msg="[!] File not attached in request",
                pred_name=DEFAULT_PRED_NAME,
                pred_score=DEFAULT_PRED_SCORE,
                img_data=DEFAULT_IMG,
            ),
            200,
        )

    file = request.files["file"]
    if file.filename == "":
        print("No file selected")
        return (
            render_template(
                "index.html",
                status_msg="[!] No file selected",
                pred_name=DEFAULT_PRED_NAME,
                pred_score=DEFAULT_PRED_SCORE,
                img_data=DEFAULT_IMG,
            ),
            200,
        )

    if check_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("filename:", filename)

        img = Image.open(file.stream)

        with BytesIO() as buf:
            img.save(buf, "jpeg")
            image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()

        tensor_image = get_tensor_image_from_buf(image_bytes)
        pred = classify_tensor_image(tensor_image)
        print(pred)
        pred_name, pred_score = unpack_top_pred_name_score(pred)

        pred_name = f"Prediction Class: {pred_name}"
        pred_score = f"Prediction Score: {pred_score}"

        img_data = f"data:image/jpeg;base64,{encoded_string}"

        if len(filename) > 18:
            filename = f"...{filename[-18:]}"
        return (
            render_template(
                "index.html",
                status_msg=f"Successfully uploaded: `{filename}`",
                pred_name=pred_name,
                pred_score=pred_score,
                img_data=img_data,
            ),
            200,
        )

    print("Not allowed file:", file.filename)
    return redirect(request.url)


@application.route("/predict", methods=["POST"])
def predict():
    result_dict = {}
    if not request.json or "image_b64" not in request.json:
        result_dict["result"] = "Error processing request"
        return result_dict

    im_b64 = request.json["image_b64"]

    # convert it into bytes
    image_bytes = base64.b64decode(im_b64.encode("utf-8"))
    tensor_image = get_tensor_image_from_buf(image_bytes)
    pred = classify_tensor_image(tensor_image)

    return pred


@application.route("/metadata", methods=["GET"])
def metadata():
    metadata_dict = get_model_metadata()
    return jsonify(metadata_dict)
