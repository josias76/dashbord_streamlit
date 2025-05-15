import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import time
from numerize.numerize import numerize
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

# Load custom CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load dataset from Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Sidebar filters
region = st.sidebar.multiselect("SELECT REGION", options=df["Region"].unique(), default=df["Region"].unique())
location = st.sidebar.multiselect("SELECT LOCATION", options=df["Location"].unique(), default=df["Location"].unique())
construction = st.sidebar.multiselect("SELECT CONSTRUCTION", options=df["Construction"].unique(), default=df["Construction"].unique())

# Apply filters
df_selection = df.query("Region == @region & Location == @location & Construction == @construction")

# Home page - descriptive analytics
def Home():
    with st.expander("VIEW EXCEL DATASET"):
        showData = st.multiselect("Filter:", df_selection.columns, 
                                  default=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"])
        st.dataframe(df_selection[showData], use_container_width=True)

    # KPIs
    total_investment = df_selection['Investment'].sum()
    investment_mode = df_selection['Investment'].mode()[0] if not df_selection['Investment'].mode().empty else 0
    investment_mean = df_selection['Investment'].mean()
    investment_median = df_selection['Investment'].median()
    total_rating = df_selection['Rating'].sum()

    total1, total2, total3, total4, total5 = st.columns(5, gap='small')
    with total1:
        st.info("Sum Investment", icon="💰")
        st.metric(label="Sum TZS", value=f"{total_investment:,.0f}")
    with total2:
        st.info("Most Investment", icon="💰")
        st.metric(label="Mode TZS", value=f"{investment_mode:,.0f}")
    with total3:
        st.info("Average", icon="💰")
        st.metric(label="Average TZS", value=f"{investment_mean:,.0f}")
    with total4:
        st.info("Central Earnings", icon="💰")
        st.metric(label="Median TZS", value=f"{investment_median:,.0f}")
    with total5:
        st.info("Ratings", icon="💰")
        st.metric(label="Rating", value=numerize(total_rating), help=f"Total Rating: {total_rating}")

    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
        df.hist(figsize=(16, 8), color='#898784', zorder=2, rwidth=0.9)
        st.pyplot()

# Graph section
def graphs():
    investment_by_business_type = df_selection.groupby("BusinessType").count()[["Investment"]].sort_values(by="Investment")

    fig_investment = px.bar(investment_by_business_type, x="Investment", y=investment_by_business_type.index,
                            orientation="h", title="<b>INVESTMENT BY BUSINESS TYPE</b>",
                            color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
                            template="plotly_white")
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"), yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        xaxis=dict(showgrid=True, gridcolor='#cecdcd')
    )

    investment_state = df_selection.groupby("State").count()[["Investment"]]
    fig_state = px.line(investment_state, x=investment_state.index, y="Investment",
                        title="<b>INVESTMENT BY STATE</b>",
                        color_discrete_sequence=["#0083b8"] * len(investment_state),
                        template="plotly_white")
    fig_state.update_layout(xaxis=dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=False))

    left, right, center = st.columns(3)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

    with center:
        fig_pie = px.pie(df_selection, values='Rating', names='State', title='RATINGS BY REGIONS')
        fig_pie.update_layout(legend_title="Regions", legend_y=0.9)
        fig_pie.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig_pie, use_container_width=True)

# Progress bar section
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)
    
    target = 3_000_000_000
    current = df_selection["Investment"].sum()
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target done!")
    else:
        st.write(f"You have {percent}% of {format(target, ',d')} TZS")
        for i in range(percent):
            time.sleep(0.01)  # Reduced for responsiveness
            mybar.progress(i + 1, text=" Target Percentage")

# Sidebar menu logic
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        Home()
        graphs()
    elif selected == "Progress":
        Progressbar()
        graphs()

# Main execution
sideBar()
st.sidebar.image("data/logo1.jpeg", caption="SDA Consulting")

# Quartile analysis
st.subheader("PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES")
feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)

fig2 = go.Figure(
    data=[go.Box(x=df['BusinessType'], y=df[feature_y])],
    layout=go.Layout(
        title="BUSINESS TYPE BY QUARTILES OF INVESTMENT",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        font=dict(color='black')
    )
)
st.plotly_chart(fig2, use_container_width=True)

# Hide streamlit default UI elements
hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# bande de bas de pages
st.markdown("""
    <hr style="border-top: 1px solid #4CAF50; margin-top: 50px;"/>
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        &copy; 2025 <strong>Josias Nteme</strong> - Tous droits réservés.
    </div>
""", unsafe_allow_html=True)