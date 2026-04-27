# Global Sustainability Dashboard - Adjusted Net Savings
# Authoer: Saviru Samarasinghe 
# Dataset: World Bank Open Data ((Adjusted net savings, including particulate emission damage (% of GNI))

This is my project for the 5DATA004C Data Science Project Lifecycle module at the University of Westminster. 

It's a Streamlit dashboard that visualizes the "Adjusted Net Savings (ANS)" data from the World Bank. The dataset looks at whether countries are depleting their natural wealth or building it, taking into account things like education spending, resource depletion, and pollution damage. A negative ANS generally means a country is consuming more wealth than it creates.

You can check out the live dashboard here: [Streamlit App](https://ans-sustainability-dashboard-bstd3z3qztkjxfn3hugyzt.streamlit.app/)

### Features
The dashboard includes:
- A choropleth map showing the ANS metric around the world over time
- Time series charts to compare different countries
- Bar charts for the top and bottom ranked countries
- Statistical distribution and global trend analysis
- A basic data explorer tool

### Running the project locally

If you want to run this on your own machine, clone the repo and run these commands:

```bash
git clone https://github.com/savirusamarasinghe7676-spec/ans-sustainability-dashboard
cd ans-sustainability-dashboard
pip install -r requirements.txt
streamlit run app.py
```

### Dataset
The data was sourced from the World Bank:
- Indicator: NY.ADJ.SVNG.GN.ZS (Adjusted net savings, including particulate emission damage (% of GNI))
- Link: [World Bank Open Data](https://data.worldbank.org/indicator/NY.ADJ.SVNG.GN.ZS)
- Coverage: 266 economies from 1960 to 2025