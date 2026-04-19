# smart_rural_dashboard_final.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(
    page_title="🌾 Smart Rural Dashboard",
    layout="wide"
)

st.title("🌾 Smart Rural Multi-Agent Dashboard")
st.markdown("Manage Crops, Water, Power, Welfare, Market & Education efficiently.")

# ---------- Sidebar Inputs ----------
st.sidebar.header("Simulation Settings")
rain_mm = st.sidebar.slider("Rainfall (mm)", 0, 50, 10)
power_available = st.sidebar.slider("Power Availability (%)", 0, 100, 70)

# ---------- Sample Data ----------
crops = [
    {"field_name": "Field A", "crop": "Tomato", "water_needed": 100},
    {"field_name": "Field B", "crop": "Rice", "water_needed": 150}
]
farmers = [{"name": "Rahul", "id": "F001"}, {"name": "Priya", "id": "F002"}]
students = [{"name": "Amit", "attendance": 70}, {"name": "Sneha", "attendance": 85}]
market_prices = {"Tomato": 25, "Rice": 18}
weather = {"rain_mm": rain_mm}

# ---------- Agents ----------
class FarmAgent:
    def monitor_crops(self, crop, weather):
        return crop['water_needed'] if weather['rain_mm'] <= 20 else 0

    def pest_alert(self, crop):
        return random.choice([True, False])

class WaterAgent:
    def optimize_water(self, crop, weather):
        return max(0, crop['water_needed'] - weather['rain_mm'])

class PowerAgent:
    def check_power(self, power):
        return power >= 50

class WelfareAgent:
    def draft_form(self, farmer):
        return f"Form ready for {farmer['name']}"

class MarketAgent:
    def advise(self, crop):
        price = market_prices[crop['crop']]
        return price >= 20

class EducationAgent:
    def alert(self, student):
        return student['attendance'] >= 75

# ---------- Coordinator ----------
farm_agent = FarmAgent()
water_agent = WaterAgent()
power_agent = PowerAgent()
welfare_agent = WelfareAgent()
market_agent = MarketAgent()
education_agent = EducationAgent()

# ---------- Metric Cards ----------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("🌧 Rainfall (mm)", rain_mm)
col2.metric("⚡ Power Availability (%)", power_available)
total_water = sum([water_agent.optimize_water(crop, weather) for crop in crops])
col3.metric("💧 Total Irrigation (Liters)", total_water)

# ---------- Irrigation Chart ----------
st.subheader("💧 Irrigation Plan per Field")
irrigation_data = {crop['field_name']: water_agent.optimize_water(crop, weather) for crop in crops}
st.bar_chart(pd.DataFrame.from_dict(irrigation_data, orient='index', columns=['Liters']))

# ---------- Market Chart ----------
st.subheader("📈 Market Prices")
market_data = {crop['crop']: market_prices[crop['crop']] for crop in crops}
st.line_chart(pd.DataFrame.from_dict(market_data, orient='index', columns=['Price']))

# ---------- Agent Tabs ----------
st.subheader("🔍 Agent Outputs")
tabs = st.tabs(["Farm", "Water", "Power", "Welfare", "Market", "Education"])

# Farm Agent
with tabs[0]:
    st.markdown("### 🌾 Farm Agent")
    for crop in crops:
        irrigation = water_agent.optimize_water(crop, weather)
        st.info(f"{crop['field_name']} irrigation needed: {irrigation} liters")
        if farm_agent.pest_alert(crop):
            st.error(f"Pest alert detected in {crop['field_name']}")
        else:
            st.success(f"No pest detected in {crop['field_name']}")

# Water Agent
with tabs[1]:
    st.markdown("### 💧 Water Agent")
    for crop in crops:
        optimized = water_agent.optimize_water(crop, weather)
        st.info(f"{crop['field_name']}: Recommended {optimized} liters")

# Power Agent
with tabs[2]:
    st.markdown("### ⚡ Power Agent")
    if power_agent.check_power(power_available):
        st.success("Power sufficient for irrigation")
    else:
        st.error("Low power! Delay irrigation")

# Welfare Agent
with tabs[3]:
    st.markdown("### 👩‍🌾 Welfare Agent")
    for farmer in farmers:
        st.info(welfare_agent.draft_form(farmer))

# Market Agent
with tabs[4]:
    st.markdown("### 💰 Market Agent")
    for crop in crops:
        if market_agent.advise(crop):
            st.success(f"Good to sell {crop['crop']} at price {market_prices[crop['crop']]}")
        else:
            st.warning(f"Hold {crop['crop']} — price low ({market_prices[crop['crop']]})")

# Education Agent
with tabs[5]:
    st.markdown("### 🎓 Education Agent")
    for student in students:
        if education_agent.alert(student):
            st.success(f"{student['name']} attendance is fine")
        else:
            st.error(f"{student['name']} low attendance ({student['attendance']}%)")

# ---------- Save Daily Plan ----------
if st.button("💾 Save Daily Plan"):
    all_data = []
    for crop in crops:
        all_data.append(["FarmAgent", f"{crop['field_name']} irrigation: {water_agent.optimize_water(crop, weather)}"])
    for crop in crops:
        all_data.append(["MarketAgent", f"{crop['crop']} price: {market_prices[crop['crop']]}"])
    df = pd.DataFrame(all_data, columns=["Agent", "Output"])
    filename = f"daily_plan_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    st.success(f"Daily plan saved to {filename}")
