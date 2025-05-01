import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- Streamlit Page Setup ---
st.set_page_config(layout="wide")
st.title("🇸🇬 Singapore Commodity Imports")

st.markdown("""
### 📊 About This Dataset

DOWNLOAD dataset HERE: https://data.gov.sg/datasets/d_b89e35ce38cb93a17f5c016e71f50690/view
            
This dataset from [data.gov.sg](https://data.gov.sg) provides:

- **Singapore's merchandise imports**, categorized by **commodity divisions**
- Reported on a **monthly basis**, currently from **January 1976 to March 2025**
- Does **not specify origin countries** — data reflects total imports regardless of source

### 🧭 What is “NES”?

In international trade classification, **NES** = *Not Elsewhere Specified*.  
It means:
- Goods that don't fit into other specific subcategories
- Often includes rare, mixed, or residual goods

📦 Example:
“Mineral Manufactures, NES” might include ceramics, stone, or insulation products that don’t fall under common labels like “glass” or “cement”.

---

### 🧠 Insights You Might Draw:

- **Beverages**: Singapore’s beverage imports have shown a strong upward trend since the 1990s, with notable growth from the early 2000s to 2020, followed by some volatility and a slight decline in recent years.
- **Pharma**: Singapore’s imports of medicinal and pharmaceutical products have surged steadily since 2000, with a dramatic spike around 2020–2022 likely driven by the COVID-19 pandemic and successive epidemics, reaching record highs in recent years.           
- **Fuels & Energy**: May reflect Singapore's lack of natural resources — high fuel imports for power, refining & re-exports
- **Machinery & Electronics**: Often imported for manufacturing or re-export from tech hub
- **Food & Agriculture**: Trends could relate to population growth, supply chains, or policy changes

""")

st.caption("📌 Source: [data.gov.sg](https://data.gov.sg) — Monthly Commodity Division (1976–2025)")

# --- Upload CSV ---
uploaded_file = st.file_uploader("📁 Upload the 'MerchandiseImportsByCommodityDivisionMonthly.csv' file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df.dropna(subset=["DataSeries"])

    df_long = df.melt(id_vars=["DataSeries"], var_name="Month", value_name="Value")
    df_long["Month"] = pd.to_datetime(df_long["Month"] + "01", format="%Y%b%d", errors="coerce")
    df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")
    df_long = df_long.dropna(subset=["Month", "Value"])

    commodity_list = sorted(df_long["DataSeries"].unique())
    selected_commodity = st.selectbox("📦 Select a Commodity Division", commodity_list)

    filtered = df_long[df_long["DataSeries"] == selected_commodity].sort_values("Month")

    st.subheader(f"📈 Monthly Imports: {selected_commodity}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered["Month"], filtered["Value"], marker="o", color="green")
    ax.set_xlabel("Date", labelpad=6)
    ax.set_ylabel("Value (thousands SGD)", labelpad=6)
    ax.set_title(f"Singapore Imports — {selected_commodity}", pad=10)
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout(pad=1.5)
    st.pyplot(fig)

    with st.expander("📋 View Raw Data Table"):
        st.dataframe(filtered)
else:
    st.info("Please upload the CSV file to begin.")
