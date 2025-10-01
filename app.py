import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os

# --------------------
# Vypocet bodu na kruznici
# --------------------
def generuj_body(x0, y0, r, n):
    uhly = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = x0 + r * np.cos(uhly)
    y = y0 + r * np.sin(uhly)
    return x, y

# --------------------
# Vykresleni a ulozeni obrazku
# --------------------
def vykresli_kruh(x, y, x0, y0, r, barva, jednotka, obrazek_soubor):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x, y, color=barva, label='Body')
    ax.plot(x, y, 'o', color=barva)
    kruznice = plt.Circle((x0, y0), r, fill=False, linestyle='--', color='gray')
    ax.add_patch(kruznice)

    ax.set_xlabel(f'X [{jednotka}]')
    ax.set_ylabel(f'Y [{jednotka}]')
    ax.set_title("Body na kruznici")
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()

    popis = f"Stred: ({x0}, {y0}) | Polomer: {r} {jednotka} | Pocet bodu: {len(x)} | Barva: {barva}"
    plt.figtext(0.5, -0.05, popis, ha="center", fontsize=10)

    plt.tight_layout()
    fig.savefig(obrazek_soubor, bbox_inches='tight')
    return fig

# --------------------
# Generovani PDF
# --------------------
def vytvor_pdf(obrazek_soubor, x0, y0, r, n, barva, jednotka):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Vystup - Body na kruznici", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Stred: ({x0}, {y0})", ln=True)
    pdf.cell(200, 10, txt=f"Polomer: {r} {jednotka}", ln=True)
    pdf.cell(200, 10, txt=f"Pocet bodu: {n}", ln=True)
    pdf.cell(200, 10, txt=f"Barva bodu: {barva}", ln=True)
    pdf.cell(200, 10, txt=f"Jednotka: {jednotka}", ln=True)
    pdf.ln(10)

    if os.path.exists(obrazek_soubor):
        pdf.image(obrazek_soubor, x=15, y=None, w=180)

    vystup_pdf = "vystup_kruh.pdf"
    pdf.output(vystup_pdf)
    return vystup_pdf

# --------------------
# STREAMLIT APLIKACE
# --------------------
st.set_page_config(page_title="Kruznice", layout="centered")
st.title("🟢 Body na kruznici")

# Sidebar: parametry
st.sidebar.header("Parametry")
x0 = st.sidebar.number_input("X stred", value=0.0)
y0 = st.sidebar.number_input("Y stred", value=0.0)
r = st.sidebar.number_input("Polomer [m]", min_value=0.1, value=5.0)
n = st.sidebar.number_input("Pocet bodu", min_value=3, value=12, step=1)
barva = st.sidebar.color_picker("Barva bodu", "#0000FF")
jednotka = st.sidebar.text_input("Jednotka", "m")

# Vykresleni grafu
x, y = generuj_body(x0, y0, r, int(n))
obrazek_soubor = "kruh.png"
fig = vykresli_kruh(x, y, x0, y0, r, barva, jednotka, obrazek_soubor)
st.pyplot(fig)

# Tlacitko: export do PDF
if st.button("📄 Ulozit vystup do PDF"):
    if os.path.exists(obrazek_soubor):
        try:
            pdf_soubor = vytvor_pdf(obrazek_soubor, x0, y0, r, n, barva, jednotka)
            with open(pdf_soubor, "rb") as f:
                st.download_button("📥 Stahnout PDF", f, file_name=pdf_soubor, mime="application/pdf")
        except Exception as e:
            st.error(f"Chyba pri generovani PDF: {e}")
    else:
        st.error("❌ Obrazek nebyl nalezen. Nejprve vykresli graf.")

# Info sekce
with st.expander("ℹ️ O aplikaci"):
    st.markdown("""
    - Aplikace vykresluje rovnomerne rozmistené body na kruznici
    - Umoznuje export grafu a parametru do PDF
    - Autor: Vase jmeno
    """)

