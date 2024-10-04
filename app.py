import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

def desc_calc():
    # Load precomputed descriptors
    desc = pd.read_csv('descriptors_output.csv')
    return desc

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# APP Logo image
image = Image.open('app_logo.png')

st.image(image, use_column_width=True)

# Page title & Description
st.markdown("""
# Bioactivity Prediction App (Acetylcholinesterase)

This app allows users to input a molecule and predict its bioactivity in inhibiting the enzyme `Acetylcholinesterase`, a crucial drug target for Alzheimer's disease. By analyzing molecular properties, the app provides insights into the molecule's potential effectiveness.

**Acetylcholine Information:** 
- `Acetylcholine` is a vital neurotransmitter involved in muscle movement, memory, and learning. It’s important because its imbalance is linked to diseases like Alzheimer's and muscle disorders.
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown("""
[Example input file](example_input.txt)
""")

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating..."):
        desc_calc()

    # Read in calculated descriptors and display the dataframe
    desc = pd.read_csv('descriptors_output.csv')
   
    # Read descriptor list used in previously built model
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')
