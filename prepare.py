# Prepare the telco dataset before beginning exploration.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# turn off warnings
import warnings
warnings.filterwarnings("ignore")

# The prep function returns the train, validate and test splits:
def prep_telco_data(df):
       
    # Use booleans to change type of variable to int in streaming columns
    df.online_security = (df.online_security == 'Yes').astype(int)
    df.online_backup = (df.online_backup == 'Yes').astype(int)
    df.device_protection = (df.device_protection == 'Yes').astype(int)
    df.tech_support = (df.tech_support == 'Yes').astype(int)
    df.streaming_tv = (df.streaming_tv == 'Yes').astype(int)
    df.streaming_movies = (df.streaming_movies == 'Yes').astype(int)
    df.streaming_movies = (df.streaming_movies == 'Yes').astype(int)
    df.multiple_lines = (df.multiple_lines == 'Yes').astype(int)
    df.partner = (df.partner == 'Yes').astype(int)
    df.dependents = (df.dependents == 'Yes').astype(int)
    df.phone_service = (df.phone_service == 'Yes').astype(int)
    df.paperless_billing = (df.paperless_billing == 'Yes').astype(int)

    # Creating dummy columns for these multi-type columns:
    service_dum = pd.get_dummies(df.contract_type)
    internet_dum = pd.get_dummies(df.internet_service_type)
    df = pd.concat([df, service_dum, internet_dum], axis = 1)
    df.rename(columns = {'Month-to-month': 'month_to_month', 'One year': 'one_year', 'Two year': 'two_year', 'DSL': 'dsl_internet', 'Fiber optic': 'fiber_internet', 'None': 'no_internet'}, inplace = True)

    # Creating column to check if customer is female. Don't need two columns since this dataset only has female/male; thus if not a female == 0, means the customer is a male.
    df['is_female'] = df.gender == "Female"
    df.is_female.replace([True, False], [1,0], inplace = True)

    # Dealing with the 11 blank values that are in the total_charges column. Since these are new customers and didn't yet attain 1 month of tenure, they don't have any total charges. However they are all locked in to 1 year and 2 year contracts, so we expect that they will at least finish out their contract period (That's an assumption). 
    # In this case, we removed the blanks and simply replaced the blanks with a 0 (float), since all 11 of these customers hadn't been here a month yet, so there wouldn't be a reason to imput their total cost as anything other as 0.
    df.total_charges = df.total_charges.str.replace(' ', '0').astype(float)
    df.total_charges.dtype
    
    # Adding a column that tells us if the customer pays automatically or manually.
    # is_automatic, 1 = True, 0 = False.
    df['is_automatic'] = df.payment_type.replace(["Mailed check", "Electronic check", "Credit card (automatic)", "Bank transfer (automatic)"], [0,0,1,1])
    
    # Now, adding a dummy column for the churn column, which will be my target variable for this analysis:
    df['churned'] = df.churn.replace(["Yes", "No"], [1,0])
    
    
    # Finally, splitting my data:
    
    train_validate, test = train_test_split(df, test_size=.2, 
                                            random_state=123, 
                                            stratify=df.churned)
    # Splitting the train_validate set into the separate train and validate datasets.
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=123, 
                                   stratify=train_validate.churned)
    return train, validate, test

# Prep function returning the entire dataset, no splits.
def prep_telco_data_all(df):
       
    # Use booleans to change type of variable to int in streaming columns
    df.online_security = (df.online_security == 'Yes').astype(int)
    df.online_backup = (df.online_backup == 'Yes').astype(int)
    df.device_protection = (df.device_protection == 'Yes').astype(int)
    df.tech_support = (df.tech_support == 'Yes').astype(int)
    df.streaming_tv = (df.streaming_tv == 'Yes').astype(int)
    df.streaming_movies = (df.streaming_movies == 'Yes').astype(int)
    df.streaming_movies = (df.streaming_movies == 'Yes').astype(int)
    df.multiple_lines = (df.multiple_lines == 'Yes').astype(int)
    df.partner = (df.partner == 'Yes').astype(int)
    df.dependents = (df.dependents == 'Yes').astype(int)
    df.phone_service = (df.phone_service == 'Yes').astype(int)
    df.paperless_billing = (df.paperless_billing == 'Yes').astype(int)

    # Creating dummy columns for these multi-type columns:
    service_dum = pd.get_dummies(df.contract_type)
    internet_dum = pd.get_dummies(df.internet_service_type)
    df = pd.concat([df, service_dum, internet_dum], axis = 1)
    df.rename(columns = {'Month-to-month': 'month_to_month', 'One year': 'one_year', 'Two year': 'two_year', 'DSL': 'dsl_internet', 'Fiber optic': 'fiber_internet', 'None': 'no_internet'}, inplace = True)

    # Creating column to check if customer is female. Don't need two columns since this dataset only has female/male; thus if not a female == 0, means the customer is a male.
    df['is_female'] = df.gender == "Female"
    df.is_female.replace([True, False], [1,0], inplace = True)
    
    # Dealing with the 11 blank values that are in the total_charges column. Since these are new customers and didn't yet attain 1 month of tenure, they don't have any total charges. However they are all locked in to 1 year and 2 year contracts, so we expect that they will at least finish out their contract period (That's an assumption). 
    # In this case, we removed the blanks and simply replaced the blanks with a 0 (float), since all 11 of these customers hadn't been here a month yet, so there wouldn't be a reason to imput their total cost as anything other as 0.
    df.total_charges = df.total_charges.str.replace(' ', '0').astype(float)
    df.total_charges.dtype
    
    # Adding a column that tells us if the customer pays automatically or manually.
    # is_automatic, 1 = True, 0 = False.
    df['is_automatic'] = df.payment_type.replace(["Mailed check", "Electronic check", "Credit card (automatic)", "Bank transfer (automatic)"], [0,0,1,1])
    
    # Now, adding a dummy column for the churn column, which will be my target variable for this analysis:
    df['churned'] = df.churn.replace(["Yes", "No"], [1,0])

    return df