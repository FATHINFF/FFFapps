import streamlit as st
from login_page import login
import numpy as np
from PIL import Image
import io
import json
import os
import pandas as pd
from tensorflow.keras.models import load_model

# Load model CNN dengan caching
@st.cache_resource
def load_cnn_model():
    return load_model('Saving_ModelCnn.h5')

model = load_cnn_model()

DATA_FILE = "data_pasien.json"

# Fungsi untuk membaca data pasien dari JSON
def load_patients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Fungsi untuk menyimpan data pasien ke JSON
def save_patients(patients):
    with open(DATA_FILE, "w") as file:
        json.dump(patients, file, indent=4)

# Fungsi untuk menghapus data pasien berdasarkan indeks
def delete_patient(index):
    patients = load_patients()
    if 0 <= index < len(patients):
        del patients[index]
        save_patients(patients)
        st.success("Data berhasil dihapus!")
        st.experimental_rerun()  # Refresh halaman setelah hapus

# Fungsi untuk memuat dan memproses gambar MRI
def load_uploaded_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    return img_array

# Fungsi untuk melakukan prediksi tumor
def predict_image(image_bytes):
    img_array = load_uploaded_image(image_bytes)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    confidence = prediction[0][0]
    return confidence

# Halaman tutorial penggunaan aplikasi
def show_tutorial():
    st.header("Tutorial Menggunakan Aplikasi")
    st.write("""
        - **Brain Tumor Detection**
        - **Deteksi Ini Hanya Digunakan untuk Gambar MRI**
        - **Akurasi Testing Dalam Program Ini 98%**
        - **Hasil Output Dalam Program Kali Ini Ada 2, yaitu Tumor dan Non-Tumor**
    """)

def show_cek_tumor():
    st.header("Cek Tumor")
    st.write("Masukkan nama pasien dan unggah gambar MRI.")

    patient_name = st.text_input("Nama Pasien")
    uploaded_image = st.file_uploader("Unggah Gambar MRI", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None and patient_name:
        if st.button("Cek Hasil"):  # Tombol buat nge-trigger prediksi & penyimpanan
            confidence = predict_image(uploaded_image.read())
            if confidence > 0.5:
                result = "Tumor detected"
                probability = confidence * 100
            else:
                result = "No tumor detected"
                probability = (1 - confidence) * 100

            st.success(result)  
            st.image(uploaded_image, caption="Gambar MRI yang Diupload", use_column_width=True)  # Baru gambar

            # Simpan data pasien ke JSON setelah tombol ditekan
            patients = load_patients()
            patients.append({
                'name': patient_name,
                'result': result,
                'confidence': probability
            })
            save_patients(patients)

def show_hasil_cek_tumor():

    st.header("Hasil Cek Tumor Otak")
    patients = load_patients()

    if len(patients) > 0:
        data = {
            "Nama Pasien": [p['name'] for p in patients],
            "Prediksi": [p['result'] for p in patients],
            "Probabilitas Tumor (%)": [f"{p['confidence']:.2f}%" for p in patients],
            "Probabilitas Non-Tumor (%)": [f"{(100 - p['confidence']):.2f}%" for p in patients]
        }
        
        st.table(data)

        patient_names = [p['name'] for p in patients]
        selected_patient = st.selectbox("Pilih pasien yang ingin dihapus:", patient_names)

        if st.button("Hapus Pasien"):
            patients = [p for p in patients if p['name'] != selected_patient]
            save_patients(patients)
            st.success(f"Data pasien {selected_patient} berhasil dihapus!")
            st.rerun() 

    else:
        st.write("Belum ada hasil cek tumor.")


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if login():
        st.session_state.logged_in = True
        st.rerun()

if st.session_state.logged_in:
    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Pilih Menu", ("Tutorial", "Cek Tumor", "Hasil Cek Tumor Otak"))

    if menu == "Tutorial":
        show_tutorial()
    elif menu == "Cek Tumor":
        show_cek_tumor()
    elif menu == "Hasil Cek Tumor Otak":
        show_hasil_cek_tumor()

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.success("Anda telah logout.")
        st.rerun()
