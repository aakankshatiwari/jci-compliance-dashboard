# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/aakanksha54/app-py.9d855850-ea2d-4e8b-9063-7d02d4b09c46.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20250416/auto/storage/goog4_request%26X-Goog-Date%3D20250416T140128Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D50a2f42a7205cb782af25f8d789f53aa35894f1bd7147352abe5b25fcaaf9e97b7f497972466be91ed34625a96f3d4dd1f541df5a3f6439b094a596be5b421dd7edec4516d126a87de398efa35454a64b5638ef9287531a648188e41c019283f93b2289b6b2969ecd68ea4a941a5e675ce9c93ba39c4fbb022998a1d17b52f3a9baf9daebf1cd21d0949965aba912a1811143fda70d4e0f883ba7cc2013f784932ff1683275cc37be9ee8c2cf8120e630f99a69b148ed5f045cb64812a5086121efbab4c39223eca3a4d6b0acc0bfc028b0787382adf4303eeee5a7c99c0311ee5cf957081549711e4428f397d0d893c36788b9f56886bab9c0ef94c1cc6f2fe
"""

!pip install streamlit
!pip install fpdf

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Load dataset (adjust the path if necessary)
df = pd.read_csv("/content/jci_hospital_compliance_data.csv")

# App Title
st.title("🏥 JCI Compliance Dashboard for Rajasthan Government Hospitals")

# Hospital Selector
hospital = st.selectbox("Select a Hospital to Audit:", df["Hospital_Name"].tolist())

# Extract selected hospital row
row = df[df["Hospital_Name"] == hospital].squeeze()
compliance_cols = df.columns.difference(["Hospital_Name", "Accreditation_Status"])

# Calculate Compliance Score
yes_count = sum(row[col] == "Yes" for col in compliance_cols)
total = len(compliance_cols)
score = round((yes_count / total) * 100, 2)

# Display results
st.subheader(f"Accreditation Status: {row['Accreditation_Status']}")
st.metric("JCI Compliance Score", f"{score}%")

# Pie Chart
labels = ['Compliant', 'Non-compliant']
values = [yes_count, total - yes_count]
colors = ['#4CAF50', '#FF7043']
fig, ax = plt.subplots()
ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Final Recommendation
if row["Accreditation_Status"] == "Accredited":
    rec = "✅ Recommended for International Patients"
    st.success(rec)
else:
    rec = "⚠️ Not yet ready for international accreditation."
    st.warning(rec)

# Export as PDF
if st.button("📄 Export PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt=f"JCI Compliance Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Hospital: {hospital}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Accreditation Status: {row['Accreditation_Status']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Compliance Score: {score}%", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Recommendation: {rec}", ln=True, align='L')

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Compliance Details:", ln=True, align='L')
    for col in compliance_cols:
        status = row[col]
        pdf.cell(200, 8, txt=f"{col.replace('_', ' ')}: {status}", ln=True, align='L')

    pdf.output("jci_report.pdf")
    st.success("PDF Report generated as jci_report.pdf")

    with open("jci_report.pdf", "rb") as f:
        st.download_button("📥 Download Report", f, file_name="jci_report.pdf")