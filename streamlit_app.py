import streamlit as st
import pandas as pd

# Function to fill missing values for each record id
def autofill(df, columns):
    for column in columns:
        df[column] = df.groupby('record_id')[column].ffill().bfill()
    return df

# Function to count non-null observations for each variable at each timepoint
def longitudinal_filter(df, timepoint_col, variables):
    # Assuming timepoint_col is a column in your dataset that denotes the timepoint
    grouped = df.groupby(timepoint_col)
    result = {}
    
    for timepoint, group_data in grouped:
        counts = {}
        for var in variables:
            counts[var] = group_data[var].notna().sum()
        result[timepoint] = counts
    
    return result

# Example dataset (replace with your actual dataset loading mechanism)
data = pd.read_excel("PRODRSOMDashboardDat_DATA_2024-06-04_1845.xlsx")

# Example variables (replace with your actual list of variables)
variables = [
    "insurance_dashboard_use", "ikdc", "pedi_ikdc", "marx", "pedi_fabs", "koos_pain", 
    "koos_sx", "koos_adl", "koos_sport", "koos_qol", "acl_rsi", "tsk", "rsi_score", 
    "rsi_emo", "rsi_con", "sh_lsi", "th_lsi", "ch_lsi", "lsi_ext_mvic_90", 
    "lsi_ext_mvic_60", "lsi_flex_mvic_60", "lsi_ext_isok_60", "lsi_flex_isok_60", 
    "lsi_ext_isok_90", "lsi_flex_isok_90", "lsi_ext_isok_180", "lsi_flex_isok_180", 
    "rts", "reinjury"
]

# Filter data and count observations for each timepoint
filtered_data = autofill(data, ['sex_dashboard', 'graft_dashboard2', 'prior_aclr'])
timepoint_col = 'tss'  # Replace with your actual timepoint column name

# Calculate counts for each variable at each timepoint
longitudinal_counts = longitudinal_filter(filtered_data, timepoint_col, variables)

# Display results in a table format
st.write("Counts of Non-Null Observations for Variables at Each Timepoint:")
for timepoint, counts in longitudinal_counts.items():
    st.subheader(f"Timepoint: {timepoint}")
    df_counts = pd.DataFrame.from_dict(counts, orient='index', columns=['Count'])
    st.write(df_counts)
