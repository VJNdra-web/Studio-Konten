import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="ContentOS - Creator AI Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESAIN TAMPILAN (CSS KUSTOM) ---
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'blueprint' not in st.session_state:
    st.session_state.blueprint = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #818cf8;'>🚀 Selamat Datang di ContentOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Platform AI All-in-One untuk Kreator Konten</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("Login / Masuk")
            email_input = st.text_input("Email")
            password_input = st.text_input("Password", type="password")
            api_key_input = st.text_input("Masukkan Google Gemini API Key Anda", type="password", help="Dapatkan gratis di Google AI Studio")
            submit_login = st.form_submit_button("Masuk ke Dashboard")
            
            if submit_login:
                if email_input and password_input and api_key_input:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.session_state.gemini_key = api_key_input.strip()
                    st.success("Login Berhasil!")
                    st.rerun()
                else:
                    st.error("Mohon isi Email, Password, dan Gemini API Key dengan lengkap.")
    st.stop()

# --- FUNGSI PEMANGGILAN AI DENGAN RECOVERY ---
def generate_ai_response(prompt_text):
    try:
        genai.configure(api_key=st.session_state.gemini_key)
        # Mencoba model flash terlebih dahulu
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt_text)
            return response.text
        except Exception:
            # Jika gagal, otomatis switch ke model pro
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt_text)
            return response.text
    except Exception as e:
        return f"Error dari Google API: {str(e)}\n\nCatatan: Pastikan API Key yang Anda masukkan saat Login sudah benar dari Google AI Studio."

# --- MENU UTAMA (SIDEBAR) ---
st.sidebar.title(f"Halo, {st.session_state.user_email.split('@')[0]}! 👋")
menu = st.sidebar.radio("Navigasi Menu", [
    "🎯 Assessment & Blueprint", 
    "✍️ Script Builder", 
    "🎬 Video to Script", 
    "📅 Content Planner", 
    "📂 Riwayat (History)"
])

if st.sidebar.button("🚪 Log Out"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# 1. ASSESSMENT & MASTER BLUEPRINT
# ==========================================
if menu == "🎯 Assessment & Blueprint":
    st.title("🎯 Creator Assessment & Master Blueprint")
    st.write("Isi formulir asesmen di bawah ini agar AI memahami target, minat, dan arah konten Anda.")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        with col1:
            niche = st.text_input("Topik / Niche Utama Konten", placeholder="Contoh: Kuliner Nusantara, Tech & AI, Personal Finance")
            target_audience = st.text_input("Target Audiens Anda", placeholder="Contoh: Gen Z, Karyawan Muda, Ibu Rumah Tangga")
        with col2:
            tone = st.selectbox("Tone / Gaya Bicara", ["Santai & Humor", "Formal & Edukatif", "Provokatif & Semangat", "Storytelling & Emosional"])
            platform = st.selectbox("Platform Utama", ["TikTok / Reels", "YouTube Long Form", "Instagram Carousel", "Multi-Platform"])
            
        submit_assessment = st.form_submit_button("Analisa & Buat Master Blueprint 🪄")
        
    if submit_assessment:
        with st.spinner("AI sedang menganalisis profil dan merancang strategi konten Anda..."):
            prompt = f"""
            Bertindaklah sebagai Master Content Strategist. Buatkan Master Blueprint profesional untuk kreator berikut:
            - Niche: {niche}
            - Target Audiens: {target_audience}
            - Tone: {tone}
            - Platform Utama: {platform}
            
            Berikan hasil analisis dengan format yang rapi:
            1. Evaluasi & Pemeriksaan Jawaban (Ulasan singkat tentang profil kreator)
            2. Content Positioning (Posisi unik di pasaran)
            3. Unique Value Proposition (UVP)
            4. 3 Content Pillars Utama
            """
            result_text = generate_ai_response(prompt)
            st.session_state.blueprint = result_text
            
            # Simpan ke history jika berhasil
            if "Error dari Google API" not in result_text:
                st.session_state.history.append({
                    "type": "Master Blueprint",
                    "title": f"Blueprint: {niche}",
                    "content": result_text,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            
    if st.session_state.blueprint:
        st.subheader("📋 Hasil Master Blueprint Anda:")
        st.markdown(st.session_state.blueprint)
        if st.button("🔄 Buat Master Blueprint Baru (Reset)"):
            st.session_state.blueprint = None
            st.rerun()

# ==========================================
# 2. SCRIPT BUILDER
# ==========================================
elif menu == "✍️ Script Builder":
    st.title("✍️ AI Script Builder")
    st.write("Masukkan ide kasar konten Anda, lalu gunakan tombol AI di bawah untuk generate bagian demi bagian secara real-time.")
    
    ide_konten = st.text_area("Masukkan Ide / Topik Konten:", placeholder="Contoh: 3 kesalahan umum saat mengatur gaji pertama...")
    
    if ide_konten:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            btn_hook = st.button("🔥 Generate Hook")
        with col2:
            btn_foreshadow = st.button("🔮 Generate Foreshadow")
        with col3:
            btn_body = st.button("📝 Generate Isi Konten")
        with col4:
            btn_cta = st.button("📢 Generate CTA")
            
        if btn_hook:
            with st.spinner("Membuat Hook memikat..."):
                res = generate_ai_response(f"Buatkan 3 opsi Hook (3 detik pertama) yang sangat memikat untuk ide konten: {ide_konten}")
                st.subheader("🔥 Hasil Hook:")
                st.write(res)
                
        if btn_foreshadow:
            with st.spinner("Membuat Foreshadow..."):
                res = generate_ai_response(f"Buatkan kalimat Foreshadow/Retention untuk menjaga penonton tetap menonton video tentang: {ide_konten}")
                st.subheader("🔮 Hasil Foreshadow:")
                st.write(res)
                
        if btn_body:
            with st.spinner("Menyusun isi konten..."):
                res = generate_ai_response(f"Buatkan poin-poin isi video/skrip yang padat, bernilai tinggi, dan mudah dipahami untuk ide: {ide_konten}")
                st.subheader("📝 Hasil Isi Konten:")
                st.write(res)
                
        if btn_cta:
            with st.spinner("Membuat CTA..."):
                res = generate_ai_response(f"Buatkan 3 kalimat Call to Action (CTA) interaktif agar penonton komen/follow untuk video tentang: {ide_konten}")
                st.subheader("📢 Hasil CTA:")
                st.write(res)

# ==========================================
# 3. VIDEO TO SCRIPT
# ==========================================
elif menu == "🎬 Video to Script":
    st.title("🎬 Video to Script Converter")
    st.write("Masukkan transkrip teks atau poin dari video referensi/viral untuk dianalisis dan diubah menjadi gaya skrip Anda sendiri.")
    
    ref_text = st.text_area("Tempel (Paste) transkrip atau teks video referensi di sini:")
    if st.button("Bongkar & Ubah ke Skrip Baru ⚡"):
        if ref_text:
            with st.spinner("Menganalisis struktur video referensi..."):
                prompt = f"""
                Analisis transkrip video referensi berikut:
                \"{ref_text}\"
                
                Uraikan struktur suksesnya (Hook, Pola Penyampaian, dan CTA) lalu buatkan versi skrip baru yang lebih segar dan orisinal berdasarkan struktur tersebut!
                """
                res = generate_ai_response(prompt)
                st.subheader("✨ Hasil Konversi Skrip:")
                st.write(res)
        else:
            st.warning("Mohon masukkan teks transkrip terlebih dahulu.")

# ==========================================
# 4. CONTENT PLANNER
# ==========================================
elif menu == "📅 Content Planner":
    st.title("📅 Smart Content Planner")
    st.write("Susun jadwal rilis konten mingguan Anda secara sistematis dan terukur.")
    
    col1, col2 = st.columns(2)
    with col1:
        p_judul = st.text_input("Judul Konten / Topik")
        p_hari = st.selectbox("Hari Rilis", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
    with col2:
        p_status = st.selectbox("Status Produksi", ["Ide Masih Mentah", "Sedang Dibuat Skrip", "Proses Syuting/Edit", "Siap Tayang"])
        
    if st.button("Tambah ke Jadwal 📌"):
        if 'planner' not in st.session_state:
            st.session_state.planner = []
        st.session_state.planner.append({"judul": p_judul, "hari": p_hari, "status": p_status})
        st.success("Konten berhasil dijadwalkan!")
        
    if 'planner' in st.session_state and st.session_state.planner:
        st.subheader("📋 Jadwal Konten Anda:")
        for idx, item in enumerate(st.session_state.planner):
            st.markdown(f"**{idx+1}. [{item['hari']}] {item['judul']}** — *Status: {item['status']}*")

# ==========================================
# 5. RIWAYAT (HISTORY)
# ==========================================
elif menu == "📂 Riwayat (History)":
    st.title("📂 Arsip Riwayat & Memori Konten")
    st.write("Semua hasil blueprint, skrip, dan analisis Anda tersimpan di sini.")
    
    if st.session_state.history:
        for idx, h in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📌 [{h['type']}] {h['title']} ({h['date']})"):
                st.write(h['content'])
    else:
        st.info("Belum ada riwayat tersimpan. Mulailah membuat blueprint atau skrip!")
