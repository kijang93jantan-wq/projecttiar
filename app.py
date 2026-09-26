import streamlit as st
from google import genai
from google.genai import types

# ── 1. Konfigurasi Halaman ───────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopBot - Asisten Online Shop",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ ShopBot - Asisten Belanja Online")
st.caption("Chatbot Asisten Toko Online untuk Pencarian Produk & Informasi Stok")

# ── 2. Sidebar: Pengaturan & Konfigurasi ─────────────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password")
    
    gaya_bahasa = st.selectbox(
        "Gaya Bahasa Bot:",
        ("Ramah & Ceria", "Sopan & Formal", "Casual / Santai")
    )
    
    reset_button = st.button("Reset Percakapan", help="Hapus semua riwayat chat")

# ── 3. Validasi API Key ──────────────────────────────────────────────────────
if not google_api_key:
    st.info("Silakan masukkan Google AI API Key di sidebar untuk mulai menggunakan ShopBot.", icon="🗝️")
    st.stop()

# ── 4. Pengetahuan Toko & Katalog Produk (Knowledge Base) ───────────────────
KATALOG_TOKO = """
Nama Toko: ElectroZone Official Store
Platform: Online Shop Electronics & Gadgets
Jam Operasional CS: 08.00 - 21.00 WIB
Kebijakan Garansi: Semua produk bergaransi resmi 1 tahun. Gratis ongkir seluruh Indonesia minimal belanja Rp 100.000.

Daftar Katalog Produk & Stok:
1. Laptop UltraBook Pro 14
   - Harga: Rp 12.500.000
   - Spesifikasi: Intel i7 Gen 13, RAM 16GB, SSD 512GB, Layar 14 inch OLED
   - Stok: 5 unit

2. Smartphone X-Pro 5G
   - Harga: Rp 7.999.000
   - Spesifikasi: Kamera 108MP, Baterai 5000mAh, RAM 8GB, Storage 256GB
   - Stok: 12 unit

3. Wireless Earbuds Noise-Cancelling
   - Harga: Rp 899.000
   - Spesifikasi: Bluetooth 5.3, Active Noise Cancelling, Baterai tahan 24 jam
   - Stok: 20 unit

4. Smartwatch FitTrack 2
   - Harga: Rp 1.250.000
   - Spesifikasi: Sensor Detak Jantung, GPS, Waterproof IP68, Baterai 7 hari
   - Stok: 8 unit

5. Keyboard Mekanik Wireless RGB
   - Harga: Rp 650.000
   - Spesifikasi: Hot-swappable, Bluetooth/2.4Ghz, Battery 3000mAh
   - Stok: 15 unit
"""

system_instruction = f"""
Kamu adalah "ShopBot", Asisten Penjualan Virtual yang sangat ramah dan responsif untuk toko online "ElectroZone".
Tugas kamu:
1. Membantu pembeli mencari produk yang sesuai kebutuhan mereka berdasarkan data katalog berikut.
2. Memberikan informasi harga, spesifikasi singkat, dan status ketersediaan stok.
3. Memberikan rekomendasi produk jika pembeli bingung memilih.

Gunakan data katalog berikut sebagai acuan utama:
{KATALOG_TOKO}

Aturan:
- Gunakan gaya bahasa: {gaya_bahasa}.
- Selalu sebutkan harga dan stok barang jika ditanyakan oleh calon pembeli.
- Jika pembeli menanyakan produk di luar katalog di atas, jawab dengan sopan bahwa produk tersebut belum tersedia di toko ElectroZone.
"""

# ── 5. Inisialisasi Gemini Client & Chat Session ────────────────────────────
if ("genai_client" not in st.session_state) or (
    getattr(st.session_state, "_last_key", None) != google_api_key
):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"API Key tidak valid: {e}")
        st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo Kak! 👋 Selamat datang di ElectroZone! Lagi cari gadget apa hari ini?"}
    ]

# ── 6. Tombol Reset ──────────────────────────────────────────────────────────
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ── 7. Tampilkan Riwayat Percakapan ─────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 8. Input & Respons Chatbot ──────────────────────────────────────────────
prompt = st.chat_input("Tanya produk, stok, atau rekomendasi barang...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = st.session_state.chat.send_message(prompt)
        answer = response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        answer = f"Maaf Kak, terjadi kendala sistem: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
