
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd 
import numpy as np
import random
from random import randrange
from random import randint
from datetime import timedelta
from datetime import date




def create_dict_values(df):
    '''
    définition du dictionnaire avec les valeurs possible pour chaque variable
    '''
    
    variables = np.array(df.columns)
    values = []
    
    #la boucle suivante va permettre de générer la liste des valeurs possibles pour chaque variable
    for v in variables:
        value = df[v].values.tolist()[1:] #la première ligne contient le type de variable, il est donc nécessaire de commencer l'itération à la ligne 2
        cleanedValue = [x for x in value if str(x) != 'nan'] #on enlève toutes les valeurs nulles pour qu'elles ne soient pas présentes dans le dictionnaire
        values.append(cleanedValue)
        
    #création du dictionnaire à partir de la liste générée    
    _dict_values = dict(zip(variables, values)) 
    
    return(_dict_values)


def create_dict_types(df):
    '''
    définition du dictionnaire avec le type de chaque variable
    '''
    
    variables = np.array(df.columns)
    types=[]
    
    #on agit de la même façon que précedemment, sauf que l'on garde ici uniquement la première ligne au lieu de l'enlever
    for v in variables:
        type_ = df[v].values.tolist()[0] 
        types.append(type_)
    _dict_types = dict(zip(variables, types))
    return(_dict_types)


def random_date(start, end):
    '''
    choix d'une date aléatoire entre la date de début et de fin en arguments
    '''
    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_min_max(dict_values, var):
    
    return min(dict_values[var]), max(dict_values[var])

def create_fake_data(df, size):
    
    variables = list(df.columns)
    dict_values=create_dict_values(df)
    dict_types=create_dict_types(df)
    
    fake_values = []
    for var in variables:
        
        if dict_types[var] == 'index':
            fake_data = list(range(size))
            fake_values.append(fake_data)
        
        elif (dict_types[var] == 'str') or (dict_types[var] == 'boolean'):
            fake_data = random.choices(dict_values[var],k=size)
            fake_values.append(fake_data)
        
        elif dict_types[var] == 'date':
            min_date, max_date = get_min_max(dict_values,var)
            fake_data = [random_date(min_date,max_date) for k in range(size)]
            fake_values.append(fake_data)
        
        elif dict_types[var] == 'int':
            min_int, max_int = get_min_max(dict_values,var)
            fake_data = [randint(int(min_int),int(max_int)) for k in range(size)]
            fake_values.append(fake_data)
            
        elif dict_types[var] == 'float':
            min_float, max_float = get_min_max(dict_values,var)
            fake_data = [random.uniform(float(min_float),float(max_float)) for k in range(size)]
            fake_values.append(fake_data)
    
    df_fake_data = pd.DataFrame(dict(zip(variables,fake_values)))
    
    return df_fake_data

@st.cache
def convert_csvdf(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
	return df.to_csv().encode('utf-8')

@st.cache 
def convert_xlsxdf(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_excel().encode('utf-8')



def main():
    l,r=st.columns(2)	
    st.title('Fake Data generator')
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        size=int(st.number_input('Insert the number of rows',step=1000))
        name_file=st.text_input('Insert the name of the new file')
        if st.button('create new data set'):
            df=pd.read_excel(uploaded_file)
            df_fake_data=create_fake_data(df,size)
            csv= convert_csvdf(df_fake_data)
            l.download_button(label="📥 Download (.csv)",data=csv,file_name=f'{name_file}.csv',mime='text/csv')
            r.download_button(label="📥 Download (.xlsx)",data=csv,file_name=f'{name_file}.xlsx',mime='text/xlsx')
main()
