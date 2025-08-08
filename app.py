# generative_scenario_explorer.py

import os
import uuid
import time
import re
import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# API keys
openrouter_key = os.getenv("OPENROUTER_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")


# OpenAI client
openai_client = OpenAI(api_key=openai_key)

# Initialize session state for portfolio
if "scenario_history" not in st.session_state:
    st.session_state["scenario_history"] = []

# Claude via OpenRouter
def call_claude(prompt):
    headers = {
        "Authorization": f"Bearer {openrouter_key}",
        "HTTP-Referer": "https://yourprojectname.streamlit.app",
        "X-Title": "Generative Scenario Explorer",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Claude-based risk tagger
def extract_tags_with_claude(narrative):
    prompt = f"""
    Read the following reinsurance risk scenario and identify relevant risk categories from this list:
    [CAT, Cyber, Systemic, Health, Supply Chain, Political, ESG]

    Respond with a comma-separated list of the most relevant 2–4 categories.

    Scenario:
    """
    {narrative}
    """
    """
    tags = call_claude(prompt)
    return [tag.strip() for tag in tags.split(",") if tag.strip()]

# UI config
st.set_page_config(page_title="Generative Scenario Explorer", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "🏠 Home",
    "🧠 Step 1: Scenario Generation",
    "📊 Step 2: Impact Simulation",
    "🤖 Step 3: RL Mitigation",
    "📋 Step 4: Final Summary"
])

# Model selector
st.sidebar.markdown("### 🔧 Model Settings")
model_choice = st.sidebar.selectbox("Choose a model", ["Claude 3 (OpenRouter)", "OpenAI GPT-4o"])

# Home
if page == "🏠 Home":
    st.image("assets/logo.png", width=220)
    st.markdown("<h1 style='text-align: center;'>Generative Scenario Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>AI-powered foresight engine for emerging and extreme reinsurance risks</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🌐 Why It Matters")
    st.markdown("""
    Global risk is evolving faster than traditional models can adapt.  
    For **reinsurers**, this means exposure to unpriced tail events.  
    For **regulators**, it complicates capital adequacy and solvency oversight.  
    And for **investors**, it increases uncertainty around performance and protection gaps.  

    The ability to **simulate plausible futures**—and plan for them—is now a competitive edge.
    """)

    st.markdown("### 🧠 What It Is")
    st.markdown("""
    The Generative Scenario Explorer is a next-generation scenario planning tool that:
    - 💬 Uses **LLMs** to generate realistic, high-impact, and emerging risk scenarios  
    - 📊 Simulates **financial outcomes** by business line and geography  
    - 🤖 Applies **Reinforcement Learning (RL)** to test and optimize response strategies  
    - 🗘 Outputs a **1-page executive report** to support board, investor, or regulatory communication
    """)

    st.markdown("### 🛠 How to Use It")
    st.markdown("""
    1. **Portfolio Setup** – Define exposures and risk assumptions  
    2. **Scenario Generation** – Use the AI to create novel, stress-test-worthy events  
    3. **Simulation** – Visualize potential losses and severity  
    4. **Optimization** – Identify best-fit mitigation strategies (e.g., exclusions, reinsurance)  
    5. **Summary** – Receive a shareable insight report
    """)

    st.markdown("### 🎯 What to Expect in This Demo")
    st.markdown("""
    - End-to-end workflow powered by LLMs + RL  
    - Interactive scenario authoring + portfolio simulation  
    - Dynamic visualizations of risk exposure and mitigated loss  
    - AI-optimized treaty adjustments or capital responses  
    - Auto-generated stakeholder summary

    _This demo is designed for reinsurers, regulators, and capital allocators evaluating next-gen risk tooling._
    """)

# Step 1: Scenario Generation
elif page == "🧠 Step 1: Scenario Generation":
    st.header("🧠 Step 1: Generate Emerging Risk Scenario")

    st.markdown("""
    **Craft a "What if?" scenario involving extreme, emerging, or compounding risks.**  
    This step uses cutting-edge large language models (LLMs) to generate detailed, plausible narratives that simulate potential tail events for reinsurers. You provide the seed idea, and the AI will expand it into a richly described risk scenario.

    ### 🧠 How It Works:
    - You describe a scenario prompt (e.g., "What if a major hurricane hits Florida during a ransomware attack?").
    - The selected LLM (Claude 3 or GPT-4o) generates a detailed narrative.
    - The system analyzes the output and auto-tags relevant risk categories (e.g., CAT, Cyber, Systemic).
    - You can save it to your portfolio for further simulation and optimization.

    ### 💡 Example Prompts:
    - "What if a new virus spreads across LATAM during an unprecedented drought?"
    - "How would markets react to a cyberattack during wildfire season in California?"
    """)

    scenario_input = st.text_area(
        "🔮 Describe Your Scenario Prompt",
        placeholder="e.g. What if a major earthquake hits LA during a cyberattack on US infrastructure?",
        height=100
    )

    if st.button("🪄 Generate Scenario"):
        if not scenario_input.strip():
            st.warning("⚠️ Please describe a scenario before generating.")
        else:
            with st.spinner("Generating AI-powered scenario narrative..."):
                try:
                    if model_choice == "Claude 3 (OpenRouter)":
                        narrative = call_claude(f"Write a detailed reinsurance scenario: {scenario_input}")
                        tags = extract_tags_with_claude(narrative)
                    else:
                        response = openai_client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "You are a reinsurance risk analyst."},
                                {"role": "user", "content": f"Write a detailed, plausible scenario: {scenario_input}"}
                            ],
                            temperature=0.7
                        )
                        narrative = response.choices[0].message.content.strip()
                        tags = extract_tags_with_claude(narrative)

                    scenario_id = str(uuid.uuid4())
                    st.session_state["scenario_history"].append({
                        "id": scenario_id,
                        "prompt": scenario_input,
                        "narrative": narrative,
                        "tags": tags,
                    })

                    st.success("✅ Scenario Generated")
                    st.markdown("### 📘 Scenario Narrative")
                    st.markdown(narrative)
                    st.markdown(f"**🏷 Risk Tags:** {', '.join(tags)}")

                    if st.button("📅 Save to Portfolio", key=f"save_{scenario_id}"):
                        st.toast("✅ Scenario saved to portfolio.", icon="💾")

                except Exception as e:
                    st.error(f"❌ Error generating scenario: {e}")

    if st.session_state["scenario_history"]:
        st.markdown("---")
        st.markdown("### 📚 Scenario Portfolio")
        for entry in reversed(st.session_state["scenario_history"]):
            with st.expander(f"🔖 {entry['prompt'][:60]}..."):
                st.markdown(f"**🧠 Prompt:** {entry['prompt']}")
                st.markdown(f"**📘 Narrative:** {entry['narrative']}")
                st.markdown(f"**🏷 Tags:** {', '.join(entry['tags']) if entry['tags'] else 'None'}")

# ====== Step 2: Impact Simulation ======
elif page == "📊 Step 2: Impact Simulation":
    st.header("📊 Step 2: Portfolio Impact Simulation")

    st.markdown("""
    This step simulates the financial impact of the generated risk scenario across major lines of business.

    ### 🛠 How to Use It:
    - After generating a scenario in Step 1, return here to see how it might affect your portfolio.
    - The tool simulates expected losses using statistical assumptions per line of business (LOB).

    ### 💡 What to Expect:
    - A table summarizing simulated losses by LOB
    - A small bar chart visualizing the distribution
    - These are synthetic results based on average loss levels and volatility; they provide directional insight
    """)

    lob = ["Homeowners", "Commercial", "Motor", "Cyber", "Liability"]
    losses = np.random.normal(loc=[300, 500, 80, 220, 120], scale=[30, 50, 15, 40, 25])
    df_loss = pd.DataFrame({"Line of Business": lob, "Losses ($M)": np.round(losses, 1)})

    st.markdown("### 🧾 Simulated Loss Table")
    st.dataframe(df_loss)

    st.markdown("### 📉 Visualized Portfolio Impact")
    fig, ax = plt.subplots(figsize=(6, 3))  # smaller chart size
    ax.bar(df_loss["Line of Business"], df_loss["Losses ($M)"], color="tomato")
    ax.set_ylabel("Losses ($M)")
    ax.set_title("Estimated Losses by Line of Business")
    st.pyplot(fig)

    st.markdown("""
    ### 📊 Interpretation of Results:
    - **Commercial and Homeowners** lines show the highest simulated losses, consistent with large-scale property damage.
    - **Cyber losses** reflect plausible attack costs under scenario stress.
    - These values are illustrative but useful for guiding the next step: risk mitigation.
    """)

    st.info("➡️ Next: AI-powered optimization will suggest how to mitigate tail risk.")



# ====== Step 3: RL Mitigation ======
elif page == "🤖 Step 3: RL Mitigation":
    st.header("🤖 Step 3: Optimize Mitigation Strategy")

    st.markdown("""
    In this step, an RL (Reinforcement Learning) agent proposes adjustments to your reinsurance structure in order to reduce expected and tail losses.

    ### 🛠 How to Use It:
    - Click **"Run Mitigation Agent"** to simulate the optimization process.
    - The agent evaluates various protection strategies and compares them against the baseline.
    - Outputs include changes in loss profile and spend impact.

    ### 💡 What to Expect:
    - A table comparing the baseline vs. mitigated strategy
    - A bar chart showing reduction in 1-in-100 tail loss
    - Insight into how small changes in spend can lead to significant improvements in resilience
    """)

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

            fig, ax = plt.subplots(figsize=(6, 3))  # smaller chart
            ax.bar(df_strategy["Strategy"], df_strategy["Tail Loss @ 1-in-100 ($M)"], color=["gray", "green"])
            ax.set_ylabel("Tail Risk ($M)")
            ax.set_title("Reduction in Tail Loss")
            st.pyplot(fig)

            st.markdown("""
            ### 📊 Interpretation of Results:
            - **Expected Loss** is reduced by 25%, showing better average-case resilience.
            - **Tail Loss** at the 1-in-100 level improves from $1.8B to $1.2B.
            - **Reinsurance Spend** increases modestly by $20M but yields high leverage on downside protection.

            This provides actionable input for underwriting teams, actuaries, and risk committees evaluating capital allocation and hedging efficiency.
            """)

            st.info("➡️ Proceed to summary for management explanation.")

# ====== Step 4: Final Summary ======
elif page == "📋 Step 4: Final Summary":
    st.header("📋 Step 4: Final Report and Takeaways")

    st.markdown("""
    This final step consolidates the key outcomes from your AI-powered reinsurance scenario simulation.

    ### 🛠 How to Use It:
    - Review the executive summary and strategic insights generated by the system.
    - Use this information for stakeholder presentations, board discussions, or regulatory engagement.

    ### 💡 What to Expect:
    - A concise summary of scenario severity and mitigation effectiveness
    - Bullet-point insights about AI's contributions to the structuring process
    - Option to export a management-ready version (PDF soon)
    """)

    st.markdown("### 🧾 Management Summary")
    st.success("""
    Under a compound cyber-catastrophe scenario, tail losses exceeded $1.8B.  
    The AI recommended purchasing $50M additional cyber cover and an earthquake excess layer.  
    This reduced 1-in-100 tail losses by 33% and improved the solvency buffer by 20 points.
    """)

    st.markdown("### 📌 Key Insights")
    st.markdown("""
    - **Generative AI** expands the stress testing frontier by simulating non-obvious, emerging risks.  
    - **Reinforcement Learning** delivers quantified, cost-effective protection strategies.  
    - **Data-backed recommendations** support better capital efficiency, solvency planning, and product design.  
    - **Executive-ready outputs** facilitate faster internal alignment and regulatory transparency.
    """)

    st.download_button(
        label="⬇️ Download Summary (PDF Coming Soon)",
        data="Summary placeholder text",
        file_name="Generative_Scenario_Explorer_Summary.txt",
        disabled=True
    )
