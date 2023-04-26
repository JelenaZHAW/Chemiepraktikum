# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 09:54:44 2023

@author: Jelena
"""
import os
import json
import streamlit as st
import pandas as pd
import altair as alt

def load_data(filename):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []
        
    return data


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def berechne_ausbeute(tatsaechliche_menge, maximale_menge):
    ausbeute = (tatsaechliche_menge / maximale_menge) * 100
    
    return ausbeute


def berechne_konzentration(stoffmenge, volumen):
    konzentration = stoffmenge / volumen
    
    return konzentration


data = load_data("data.json")

# Seitenpanel zur Auswahl des Tests
test_choice = st.sidebar.radio("Wähle einen Test aus", ["neuer test", "alte tests"])

if test_choice == "neuer test":
    testname = st.text_input("Testname: ")

    tab1, tab2 = st.tabs(["Theoretische Ausbeute", "Stoffmengenkonzentration"])

    with tab1:
       st.header("Theoretische Ausbeute")
       st.write("Mit dieser App wird die theoretische Ausbeute in einer Lösung berechnet")
       st.title("Berechnung der theoretischen Ausbeute")
    
        # get user input
       tatsaechliche_menge = st.number_input("Tatsächliche Stoffmenge an Produkt")
       maximale_menge = st.number_input("Maximal mögliche Stoffmenge an Produkt")
       praktische_menge1 = st.number_input("Praktische Stoffmenge an Produkt 1")
       praktische_menge2 = st.number_input("Praktische Stoffmenge an Produkt 2") 
       praktische_menge3 = st.number_input("Praktische Stoffmenge an Produkt 3")
       praktische_menge4 = st.number_input("Praktische Stoffmenge an Produkt 4")
       praktische_menge5 = st.number_input("Praktische Stoffmenge an Produkt 5")
       
       
       # create chart from user input
       usr_input = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [praktische_menge1,
                      praktische_menge2,
                      praktische_menge3,
                      praktische_menge4,
                      praktische_menge5]
            }
        )
    
       chart = alt.Chart(usr_input).mark_circle().encode(
            x='x',
            y='y',
            color='x',
        ).interactive()
    
        # save user input
       if st.button("Berechnen Ausbeute"):
            ausbeute = berechne_ausbeute(tatsaechliche_menge, maximale_menge)
            st.write("Die theoretische Ausbeute beträgt:", ausbeute, "%")
        
            st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
            # save values to data dict
            if test_choice not in data:
                data["Ausbeute"][testname] = {}
            data["Ausbeute"][testname]["tatsächliche_menge"] = tatsaechliche_menge
            data["Ausbeute"][testname]["max_menge"] = maximale_menge
            save_data("data.json", data)
            
            
    
    with tab2:
        st.header("Stoffmengenkonzentration c")
        st.write("Hier wird berechnet wie hoch die Konzentration der Stoffmenge in einer Lösung ist.")
        st.title("Berechnung der Konzentration")
    
        stoffmenge = st.number_input("Stoffmenge n in mol")
        volumen = st.number_input("Volumen V in Liter")
    
        if st.button("Berechnen Stoffmenge"):
            konzentration = berechne_konzentration(stoffmenge, volumen)
            st.write("Die Konzentration beträgt:", konzentration, "mol/L")
            
            
            if test_choice not in data:
                data["Konzentration"][testname] = {}
            data["Konzentration"][testname]["stoffmenge"] = stoffmenge
            data["Konzentration"][testname]["volumen"] = volumen
            save_data("data.json", data)
           
            
           # data["test2"]= {}
           #  data["test2"]["stoffmenge"] = stoffmenge
           #  data["test2"]["vol"] = volumen 
            
elif test_choice == "alte tests":
    data = load_data("data.json")
    # Create a DataFrame from the dictionary, with the row names as columns and the column names as index
    # df = pd.DataFrame.from_dict(data, orient='columns')
    # # Transpose the DataFrame so that the row names become row index
    # df = df.T
    # st.table(df)
    flat_data = {}
    for key1, inner_dict in data.items():
        for key2, inner_inner_dict in inner_dict.items():
            for key3, value in inner_inner_dict.items():
                flat_data.setdefault(key3, {})[(key1, key2)] = value
    
    # Create a DataFrame from the flattened dictionary
    df = pd.DataFrame.from_dict(flat_data, orient='index')
    # Reset the index 
    df = df.reset_index()
    
    # Rename the "index" column to "Row Names" and "level_0" to "Column Names"
    df = df.rename(columns={"index": "Row Names", "level_0": "Column Names"})
    
    # Set the index to be the "Row Names" column
    df = df.set_index("Row Names")
    
    st.table(df)     