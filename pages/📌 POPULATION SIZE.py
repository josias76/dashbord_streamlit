import pandas as pd
import numpy as np
import plotly.graph_objs as go
from scipy.stats import chi2, norm
import streamlit as st

#actual population
st.title("ACTUAL POPULATION")

N=1000

# Load the CSV file
dataset = pd.read_csv('telehealth_data.csv',)

population_ages  = dataset['age']

population_mean = np.mean(population_ages)
population_std = np.std(population_ages, ddof=1)  

st.write("___")

st.metric(label="Population Mean (Age)", value=f"{population_mean:.2f}")
st.metric(label="Population Standard Deviation (Age)", value=f"{population_std:.2f}")
st.metric(label="Population Size (N)", value=f"{N}")
# bande de bas de pages
st.markdown("""
    <hr style="border-top: 1px solid #4CAF50; margin-top: 50px;"/>
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        &copy; 2025 <strong>Josias Nteme</strong> - Tous droits réservés.
    </div>
""", unsafe_allow_html=True)