from sqlalchemy import create_engine
from .extract import extract 
import pandas as pd
import re



def convert_duration_if_colon(s):
        if ":" in s:
            s_no_dot = s.replace(".", "")
            s_fixed = re.sub(r":", ".", s_no_dot, count=1)
            return float(s_fixed)
        else:
            return float(s)

def transform(dataFrame):
    #Check for unique values to make sure missing entries aren't represented differently (e.g., '\N', 'None', '', etc.)
    for col in formulaDF.columns:
        print(f"\nColumn: {col}")
        print("Unique count: ", formulaDF[col].nunique())
        print("Values: ", formulaDF[col].unique())
        print("Data type: ", formulaDF[col].dtype)
        print("Null counts: ", formulaDF[col].isna().sum())


    null_values = ['\\N', 'nan', 'NaN', '', 'None']

    # Iterate through all columns and replace any non-standard null indicators ('\N') 
    # with Pandas NA (pd.NA), so that all missing values are consistently recognized as nulls.
    for col in formulaDF.columns:
        formulaDF[col] = formulaDF[col].replace(null_values, pd.NA)
        print(f"\nColumn: {col}")
        print("Null counts: ", formulaDF[col].isna().sum())

    


    #Convert time values to appropriate format
    formulaDF["milliseconds"] = pd.to_numeric(formulaDF["milliseconds"], errors="coerce")
    formulaDF["time"] = (
        pd.to_timedelta(formulaDF["milliseconds"], unit="ms")
        .astype(str)
        .str.replace("0 days ", "")
        .str[:-3]
    )

    #Drop NA values from these columns as they will not impact analysis
    formulaDF.dropna(subset=['fastestLap', 'fastestLapTime', 'fastestLapSpeed'], inplace=True)

    #Convert to integer in order to fill missing values with median
    formulaDF['alt'] = pd.to_numeric(formulaDF['alt'], errors='coerce').astype('Int64')
    formulaDF['alt'] = formulaDF['alt'].fillna(formulaDF['alt'].median())

    #Format all records that have time like '18:56.074'
    formulaDF["duration"] = formulaDF["duration"].apply(convert_duration_if_colon)
        
    return formulaDF

if __name__ == "__main__":
    formulaDF = extract()
    transform(formulaDF)


