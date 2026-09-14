import streamlit as st
import requests
import re
import time

# --- SISTEM KEAMANAN (PASSWORD DARI SOCIABUZZ) ---
PASSWORD_RAHASIA = "AKSESPRO2026"

def check_password():
    if "password_benar" not in st.session_state:
        st.session_state["password_benar"] = False

    if not st.session_state["password_benar"]:
        st.title("🔒 Portal AI Bisnis")
        masukan = st.text_input("Masukkan Password Akses:", type="password")
        if st.button("Masuk"):
            if masukan == PASSWORD_RAHASIA:
                st.session_state["password_benar"] = True
                st.rerun()
            else:
                st.error("Password salah! Silakan periksa kembali.")
        return False
    return True

def generate_iklan_global(api_key, nama_produk, deskripsi_lokal, negara_tujuan, keunggulan, target_konsumen, harga, gaya_bahasa):
    # Menggunakan model Gemini terbaru
    nama_mesin = "models/gemini-3.5-flash"
    
    prompt = f"""
    Kamu adalah Copywriter Internasional, Pakar Ekspor, dan Spesialis Digital Marketing Global.
    Tugasmu menyulap produk UMKM Indonesia menjadi copywriting profesional berstandar internasional yang siap pakai untuk Website, TikTok, Instagram, Meta Ads, atau Marketplace Global.
    
    Data Produk:
    - Nama Produk: {nama_produk}
    - Deskripsi Asli: {deskripsi_lokal}
    - Keunggulan Utama / USP: {keunggulan if keunggulan else '-'}
    - Target Konsumen: {target_konsumen if target_konsumen else '-'}
    - Harga Produk: {harga if harga else '-'}
    - Gaya Bahasa yang Diinginkan: {gaya_bahasa if gaya_bahasa else '-'}
    - Target Market: Negara {negara_tujuan}
    
    ATURAN KETAT:
    1. Tulis seluruh hasil akhir menggunakan bahasa resmi negara target (misal: Jepang -> Bahasa Jepang, AS -> Inggris, dst). 
    2. Gunakan formula AIDA (Attention, Interest, Desire, Action) yang dirancang khusus untuk psikologi konsumen di negara tersebut.
    3. Manfaatkan Keunggulan Utama, Target Konsumen, dan Harga (jika diisi) untuk membuat copy lebih personal dan meyakinkan.
    4. Sesuaikan gaya bahasa dengan preferensi yang diberikan (jika diisi), tetap natural sesuai kultur negara target.
    5. Buat tanpa simbol bintang/markdown agar bersih saat di-copy.
    
    FORMAT WAJIB:
    
    [Tulis Bendera Negara Target] COPYWRITING GLOBAL ({negara_tujuan})
    
    HEADLINE:
    (Buat 1 kalimat hook yang sangat memikat untuk menarik perhatian audiens)
    
    BODY COPY:
    (Paragraf persuasif yang memicu rasa penasaran dan keinginan kuat untuk membeli produk lokal ini)
    
    CALL TO ACTION:
    (Kalimat ajakan bertindak / membeli yang mendesak)
    
    ---
    SEO & TARGETING METADATA:
    - TARGET AUDIENCE / INTEREST: (Sebutkan 3 target audiens atau interest spesifik untuk periklanan digital di negara tersebut)
    - KATA KUNCI E-COMMERCE / WEBSITE: (5 keyword pencarian lokal di negara tersebut)
    - HASHTAG: (7 hashtag viral di negara tersebut terkait produk ini)
    """

    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/{nama_mesin}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url_gemini, json=payload, headers={'Content-Type': 'application/json'}, timeout=90)
        data = response.json()
        
        if 'error' in data:
            return None, f"Error API: {data['error']['message']}"
            
        hasil_ai = data['candidates'][0]['content']['parts'][0]['text']
        return hasil_ai.replace('*', ''), None
        
    except Exception as e:
        return None, f"Gagal menghubungi server AI. Pastikan internet aktif. Error: {e}"

def buat_nama_file_aman(nama_produk, negara):
    clean_produk = re.sub(r'[^a-zA-Z0-9]', '_', nama_produk)
    clean_negara = re.sub(r'[^a-zA-Z0-9]', '_', negara)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"Copywriting_{clean_produk}_{clean_negara}_{timestamp}.txt"

# --- JALANKAN APLIKASI WEB JIKA PASSWORD BENAR ---
if check_password():
    # 1. TAMPILAN SIDEBAR
    st.sidebar.title("⚙️ Pengaturan Akses")
    
    st.sidebar.markdown("**Langkah 1:** Dapatkan Kunci API (Gratis)")
    st.sidebar.markdown("[Klik di sini untuk buat API Key (Google AI Studio)](https://aistudio.google.com/app/apikey)")
    
    st.sidebar.markdown("**Langkah 2:** Masukkan Kunci API Anda di bawah ini:")
    api_key_pelanggan = st.sidebar.text_input(
        "API Key Gemini:", 
        type="password", 
        help="Paste API Key Anda di sini"
    )
    
    if api_key_pelanggan:
        st.session_state["API_KEY"] = api_key_pelanggan

    st.sidebar.markdown("---")
    st.sidebar.info("Data 100% aman dan menggunakan server Google secara langsung.")

    # 2. TAMPILAN UTAMA
    if "API_KEY" not in st.session_state or st.session_state["API_KEY"] == "":
        st.warning("⚠️ Silakan masukkan API Key Gemini Anda di menu samping (sidebar) terlebih dahulu.")
        
    else:
        st.title("🌍 Bot Ekspor UMKM - Global Copywriter AI")
        st.write("Ubah deskripsi lokal jadi konten & iklan internasional dalam hitungan detik.")
        
        with st.form("form_copywriter"):
            col1, col2 = st.columns(2)
            
            with col1:
                nama = st.text_input("1. Nama Produk *", placeholder="contoh: Keripik Tempe, Tas Rotan")
                deskripsi = st.text_area("2. Deskripsi Singkat/Bahan *", placeholder="contoh: Dibuat dari rotan asli Bali, tahan lama")
                negara = st.text_input("3. Negara Target *", placeholder="contoh: Jepang, Amerika Serikat, Arab Saudi")
                
            with col2:
                keunggulan = st.text_input("4. Keunggulan Utama (Opsional)", placeholder="contoh: Handmade, tahan air")
                target_konsumen = st.text_input("5. Target Konsumen (Opsional)", placeholder="contoh: Wanita 25-40 tahun")
                harga = st.text_input("6. Harga Produk (Opsional)", placeholder="contoh: Rp150.000 / $15")
                gaya_bahasa = st.text_input("7. Gaya Bahasa (Opsional)", placeholder="contoh: elegan, mendesak/urgent")
                
            st.markdown("*Wajib diisi")
            submitted = st.form_submit_button("Generate Copywriting Global")

        if submitted:
            if nama and deskripsi and negara:
                with st.spinner(f"Menghubungkan ke server global... Menganalisis kultur {negara}..."):
                    hasil_copywriting, error = generate_iklan_global(
                        st.session_state["API_KEY"], 
                        nama, deskripsi, negara, keunggulan, target_konsumen, harga, gaya_bahasa
                    )
                    
                    if error:
                        st.error(f"[GAGAL] {error}")
                    else:
                        st.success("Copywriting Selesai!")
                        st.markdown("---")
                        
                        # Tampilkan hasil di layar
                        st.text_area("Hasil Copywriting:", value=hasil_copywriting, height=400)
                        
                        # Tombol Download File .txt (menggantikan sistem save otomatis sebelumnya)
                        nama_file = buat_nama_file_aman(nama, negara)
                        st.download_button(
                            label="📥 Download Teks (.txt)",
                            data=hasil_copywriting,
                            file_name=nama_file,
                            mime="text/plain"
                        )
            else:
                st.warning("Harap isi Nama Produk, Deskripsi Singkat, dan Negara Target terlebih dahulu!")