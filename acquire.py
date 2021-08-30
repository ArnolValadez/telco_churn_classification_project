from env import host, password, user, get_connection
import pandas as pd
import numpy as np
import os

def get_telco_data():

    my_query = ''' SELECT c.*, pt.payment_type, ist.internet_service_type, ct.contract_type
    FROM customers as c
    JOIN payment_types as pt on c.payment_type_id = pt.payment_type_id
    JOIN internet_service_types AS ist on ist.internet_service_type_id = c.internet_service_type_id
    JOIN contract_types as ct ON ct.contract_type_id = c.contract_type_id;'''

    filename = "telco_data.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        telco_df = pd.read_sql(my_query, get_connection('telco_churn'))
        telco_df.to_csv(filename, index = False)
        
    return telco_df