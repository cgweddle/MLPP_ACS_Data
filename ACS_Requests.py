import requests
import json
import psycopg2

"""
B01001_001E: Total population for sex
B01001_002E: Total Male
B01001_026E: Total female
B05002_001E: Total for place of birth
B05002_003E: Total for born in state of residence
B05002_004E: Total for born in another state
B05002_009E: Total for born outside the US
"""

def connect_to_database():
    conn = psycopg2.connect(
        host = "acs-db.mlpolicylab.dssg.io",
        port = "5432",
        user="mlpp_student",
        password = "CARE-horse-most",
        database = "acs_data_loading",
        options="-c search_path=dbo,acs"
    )
    return conn




def make_get_string(variable_list):
    get = ''
    for v in variable_list:
        get = get + v + ','
    get = get.rstrip(',')
    return get

def get_variable_names(vars):
    variable_types = {}
    for variable in vars:
        if variable == 'Name':
            var_type = 'Text'
            var_name = 'Name'
        else:
            var_call = requests.get(f"https://api.census.gov/data/2019/acs/acs5/variables/{variable}.json")
            var_type = var_call.json()['predicateType']
            var_name = var_call.json()['label']
            var_name = var_name.rstrip(':')
            var_name = var_name.replace(" ", "_")
            var_name = var_name.replace("!!", "_")
            var_name = var_name.replace(":", "")
            if var_type == 'int':
                var_type = 'integer'
        variable_types[var_name] = var_type
    return variable_types
    



if __name__ == '__main__':
    state = '24'
    variables = ['B01001_001E','B01001_002E','B01001_026E','B05002_001E','B05002_003E','B05002_004E','B05002_009E']
    get = make_get_string(variables)
    tablename = "cweddle_acs_data"

    #API Call
    call = f"https://api.census.gov/data/2019/acs/acs5?get={get}&for=block+group:*&in=state:{state}+county:*&key=60f45d14da19259448e4ef39a0f612b15194dbe8"
    response = requests.get(call)
    data = response.json()
    

    #Connect to the database
    conn = psycopg2.connect(
        host = "acs-db.mlpolicylab.dssg.io",
        port = "5432",
        user="mlpp_student",
        password = "CARE-horse-most",
        database = "acs_data_loading",
        options="-c search_path=dbo,acs"
    )

    cur = conn.cursor()

    variable_types = get_variable_names(variables)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {tablename}(
        Total_Population_Sex integer,
        Total_Male_Population integer,
        Total_Female_Population integer,
        Total_Population_Birthplace integer,
        Born_in_State_of_Residence integer,
        Born_in_Another_State integer,
        Born_out_of_country integer,
        State integer,
        County integer,
        Tract integer,
        Block_Group integer
    )
    """)

    index = 0
    for i in data:
        if index == 0:
            pass
        else:
            cur.execute(f"""INSERT INTO {tablename} VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]))
        index += 1
    conn.commit()
    conn.close()



