# generative_scenario_explorer.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import openai  # Or use huggingface_hub for open-source models

# ====== Page Config ======
st.set_page_config(page_title="Generative Scenario Explorer", layout="wide")

# ====== Sidebar ======
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "🧠 Step 1: Scenario Generation",
    "📊 Step 2: Impact Simulation",
    "🤖 Step 3: RL Mitigation",
    "📋 Step 4: Final Summary"
])

# ====== Step 0: Home ======
if page == "🏠 Home":
    st.image("assets/logo.png", width=220)
    st.markdown("<h1 style='text-align: center;'>🌍 Generative Scenario Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>AI-powered foresight tool for emerging and extreme reinsurance risks</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🚨 Problem")
    st.markdown("""
    Traditional stress testing can’t anticipate emerging or compound risks (e.g. hurricane + cyberattack).
    - Reinsurers need better foresight into “unknown unknowns”
    - Current planning relies on outdated scenarios or historical data only
    """)

    st.markdown("### 💡 Our Solution")
    st.markdown("""
    - 💬 **LLM** generates plausible extreme or emerging scenarios from user prompts
    - 📊 Simulated losses for each business line
    - 🧠 **RL** finds optimal mitigation (e.g. cover changes, exclusions, limits)
    - 📋 Summarized insight report to share with stakeholders
    """)

    st.success("✅ Use the sidebar to begin your interactive scenario exploration.")


# ====== Step 1: Scenario Generation ======
elif page == "🧠 Step 1: Scenario Generation":
    st.header("🧠 Step 1: Generate Emerging Risk Scenario")
    st.image("assets/step1_icon.png", width=80)

    st.markdown("Describe a ‘What if?’ scenario. The LLM will generate a narrative and plausible risk factors.")

    scenario_input = st.text_area("🔮 Describe a scenario", placeholder="e.g. What if a major earthquake hits LA during a cyberattack on US infrastructure?", height=100)

    if st.button("🪄 Generate Scenario"):
        with st.spinner("Generating narrative..."):
            time.sleep(2)  # Replace with OpenAI or Hugging Face call
            narrative = f"""
            A 7.8 magnitude earthquake strikes Los Angeles during a coordinated cyberattack on national infrastructure. 
            Power outages disrupt emergency response. Property damage is compounded by fire following quake. 
            The cyberattack disables insurer claim systems for 72 hours, delaying response.
            """
            st.success("✅ Scenario Generated")
            st.markdown("### 📘 Scenario Narrative")
            st.markdown(narrative.strip())


# ====== Step 2: Impact Simulation ======
elif page == "📊 Step 2: Impact Simulation":
    st.header("📊 Step 2: Portfolio Impact Simulation")
    st.image("assets/step2_icon.png", width=80)

    st.markdown("We simulate losses across key lines of business under the generated scenario.")

    lob = ["Homeowners", "Commercial", "Motor", "Cyber", "Liability"]
    losses = np.random.normal(loc=[300, 500, 80, 220, 120], scale=[30, 50, 15, 40, 25])
    df_loss = pd.DataFrame({"Line of Business": lob, "Losses ($M)": np.round(losses, 1)})

    st.dataframe(df_loss)

    fig, ax = plt.subplots()
    ax.bar(df_loss["Line of Business"], df_loss["Losses ($M)"], color="tomato")
    ax.set_title("Simulated Losses by Line of Business")
    st.pyplot(fig)

    st.info("➡️ Next, let the AI find optimal mitigation strategies.")


# ====== Step 3: RL Mitigation ======
elif page == "🤖 Step 3: RL Mitigation":
    st.header("🤖 Step 3: Optimize Mitigation Strategy")
    st.image("assets/step3_icon.png", width=80)

    st.markdown("An RL agent proposes protection adjustments to reduce tail risk.")

    if st.button("🚀 Run Mitigation Agent"):
        with st.spinner("Training and optimizing..."):
            time.sleep(2)

            df_strategy = pd.DataFrame({
                "Strategy": ["Baseline", "Mitigated"],
                "Expected Loss ($M)": [1220, 920],
                "Tail Loss @ 1-in-100 ($M)": [1800, 1200],
                "Reinsurance Spend ($M)": [90, 110]
            })

            st.success("✅ Mitigation strategy found.")

            st.markdown("### 🧮 Strategy Comparison")
            st.dataframe(df_strategy)

            fig, ax = plt.subplots()
            ax.bar(df_strategy["Strategy"], df_strategy["Tail Loss @ 1-in-100 ($M)"], color=["gray", "green"])
            ax.set_ylabel("Tail Risk ($M)")
            ax.set_title("Reduction in Tail Loss")
            st.pyplot(fig)

            st.info("➡️ Proceed to summary for management explanation.")


# ====== Step 4: Final Summary ======
elif page == "📋 Step 4: Final Summary":
    st.header("📋 Step 4: Final Report and Takeaways")
    st.image("assets/step4_icon.png", width=80)

    st.markdown("### 🧾 Management Summary")
    st.success("""
    Under a compound cyber-catastrophe scenario, tail losses exceeded $1.8B.  
    The AI recommended purchasing $50M additional cyber cover and earthquake excess layer.  
    This reduced 1-in-100 tail losses by 33% and improved solvency buffer by 20 points.
    """)

    st.markdown("### 📌 Key Insights")
    st.markdown("""
    - Generative AI expands stress test possibilities  
    - RL delivers quantified recommendations  
    - Supports capital efficiency, solvency, and product design  
    """)

    st.download_button(
        label="⬇️ Download Summary (PDF Coming Soon)",
        data="Summary placeholder text",
        file_name="Generative_Scenario_Explorer_Summary.txt",
        disabled=True
    )
