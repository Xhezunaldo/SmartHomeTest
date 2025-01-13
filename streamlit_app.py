import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="SMART HOME", layout="wide")

# Uncomment to enable autorefresh
count = st_autorefresh(interval=1000, limit=None, key="auto-refresh-handler")

# --------------- HELPER FUNCTIONS -----------------------

def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")

humidityData = pd.DataFrame()
temperatureData = pd.DataFrame()

def main():
    global humidityData, temperatureData

    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    if "LED1ButtonText" not in st.session_state:
        st.session_state.LED1ButtonText = " LED 1 On!"

    if "LED2ButtonText" not in st.session_state:
        st.session_state.LED2ButtonText = " LED 2 On!"

    if "LED1State" not in st.session_state:
        st.session_state.LED1State = False

    if "LED2State" not in st.session_state:
        st.session_state.LED2State = False

    if "CurrentHumidity" not in st.session_state:
        st.session_state.CurrentHumidity = 0

    if "CurrentTemperature" not in st.session_state:
        st.session_state.CurrentTemperature = 0

    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        drawDashboard()

def drawLogin():
    cols = st.columns([1, 0.8, 1], gap='small')
    with cols[0]:
        pass
    with cols[1]:
        st.markdown("<h1 style='color: navy;'>SMART HOME</h1>", unsafe_allow_html=True)
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")
        submit_button = st.button(label="Submit")

        if submit_button:
            if username_inp == "admin" and password_inp == "admin":
                st.session_state.LoggedIn = True
                st.rerun()
            else:
                st.error("Invalid Credential!")
    with cols[2]:
        pass

def drawDashboard():
    headercols = st.columns([1, 0.1, 0.1], gap="small")
    with headercols[0]:
        st.markdown("<h1 style='color: navy;'>SMART HOME Dashboard</h1>", unsafe_allow_html=True)
    with headercols[1]:
        st.button("Refresh")
    with headercols[2]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    st.markdown("<p style='color: navy;'>This dashboard provides a Smart Home data overview, also allowing you to control the LEDs!</p>", unsafe_allow_html=True)

    st.subheader(body="Current Status", anchor=False)
    cols = st.columns(2, gap="medium")
    with cols[0]:
        st.metric(label="Humidity", value=str(st.session_state.CurrentHumidity) + " %")
    with cols[1]:
        st.metric(label="Temperature", value=str(st.session_state.CurrentTemperature) + " °C")

    buttons = st.columns(2, gap="small")
    with buttons[0]:
        st.text("Control LED 1:")
        st.button(label=st.session_state.LED1ButtonText, on_click=operateLED1)
    with buttons[1]:
        st.text("Control LED 2:")
        st.button(label=st.session_state.LED2ButtonText, on_click=operateLED2)

    # Data input fields for testing
    st.subheader("Set Data Values for Testing")
    st.session_state.CurrentHumidity = st.number_input("Set Humidity (%)", min_value=0, max_value=100, value=st.session_state.CurrentHumidity)
    st.session_state.CurrentTemperature = st.number_input("Set Temperature (°C)", min_value=-50, max_value=50, value=st.session_state.CurrentTemperature)

def operateLED1():
    if st.session_state.LED1State is False:
        st.session_state.LED1ButtonText = "LED 1 Off!"
        st.session_state.LED1State = True
        st.toast("LED 1 on!")
    else:
        st.session_state.LED1ButtonText = "LED 1 On!"
        st.session_state.LED1State = False
        st.toast("LED 1 off!")

def operateLED2():
    if st.session_state.LED2State is False:
        st.session_state.LED2ButtonText = "LED 2 Off!"
        st.session_state.LED2State = True
        st.toast("LED 2 on!")
    else:
        st.session_state.LED2ButtonText = "LED 2 On!"
        st.session_state.LED2State = False
        st.toast("LED 2 off!")

if __name__ == "__main__":
    main()
