import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os

# --------------------
# Funkce: výpočet bodů
# --------------------
def generuj_body(x0, y0, r, n):
    uhly = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = x0 + r * np.cos(uhly)
    y = y0 + r * np.sin(uhly)
    return x, y

# --------------------
# Funkce: vykreslení grafu a uložení
# --------------------
def vykresli_kruh(x, y, x0, y0, r, barva, jednotka, obrazek_soubor):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x, y, color=barva, label='Body na kružnici')
    ax.plot(x, y, 'o', color=barva)
    kruznice = plt.Circle((x0, y0), r, fill=False, linestyle='--', color='gray')
    ax.add_patch(kruznice)

    ax.set_xlabel(f'X [{jednotka}]')
    ax.set_ylabel(f'Y [{jednotka}]')
    ax.set_title("Body na kružnici")
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()

    popis = f"Střed: ({x0}, {y0}) | Poloměr: {r} {jednotka} | Počet bodů: {len(x)} | Barva: {barva}"
    plt.figtext(0.5, -0.05, popis, ha="center", fontsize=10)

    plt.tight_layout()
    fig.savefig(obrazek_soubor, bbox_inches='tight')
    return fig

# --------------------
# Funkce: generování PDF
# --------------------
def vytvor_pdf(obrazek_soubor, x0, y0, r, n, barva, jednotka):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Výstup – Body na kružnici", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Střed: ({x0}, {y0})", ln=True)
    pdf.cell(200, 10, txt=f"Poloměr: {r} {jednotka}", ln=True)
    pdf.cell(200, 10, txt=f"Počet bodů: {n}", ln=True)
    pdf.cell(200, 10, txt=f"Barva bodů: {barva}", ln=True)
    pdf.cell(200, 10, txt=f"Jednotka: {jednotka}", ln=True)
    pdf.ln(10)

    if os.path.exists(obrazek_soubor):
        pdf.image(obrazek_soubor, x=15, y=None, w=180)

    vystup_pdf = "vystup_kruh.pdf"
    pdf.output(vystup_pdf)
    return vystup_pdf

# --------------------
# Streamlit UI
# --------------------
st.set_page_config(page_title="Body na kružnici", layout="centered")
st.title("🟢 Body na kružnici")

# Vstupní formulář
st.sidebar.header("Parametry kružnice")
x0 = st.sidebar.number_input("X střed", value=0.0)
y0 = st.sidebar.number_input("Y střed", value=0.0)
r = st.sidebar.number_input("Poloměr [m]", min_value=0.1, value=5.0)
n = st.sidebar.number_input("Počet bodů", min_value=3, value=12, step=1)
barva = st.sidebar.color_picker("Barva bodů", "#0000FF")
jednotka = st.sidebar.text_input("Jednotka os", "m")

# Výpočet a graf
x, y = generuj_body(x0, y0, r, int(n))
obrazek_soubor = "kruh.png"
fig = vykresli_kruh(x, y, x0, y0, r, barva, jednotka, obrazek_soubor)
st.pyplot(fig)

# Tlačítko: Vytvořit PDF
if st.button("📄 Uložit výstup do PDF"):
    pdf_soubor = vytvor_pdf(obrazek_soubor, x0, y0, r, n, barva, jednotka)
    with open(pdf_soubor, "rb") as f:
        st.download_button("📥 Stáhnout PDF", f, file_name=pdf_soubor, mime="application/pdf")

# Info panel
with st.expander("ℹ️ O aplikaci"):
    st.markdown("""
    **Autor:** *Tvoje jméno*  
    **Popis:** Aplikace vykreslí zadaný počet bodů rovnoměrně rozložených na kružnici podle zadaného středu a poloměru.  
    **Funkce:**
    - Volba středu, poloměru, počtu bodů, barvy a jednotky
    - Vykreslení kružnice s body a legendou
    - Export do PDF včetně grafu a parametrů
    """)
