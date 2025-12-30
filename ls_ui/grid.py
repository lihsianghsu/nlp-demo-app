import streamlit as st

def full():
    return st.container()

def two_col(ratios=(1, 1), gap="large"):
    return st.columns(ratios, gap=gap)

def dashboard():
    """Main content + control panel"""
    return st.columns((2, 1), gap="large")

def three_col():
    return st.columns((1, 1, 1), gap="large")
