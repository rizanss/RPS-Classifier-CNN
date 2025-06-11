import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Muat model yang sudah kita latih
model = load_model('models/rps_cnn_model.h5')

# Buka webcam
cap = cv2.VideoCapture(2)

# Definisikan label kelas
class_labels = ['KERTAS', 'BATU', 'GUNTING']

while True:
    # Ambil frame dari webcam
    ret, frame = cap.read()
    if not ret:
        break

    # -- Bagian Preprocessing Real-Time --
    # Kita harus membuat frame dari webcam sama persis seperti data training

    # Resize frame menjadi 150x150 piksel
    resized_frame = cv2.resize(frame, (150, 150))
    
    # Normalisasi nilai piksel (0-1)
    normalized_frame = resized_frame / 255.0
    
    # Tambah dimensi batch (model mengharapkan input bentuk (1, 150, 150, 3))
    input_frame = np.expand_dims(normalized_frame, axis=0)

    # -- Lakukan Prediksi --
    prediction = model.predict(input_frame)
    
    # Ambil indeks kelas dengan probabilitas tertinggi
    predicted_class_index = np.argmax(prediction)
    
    # Ambil nama labelnya
    predicted_class_label = class_labels[predicted_class_index]
    
    # Ambil nilai confidence (probabilitas)
    confidence = prediction[0][predicted_class_index] * 100

    # -- Tampilkan Hasil di Layar --
    # Tampilkan teks prediksi di frame
    text = f'{predicted_class_label} ({confidence:.2f}%)'
    cv2.putText(
        frame,                          # Frame yang mau digambar
        text,                           # Teks yang mau ditampilkan
        (20, 40),                       # Posisi teks (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,       # Jenis font
        1,                              # Ukuran font
        (0, 255, 0),                    # Warna font (hijau)
        2                               # Ketebalan font
    )

    # Tampilkan frame yang sudah ada teksnya
    cv2.imshow('Real-Time Rock-Paper-Scissors Classifier', frame)

    # Hentikan loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan webcam dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()