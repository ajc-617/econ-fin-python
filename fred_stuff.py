import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

men_df = pd.read_csv("men_real_median_wages.csv")
women_df = pd.read_csv("women_real_median_wages.csv")


men_df["date"] = pd.to_datetime(men_df["observation_date"])
women_df["date"] = pd.to_datetime(women_df["observation_date"])
#dataframe containing difference between wage in each quarter
difference_df = men_df["LES1252881900Q"] - women_df["LES1252882800Q"]
percent_df = men_df["LES1252881900Q"] / women_df["LES1252882800Q"] * 100 - 100
fig, ax1 = plt.subplots()
ax1.plot(men_df["date"], men_df["LES1252881900Q"])
ax1.plot(women_df["date"], women_df["LES1252882800Q"], color="red")
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