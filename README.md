# 🤖 Gemini AI Chatbot

Aplikasi chatbot interaktif berbasis Artificial Intelligence yang dibangun menggunakan **Google Gemini API** dan framework **Streamlit**. Proyek ini dibuat sebagai syarat pengumpulan *Final Project* pelatihan Data Science & AI.

---

## 📌 Fitur Utama
- **Interaktif & Responsif**: Menggunakan komponen UI bawaan Streamlit (`st.chat_message` & `st.chat_input`).
- **Memory/Context Session**: Mengingat riwayat percakapan sebelumnya menggunakan `st.session_state`.
- **Dukungan API Key**: Pengguna dapat memasukkan Google AI API Key secara aman melalui panel *sidebar*.
- **Fitur Reset**: Memungkinkan pengguna mereset percakapan dan memulai sesi chat baru.

---

## 🛠️ Teknologi yang Digunakan
- **Bahasa Pemrograman**: Python
- **UI Framework**: Streamlit
- **LLM SDK**: `google-genai` (Model: `gemini-2.5-flash`)
- **Deployment / Tunneling**: `pyngrok` (Google Colab Integration)

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. **Clone Repositori Ini**
   ```bash
   git clone [https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git](https://github.com/USERNAME_KAMU/NAMA_REPO_KAMU.git)
   cd NAMA_REPO_KAMU
