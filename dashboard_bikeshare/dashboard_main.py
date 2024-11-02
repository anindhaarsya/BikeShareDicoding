import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_monthly_rentals(daily_df):
    month_daily = daily_df.groupby(by=['mnth'],sort=False).agg({
    "cnt":"sum"
    }).reset_index()
    
    return month_daily

def create_weekly_rentals(daily_df):
    weekly_daily = daily_df.groupby(by=['weekday'],sort=False).agg({
    "cnt":"sum"
    }).reset_index()
    
    return weekly_daily

def create_atemp_category(daily_df):
    atemp_category_daily = daily_df.groupby(by=['atemp_category'],sort=False).agg({
    "cnt":"sum"
    }).reset_index()
    
    return atemp_category_daily

def create_users_total(daily_df):
    users_total = daily_df.groupby(by=['yr']).agg({
        "casual": "sum",
        "registered": "sum"
    }).reset_index()
    return users_total

def create_seasonal_daily(daily_df):
    total_per_season = daily_df.groupby(by=['season']).agg({
        "cnt": "sum"
    }).reset_index()
    return total_per_season

def create_weather_daily(daily_df):
    total_weather = daily_df.groupby(by=['weathersit']).agg({
        "cnt": "sum"
    }).reset_index()
    return total_weather

day_df_after = pd.read_csv("day_after_clean.csv")

with st.sidebar:
    st.image("bike-logo.png")
    
    selected_year = st.selectbox(
        label="Year",
        options=(2011,2012)
    )

st.header('Bike Sharing Analysis Dashboard :bike:')

st.subheader('Bike Sharing Analysis {selected_year}'.format(selected_year=selected_year))

daily_df = day_df_after[day_df_after['yr'] == selected_year]
col1, col2 = st.columns(2)

count_sum = day_df_after[day_df_after['yr'] == 2011]['cnt'].sum()
difference = daily_df['cnt'].sum() - count_sum

mean_2011 = day_df_after[day_df_after['yr'] == 2011]['cnt'].mean().round(2)
mean_2012 = day_df_after[day_df_after['yr'] == 2012]['cnt'].mean().round(2)
avg_mean = ((mean_2012 - mean_2011) / mean_2011).round(2) * 100

with col1:
    jml_bike_sharing = day_df_after['cnt'].sum()
    if selected_year == 2012:
        st.metric("Count", value=jml_bike_sharing, delta=str(difference))
    else:
        st.metric("Count", value=jml_bike_sharing)

with col2:
    if selected_year == 2012:
        st.metric("Average", value=mean_2012, delta=str("+{avg_mean}%".format(avg_mean=avg_mean)))
    else:
        st.metric("Average", value=mean_2011)    

monthly_rentals = create_monthly_rentals(daily_df)

st.subheader(f"Monthly Rentals Trend for {selected_year}")
plt.figure(figsize=(14, 6))
sns.lineplot(data=monthly_rentals, x="mnth", y="cnt", marker="o", linewidth=2.5, color="orange")

offset = -15
for x, y in zip(monthly_rentals["mnth"], monthly_rentals["cnt"]):
    plt.text(x, y, f"{y:,}", ha="center", va="bottom", fontsize=10, color="black")

plt.title(f"Total Monthly Bike Rentals in {selected_year}")
plt.xlabel("Month")
plt.ylabel("Total Rentals")

st.pyplot(plt)

weekly_rentals = create_weekly_rentals(daily_df)

st.subheader(f"Weekly Rentals Trend for {selected_year}")
plt.figure(figsize=(14, 6))
sns.lineplot(data=weekly_rentals, x="weekday", y="cnt", marker="o", linewidth=3.5, color="purple")

offset = -15
for x, y in zip(weekly_rentals["weekday"], weekly_rentals["cnt"]):
    plt.text(x, y, f"{y:,}", ha="center", va="bottom", fontsize=10, color="black")

plt.title(f"Total Weekly Bike Rentals in {selected_year}")
plt.xlabel("Weekday")
plt.ylabel("Total Rentals")

st.pyplot(plt)

st.subheader(f"Rentals by Season and Weather for {selected_year}")

col1, col2 = st.columns(2)

with col1:
    total_per_season = create_seasonal_daily(daily_df)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(data=total_per_season, x="season", y="cnt", color="#9370db")
    plt.title(f"Total Rentals by Season in {selected_year}")
    plt.xlabel("Season")
    plt.ylabel("Total Per Season")
    
    st.pyplot(plt)

with col2:
    total_weather = create_weather_daily(daily_df)
    plt.figure(figsize=(8, 6))
    sns.barplot(data=total_weather, x="weathersit", y="cnt", color="#50c878")
    plt.title(f"Total Rentals by weather in {selected_year}")
    plt.xlabel("Weather")
    plt.ylabel("Total Per Weather")
    
    st.pyplot(plt)
    
atemp_category_daily= create_atemp_category(daily_df)
    
st.subheader(f"Rentals by temperature(feels-like) for {selected_year}")
plt.figure(figsize=(14, 6))
sns.barplot(data=atemp_category_daily, x="atemp_category", y="cnt", color="#ff8c00")
plt.title(f"Total Rentals by temperatur(feels-like) in {selected_year}")
plt.xlabel("atemp")
plt.ylabel("Total Per atemp")
    
st.pyplot(plt)

users_total= create_users_total(daily_df)
    
st.subheader(f"Rentals by Users for {selected_year}")
plt.figure(figsize=(10, 5))
sns.barplot(data=users_total, x="yr", y="casual", color="#ff8c00", label="Casual")
sns.barplot(data=users_total, x="yr", y="registered", color="#50c878", label="Registered", alpha=0.7)
plt.title(f"Total Rentals by Users in {selected_year}")
plt.xlabel("Tahun")
plt.ylabel("Category users")

plt.tight_layout()    
st.pyplot(plt)