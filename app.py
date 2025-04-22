
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io
from PIL import Image

# --- Logout ---
def logout_button():
    if st.sidebar.button("🔓 Logout"):
        st.session_state.clear()
        st.experimental_rerun()

# --- Simulasi login sederhana ---
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username.startswith("admin") and password == "admin":
            st.success("Berhasil login sebagai Admin")
            st.session_state["role"] = "admin"
            st.rerun()
        elif username.startswith("guru") and password == "guru":
            st.success("Berhasil login sebagai Guru")
            st.session_state["role"] = "guru"
            st.session_state["username"] = username
            st.rerun()
        elif username.startswith("siswa") and password == "siswa":
            st.success("Berhasil login sebagai Siswa")
            st.session_state["role"] = "siswa"
            st.rerun()
        else:
            st.error("Login gagal")

# --- Halaman evaluasi untuk siswa ---
def siswa_page():
    logout_button()
    st.title("Form Evaluasi Guru")
    nama_guru = st.text_input("Nama Guru")
    kedisiplinan = st.slider("Kedisiplinan", 1, 5)
    komunikasi = st.slider("Komunikasi", 1, 5)
    penguasaan = st.slider("Penguasaan Materi", 1, 5)
    kreativitas = st.slider("Kreativitas", 1, 5)
    kerapian = st.slider("Kerapian Penampilan", 1, 5)
    if st.button("Kirim Evaluasi"):
        st.success("Terima kasih, evaluasi berhasil dikirim (simulasi).")

# --- Halaman admin ---
def admin_page():
    logout_button()
    st.title("Admin Panel - Clustering Kinerja Guru")

    uploaded_file = st.file_uploader("Upload file CSV data evaluasi", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("Proses Clustering"):
            X = df.iloc[:, 1:]  # tanpa kolom nama
            kmeans = KMeans(n_clusters=3, random_state=42)
            df["Cluster"] = kmeans.fit_predict(X)
            st.session_state["clustered_df"] = df
            st.success("Clustering selesai")
            st.dataframe(df)

            # Export to Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Hasil Klaster')
                writer.save()
                st.download_button(
                    label="📥 Download Hasil Klaster (.xlsx)",
                    data=buffer.getvalue(),
                    file_name="hasil_klaster.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            # Grafik
            fig, ax = plt.subplots()
            scatter = ax.scatter(df.iloc[:, 1], df.iloc[:, 2], c=df["Cluster"], cmap='viridis')
            ax.set_xlabel(df.columns[1])
            ax.set_ylabel(df.columns[2])
            ax.set_title("Visualisasi Klaster")
            st.pyplot(fig)

            # Download gambar grafik
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            st.download_button("📷 Download Grafik Klaster (.png)", data=buf.getvalue(), file_name="klaster.png", mime="image/png")

# --- Halaman guru ---
def guru_page():
    logout_button()
    st.title("Halaman Guru")
    if "clustered_df" in st.session_state:
        df = st.session_state["clustered_df"]
        nama = st.session_state["username"].replace("guru_", "").capitalize()
        data_guru = df[df["Nama Guru"].str.lower().str.contains(nama.lower())]
        if not data_guru.empty:
            st.write(f"Data evaluasi untuk: **{nama}**")
            st.dataframe(data_guru)
        else:
            st.warning("Data Anda belum tersedia.")
    else:
        st.info("Admin belum melakukan proses clustering.")

# --- Main App ---
def main():
    if "role" not in st.session_state:
        login_page()
    elif st.session_state["role"] == "admin":
        admin_page()
    elif st.session_state["role"] == "guru":
        guru_page()
    elif st.session_state["role"] == "siswa":
        siswa_page()

if __name__ == "__main__":
    main()
