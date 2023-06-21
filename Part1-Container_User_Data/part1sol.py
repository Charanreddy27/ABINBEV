import pandas as pd
import numpy as np

# Step 1: Load the required data
actuals = pd.read_csv('actuals.csv')
target = pd.read_csv('targets.csv')
price = pd.read_csv('price.csv')
bcr = pd.read_csv('b&cr.csv')

# Step 2: Clean the datasets (if needed)
#fill the null values with "0"
actual_data = actuals.fillna(0)
price_data = price.fillna(0)
bcr_data = b_cr.fillna(0)
target_data = target.fillna(0)

#Replace the values filled by "0" with the mean values
actual_mean=actual_data.fillna(actuals.mean())
price_mean = price_data.fillna(price.mean())
bcr_mean = bcr_data.fillna(b_cr.mean())
target_mean = target_data.fillna(target.mean())

#Merge actuals data and price data based on Material Description
merged_df = pd.merge(actual_mean, price_mean, on='Material Description')

#Handling the duplicate plant value creation
merged_df['Plant'] = merged_df['Plant_x'].fillna(merged_df['Plant_y'])
merged_df.drop(['Plant_x', 'Plant_y'], axis=1, inplace=True)

#renaming the material number as material descriptiona as material number
merged_df = merged_df.rename(columns={'Material Description':'Material Number'})

#Merge the bcr file with merged data
merge_bcr = pd.merge(merged_df, bcr_mean, on=['Material Number'])

# Step 3: Create a consolidated view of the Actuals data
consolidated_actuals = actuals_mean.merge(price_mean, on=['Plant', 'Material Description'], how='left')
consolidated_actuals['Bottle Rands'] = consolidated_actuals['Price per case '] * consolidated_actuals['Quantity']
consolidated_actuals['Crate Rands'] = consolidated_actuals['Crate Price'] * consolidated_actuals['Quantity']

# Step 4: Variance analyses
variance_analysis = actuals_mean.merge(target_mean, on=['Year', 'Period', 'Plant', 'Material Number'], suffixes=('_Actual', '_Target'))

# Step 5: Actuals & Target analysis by Plant and Category
actuals_target_analysis = consolidated_actuals.groupby(['Plant', 'Category']).agg({
    'Amount in LC': 'sum',
    'Target Value in LC': 'sum'
}).reset_index()

# Step 6: Actuals, Target & variance analysis by Plant and Category
actuals_target_variance = consolidated_actuals.merge(target, on=['Year', 'Period', 'Plant', 'Material Number'], suffixes=('_Actual', '_Target'))
actuals_target_variance['Variance'] = actuals_target_variance['Amount in LC'] - actuals_target_variance['Target Value in LC']

# Step 7: Trend analysis for each Category and Plant
trend_analysis = consolidated_actuals.groupby(['Category', 'Plant']).agg({
    'Period': 'count',
    'Amount in LC': 'sum'
}).reset_index()

# Step 8: Identify focus areas and planning periods for smooth supply
# Analyze the variance, trend, and overall performance metrics to identify focus areas and planning periods.

# Print the consolidated view of Actuals data
print("Consolidated Actuals Data:")
print(consolidated_actuals)

# Print the variance analysis
print("Variance Analysis:")
print(variance_analysis)

# Print the Actuals & Target analysis by Plant and Category
print("Actuals & Target Analysis by Plant and Category:")
print(actuals_target_analysis)

# Print the Actuals, Target & variance analysis by Plant and Category
print("Actuals, Target & Variance Analysis by Plant and Category:")
print(actuals_target_variance)

# Print the Trend analysis for each Category and Plant
print("Trend Analysis for each Category and Plant:")
print(trend_analysis)


