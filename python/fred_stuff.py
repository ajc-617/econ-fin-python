import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

MEN_REAL_MEDIAN_WAGES_FRED_CODE = "LES1252881900Q"
WOMEN_REAL_MEDIAN_WAGES_FRED_CODE = "LES1252882800Q"
FRED_API_KEY = open("fred_api_key.txt", "r").read().strip()

def main():

    men_df = get_fred_data(MEN_REAL_MEDIAN_WAGES_FRED_CODE)
    women_df = get_fred_data(WOMEN_REAL_MEDIAN_WAGES_FRED_CODE)

    #Convert observation_date to datetime
    men_df["date"] = pd.to_datetime(men_df["observation_date"])
    women_df["date"] = pd.to_datetime(women_df["observation_date"])
    #dataframe containing difference between wage in each quarter
    difference_df = men_df["value"] - women_df["value"]
    percent_df = men_df["value"] / women_df["value"] * 100 - 100
    fig, ax1 = plt.subplots()
    ax1.plot(men_df["date"], men_df["value"])
    ax1.plot(women_df["date"], women_df["value"], color="red")
    ax1.plot(men_df["date"], difference_df, color="green")

    ax2 = ax1.twinx()
    ax2.plot(men_df["date"], percent_df, color="purple")
    plt.gcf().autofmt_xdate()  # angled labels so they don’t overlap
    plt.title("Real Median Wages for Men and Women, quarterly, seasonally adjusted")

    # Set axis labels
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Real Median Wages (Seasonally Adjusted)")
    ax2.set_ylabel("Percent Difference")


    # Actually use handle/labels from the real plots
    lines_labels = [ax1.lines[0], ax1.lines[1], ax1.lines[2], ax2.lines[0]]
    labels = ["Men", "Women", "Nominal Difference", "Percent Difference"]

    ax1.legend(lines_labels, labels, loc="upper left")

    plt.show()

def get_fred_data(fred_code):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={fred_code}&api_key={FRED_API_KEY}&file_type=json"
    response = requests.get(url)
    observations = response.json()["observations"]
    dates = [obs["date"] for obs in observations]
    values = [float(obs["value"] )for obs in observations]
    return pd.DataFrame({"observation_date": dates, "value": values})

if __name__ == "__main__":
    main()