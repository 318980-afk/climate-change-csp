import matplotlib.pyplot as plt
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'crops.csv')
df = pd.read_csv(csv_path)

#hypothesis: how do CO2 emissions, total precipitation, and irrigation access affects crop yield of fruits?

#code to highlight, to line 20
start_year = 2000
end_year = 2025
crop = "Corn"
df_crop = df[df["Crop_Type"] == crop]
df_crop = df_crop[(df_crop["Year"] >= start_year) & (df_crop["Year"] <= end_year)]

'''
avg_yield = df_crop["Crop_Yield_MT_per_HA"].mean()
min_yield = df_crop["Crop_Yield_MT_per_HA"].min()
max_yield = df_crop["Crop_Yield_MT_per_HA"].max()
'''

unique_countries = df['Country'].unique()

region_counts = df_crop["Region"].value_counts() #gets the number of times each region appears in the dataset
top_regions = region_counts.head(5).index.tolist() #gets top 5 regions that appear the most in the dataset

year_region_avg = (
    df_crop[df_crop["Region"].isin(top_regions)] #filters the dataset to only include rows where the region is in the top 5 regions
    .groupby(["Year", "Region"])["Crop_Yield_MT_per_HA"] #all rows with same year and region are grouped together 
    .mean() #average crop yield for each region and year group
    .reset_index() #converts the grouped data back into clean columns
)

#Visualization #1 for crop yield over time for top 5 regions
plt.figure(figsize=(8, 5))
for region in top_regions:
    region_data = year_region_avg[year_region_avg["Region"] == region] #filters new dataset to only rows for each top 5 region
    plt.plot(region_data["Year"], region_data["Crop_Yield_MT_per_HA"], marker="o", label=region) #plots each region's average crop yield over time

plt.title(crop + " Yield Over Time (Top 5 Regions)")
plt.xlabel("Year")
plt.ylabel("Average Crop Yield (MT/HA)")
plt.legend()
plt.show()

#Visualization #2 for CO2 emissions vs crop yield
scatter_df = df_crop[df_crop["Total_Precipitation_mm"] <= 3000]

plt.figure(figsize=(8, 5))
plt.scatter(scatter_df["Total_Precipitation_mm"], scatter_df["Crop_Yield_MT_per_HA"])
plt.title(crop +  " Yield vs Total Precipitation")
plt.xlabel("Total Precipitation (mm)")
plt.ylabel("Crop Yield (MT/HA)")
plt.show()

#Visualization #3 for irrigation access vs crop yield
irrig_df = df_crop.dropna(subset=["Irrigation_Access_%"]) #removes rows with missing irrigation access data
def irrigation_bin(pct):
    if pct < 20:
        return "0-20"
    elif pct < 40:
        return "20-40"
    elif pct < 60:
        return "40-60"
    elif pct < 80:
        return "60-80"
    else:
        return "80-100"

irrig_df["Irrigation_Bin"] = irrig_df["Irrigation_Access_%"].apply(irrigation_bin) #creates new column that categorizes irrigation access into 5 bins based on percentage

bin_avg_yield = irrig_df.groupby("Irrigation_Bin")["Crop_Yield_MT_per_HA"].mean() #mean crop yield for each irrigation access bin

bin_order = ["0-20", "20-40", "40-60", "60-80", "80-100"]
bin_avg_yield = bin_avg_yield.reindex(bin_order) #reorders the bins in the order of percentage

plt.figure(figsize=(8, 5))
plt.bar(bin_avg_yield.index, bin_avg_yield.values)
plt.title(crop + " Yield by Irrigation Access (20% bins)")
plt.xlabel("Irrigation Access (%)")
plt.ylabel("Average Crop Yield (MT/HA)")
plt.show()

# Visualization 4: CO2 emissions vs crop yield
co2_df = df_crop.dropna(subset=["CO2_Emissions_MT", "Crop_Yield_MT_per_HA"]).copy() #removes rows with missing CO2 emissions or crop yield data

co2_cap = co2_df["CO2_Emissions_MT"].quantile(0.99) #sets a cap to 99th percentile of CO2 emissions to remove extreme outliers
co2_df = co2_df[co2_df["CO2_Emissions_MT"] <= co2_cap] #keeps rows where CO2 emissions are within the cap

num_bins = 12
co2_df["CO2_Bin"] = pd.cut(co2_df["CO2_Emissions_MT"], bins=num_bins) #creates new column categorizing the CO2 emissions to 12 bins based on the range of data

co2_bin_avg = co2_df.groupby("CO2_Bin")["Crop_Yield_MT_per_HA"].mean().reset_index() #calculates avg crop yield for each bin and converts back to clean columns

co2_bin_avg["CO2_Midpoint"] = co2_bin_avg["CO2_Bin"].apply(lambda b: (b.left + b.right) / 2) #new column that calculates the crop yield midpoint of each CO2 bin for plotting

plt.figure(figsize=(8, 5))
plt.plot(co2_bin_avg["CO2_Midpoint"], co2_bin_avg["Crop_Yield_MT_per_HA"], marker="o")
plt.title(crop + " Yield vs CO2 Emissions")
plt.xlabel("CO2 Emissions (MT)")
plt.ylabel("Average Crop Yield (MT/HA)")
plt.show()
