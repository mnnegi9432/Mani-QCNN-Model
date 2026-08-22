from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from werkzeug.utils import secure_filename

from predict import predict_image
from tumor_information import tumor_information
from generate_report import create_report

import os
import traceback


# ==========================================================
# Flask Configuration
# ==========================================================

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================================
# Helper Function
# ==========================================================

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_EXTENSIONS

    )


# ==========================================================
# Home Page
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# About Page
# ==========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ==========================================================
# Model Page
# ==========================================================

@app.route("/model")
def model():

    return render_template(
        "model.html"
    )


# ==========================================================
# Dataset Page
# ==========================================================

@app.route("/dataset")
def dataset():

    return render_template(
        "dataset.html"
    )


# ==========================================================
# Charts Page
# ==========================================================

@app.route("/charts")
def charts():

    return render_template(
        "charts.html"
    )


# ==========================================================
# Report Page
# ==========================================================

@app.route("/report")
def report():

    return render_template(
        "report.html"
    )
# ==========================================================
# Prediction Route
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        print("=" * 60)
        print("Prediction Request Received")

        # -----------------------------------------
        # Check Upload
        # -----------------------------------------

        if "image" not in request.files:
            return "No image uploaded."

        file = request.files["image"]

        if file.filename == "":
            return "No file selected."

        if not allowed_file(file.filename):
            return "Only PNG, JPG and JPEG images are allowed."

        # -----------------------------------------
        # Save Uploaded Image
        # -----------------------------------------

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        print("Saving image:", filepath)

        file.save(filepath)

        print("Image Saved Successfully")

        # -----------------------------------------
        # Prediction
        # -----------------------------------------

        prediction, confidence = predict_image(filepath)

        print("Prediction :", prediction)
        print("Confidence :", confidence)

        # -----------------------------------------
        # Tumor Information
        # -----------------------------------------

        info = tumor_information.get(
            prediction,
            {
                "features": [],
                "symptoms": [],
                "recommendation": "No recommendation available."
            }
        )

        # -----------------------------------------
        # Generate PDF Report
        # -----------------------------------------

        report_path = create_report(
            prediction=prediction,
            confidence=float(confidence),
            filename=filename,
            image_path=filepath,
            features=info["features"],
            symptoms=info["symptoms"],
            recommendation=info["recommendation"]
        )

        print("Report Generated :", report_path)

        # -----------------------------------------
        # Return Result Page
        # -----------------------------------------

        return render_template(
            "result.html",
            prediction=prediction,
            confidence=round(float(confidence), 2),
            image_path=filepath,
            features=info["features"],
            symptoms=info["symptoms"],
            recommendation=info["recommendation"]
        )

    except Exception as e:

        print("\nERROR OCCURRED\n")
        traceback.print_exc()

        return f"""
        <h2>Prediction Failed</h2>
        <pre>{e}</pre>
        """
    # ==========================================================
# Download Report
# ==========================================================

@app.route("/download-report")
def download_report():

    report_path = "static/reports/Brain_Tumor_Report.pdf"

    if os.path.exists(report_path):

        return send_file(
            report_path,
            as_attachment=True
        )

    return "Report not found."


# ==========================================================
# Download Dataset (Optional)
# ==========================================================

@app.route("/download-dataset")
def download_dataset():

    dataset_zip = "static/dataset/Brain_Tumor_Dataset.zip"

    if os.path.exists(dataset_zip):

        return send_file(
            dataset_zip,
            as_attachment=True
        )

    return "Dataset not found."


# ==========================================================
# Download Architecture Image (Optional)
# ==========================================================

@app.route("/download-architecture")
def download_architecture():

    architecture = "static/architecture/framework_ieee_compact.png"

    if os.path.exists(architecture):

        return send_file(
            architecture,
            as_attachment=True
        )

    return "Architecture image not found."
# ==========================================================
# Health Check (Optional)
# ==========================================================

@app.route("/health")
def health():

    return {
        "status": "Running",
        "application": "Hybrid QCNN Brain Tumor Detection System"
    }


# ==========================================================
# Run Flask Application
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Hybrid QCNN Brain Tumor Detection System")
    print("Developed by Manish Negi")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )