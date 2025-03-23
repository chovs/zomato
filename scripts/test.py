from scripts.data_ingestion import load_data
from scripts.data_cleaning import clean_missing_values
from scripts.data_validation import validate_ids,validate_delivery_person_ids

raw_data = load_data("data/raw/Zomato Dataset.csv")

print(raw_data.head())


# clean the data 

# Clean missing values in multiple columns

raw_data['delivery_person_age'] = clean_missing_values(raw_data['delivery_person_age'], fill_value=0)     # Clean 'price' column

# looking for the next step about what processed new raw data object is 


# validate the data 
validation_results = validate_and_return(raw_data)
print(len(validation_results))

# cut out the id column
# differ in the notebook file



# loop of clean and EDA - 





# loop of EDA and modeling