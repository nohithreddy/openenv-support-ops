import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env.environment import SupportEnv
from env.models import Action

st.set_page_config(page_title="SupportOps Dashboard", layout="wide")

st.title("📊 SupportOps Environment Dashboard")

if "env" not in st.session_state:
    st.session_state.env = SupportEnv()
    st.session_state.obs = st.session_state.env.reset("medium")

env = st.session_state.env
obs = st.session_state.obs

# Display tickets
st.subheader("🎫 Tickets")

for t in obs.tickets:
    col1, col2, col3, col4 = st.columns(4)

    col1.write(f"ID: {t.id}")
    col2.write(f"Priority: {t.priority}")
    col3.write(f"SLA: {t.sla}")
    col4.write("✅ Resolved" if t.resolved else "❌ Open")

# Action section
st.subheader("⚡ Take Action")

ticket_id = st.number_input("Ticket ID", min_value=1, step=1)
action_type = st.selectbox("Action", ["close", "escalate", "reply"])

if st.button("Submit Action"):
    action = Action(type=action_type, ticket_id=int(ticket_id))
    obs, reward, done, _ = env.step(action)

    st.session_state.obs = obs

    st.success(f"Reward: {reward.score}")

    if done:
        st.warning("Episode finished")

# Show metrics
st.subheader("📈 Metrics")

st.write("Steps:", obs.steps)
st.write("Customer Satisfaction:", obs.satisfaction)