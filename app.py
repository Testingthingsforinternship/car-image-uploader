import streamlit as st
import os
from pathlib import Path
import pandas as pd

# Set upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
CSV_FILE = Path("canva_bulk_upload.csv")

# Title
st.title("Car Image Uploader")
st.write("Upload images for each car based on registration number. The app will also generate a Canva-compatible CSV.")

# Form for uploading images
with st.form("upload_form", clear_on_submit=True):
    reg_no = st.text_input("Car Registration Number").replace(" ", "_").upper()
    car_name = st.text_input("Car Name")

    arrival = st.file_uploader("Arrival Photo", type=["jpg", "jpeg", "png"], key="arrival")
    inspection = st.file_uploader("Inspection Photo", type=["jpg", "jpeg", "png"], key="inspection")
    servicing = st.file_uploader("Servicing Photo", type=["jpg", "jpeg", "png"], key="servicing")
    cleaning = st.file_uploader("Cleaning Photo", type=["jpg", "jpeg", "png"], key="cleaning")
    delivery = st.file_uploader("Delivery Photo", type=["jpg", "jpeg", "png"], key="delivery")

    submitted = st.form_submit_button("Upload")

    if submitted and reg_no:
        folder_path = UPLOAD_DIR / reg_no
        folder_path.mkdir(parents=True, exist_ok=True)

        uploads = {
            "arrival.jpg": arrival,
            "inspection.jpg": inspection,
            "servicing.jpg": servicing,
            "cleaning.jpg": cleaning,
            "delivery.jpg": delivery
        }

        filenames = {}

        for filename, file in uploads.items():
            if file is not None:
                filepath = folder_path / filename
                with open(filepath, "wb") as f:
                    f.write(file.read())
                filenames[filename] = f"{reg_no}/{filename}"
            else:
                filenames[filename] = ""

        # Update or create CSV
        row = {
            "Car Name": car_name,
            "Arrival": filenames["arrival.jpg"],
            "Inspection": filenames["inspection.jpg"],
            "Servicing": filenames["servicing.jpg"],
            "Cleaning": filenames["cleaning.jpg"],
            "Delivery": filenames["delivery.jpg"]
        }

        if CSV_FILE.exists():
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            df = pd.DataFrame([row])

        df.to_csv(CSV_FILE, index=False)

        st.success(f"Images uploaded for {reg_no} and CSV updated.")

# Download link
if CSV_FILE.exists():
    with open(CSV_FILE, "rb") as f:
        st.download_button("Download Canva CSV", f, file_name="canva_bulk_upload.csv")
