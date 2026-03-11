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
    
    null_values = ['\\N', 'nan', 'NaN', '', 'None']

    for col in dataFrame.columns:
        dataFrame[col] = dataFrame[col].replace(null_values, pd.NA)

    #Convert time values to appropriate format
    dataFrame["milliseconds"] = pd.to_numeric(dataFrame["milliseconds"], errors="coerce")
    dataFrame["time"] = (
        pd.to_timedelta(dataFrame["milliseconds"], unit="ms")
        .astype(str)
        .str.replace("0 days ", "")
        .str[:-3]
    )

    #Drop NA values from these columns as they will not impact analysis
    dataFrame.dropna(subset=['fastestLap', 'fastestLapTime', 'fastestLapSpeed'], inplace=True)

    #Convert to integer in order to fill missing values with median
    dataFrame['alt'] = pd.to_numeric(dataFrame['alt'], errors='coerce').astype('Int64')
    dataFrame['alt'] = dataFrame['alt'].fillna(dataFrame['alt'].median())

    #Format all records that have time like '18:56.074'
    dataFrame["duration"] = dataFrame["duration"].apply(convert_duration_if_colon)
        
    return dataFrame

if __name__ == "__main__":
    formulaDF = extract()
    transform(formulaDF)


