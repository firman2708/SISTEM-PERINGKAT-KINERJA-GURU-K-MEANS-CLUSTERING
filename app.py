
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Simulasi database pengguna
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "guru1": {"password": "guru123", "role": "Guru"},
    "siswa1": {"password": "siswa123", "role": "Siswa"}
}

st.set_page_config(page_title="Sistem Peringkat Kinerja Guru", layout="wide")

# Setup session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

def login_page():
    st.title("🔐 Login Pengguna")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Berhasil login sebagai {st.session_state.role}")
            st.rerun()

        else:
            st.error("Username atau password salah")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.experimental_rerun()

def main_app():
    st.sidebar.title(f"Halo, {st.session_state.username}")
    st.sidebar.write(f"Peran: {st.session_state.role}")
    st.sidebar.button("Logout", on_click=logout)

    st.title("📊 Sistem Peringkat Kinerja Guru Berdasarkan Evaluasi Siswa")
    
    uploaded_file = st.file_uploader("📁 Unggah file CSV data evaluasi", type="csv")
    
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.subheader("🧾 Data Evaluasi")
        st.dataframe(data)

        fitur = data.iloc[:, 1:]
        kmeans = KMeans(n_clusters=3, random_state=42)
        data['Klaster'] = kmeans.fit_predict(fitur)

        st.subheader("📄 Hasil Klasterisasi")
        st.dataframe(data)

        # Visualisasi
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(fitur)
        data['PCA1'] = pca_data[:, 0]
        data['PCA2'] = pca_data[:, 1]

        st.subheader("📈 Visualisasi Klaster")
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x='PCA1', y='PCA2', hue='Klaster', palette='Set2', s=100, ax=ax)
        ax.set_title("Visualisasi Klaster Kinerja Guru")
        st.pyplot(fig)
    else:
        st.info("Silakan unggah file CSV untuk memulai analisis.")

# Kontrol alur
if st.session_state.logged_in:
    main_app()
else:
    login_page()
