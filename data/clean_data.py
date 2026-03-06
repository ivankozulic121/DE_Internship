import pandas as pd
from tabulate import tabulate

pd.set_option('display.max_rows', None)    
pd.set_option('display.max_columns', None)   
pd.set_option('display.width', 2000)        
pd.set_option('display.max_colwidth', None)  



formulaDF = pd.read_csv("C:\\Users\\ivan.kozulic\\Downloads\\dataEngineeringDataset.csv")

#Get columns info 
print(formulaDF.info())


# Check for unique values to make sure missing entries aren't represented differently (e.g., '\N', 'None', '', etc.)
# for col in formulaDF.columns:
#     print(f"\nColumn: {col}")
#     print("Unique count: ", formulaDF[col].nunique())
#     print("Values: ", formulaDF[col].unique())
#     print("Data type: ", formulaDF[col].dtype)
#     print("Null counts: ", formulaDF[col].isna().sum())


# null_values = ['\\N', 'nan', 'NaN', '', 'None']

# # Iterate through all columns and replace any non-standard null indicators ('\N') 
# # with Pandas NA (pd.NA), so that all missing values are consistently recognized as nulls.
# for col in formulaDF.columns:
#     formulaDF[col] = formulaDF[col].replace(null_values, pd.NA)
#     print(f"\nColumn: {col}")
#     print("Null counts: ", formulaDF[col].isna().sum())


# #Convert time values to appropriate format
# formulaDF["milliseconds"] = pd.to_numeric(formulaDF["milliseconds"], errors="coerce")
# formulaDF["time"] = (
#     pd.to_timedelta(formulaDF["milliseconds"], unit="ms")
#     .astype(str)
#     .str.replace("0 days ", "")
#     .str[:-3]
# )

# #Drop NA values from these columns as they will not impact analysis
# formulaDF.dropna(subset=['fastestLap', 'fastestLapTime', 'fastestLapSpeed'], inplace=True)

# #Convert to integer in order to fill missing values with median
# formulaDF['alt'] = pd.to_numeric(formulaDF['alt'], errors='coerce').astype('Int64')
# formulaDF['alt'] = formulaDF['alt'].fillna(formulaDF['alt'].median())










