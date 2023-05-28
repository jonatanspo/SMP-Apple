# Import der benötigten Bibliotheken
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import pickle
import joblib

# Import des trainierten SVR-Modells
with open('model_svr.pkl', 'rb') as file: 
    svr_model = pickle.load(file)

# Import des MinMaxScaler
with open('min_max_scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Sidebar für die Berechnung der przentualen Veränderung des IXIC
st.sidebar.header("Berechnung prozentuale Veränderung des NASDAQ Composite Indexes")
x1 = st.sidebar.number_input("aktueller Schlusskurs ($)", min_value = 0.00, step = 0.01)
x2 = st.sidebar.number_input("vorheriger Schlusskurs ($)", min_value = 0.00, step = 0.01) 

def calculate(x1, x2):
    result = ((x1 - x2) / x2) * 100
    return result
             
if st.sidebar.button("Berechnen"):
        result = calculate(x1, x2)
        st.sidebar.success("Die prozentuale Veränderung des NASDAQ Composite Index beträgt {:.2f} %".format(result))
             
# Titel
st.write("""
# Apple Inc. Aktienkursprognose

""")
st.markdown("### Wie hoch ist der morgige Schlusskurs der Apple Aktie?")

# Aufteilung der Eingabefelder in zwei Spalten
left_column, right_column = st.columns(2)

# Eingabefelder linke Spalte
with left_column:
    p1 = st.number_input("Eröffnungskurs heute morgen ($)", min_value = 0.00, step = 0.01)
    p2 = st.number_input("Tageshöchstwert heute ($)", min_value = 0.00, step = 0.01)
    p3 = st.number_input("Niedrigster Tageskurs heute ($)", min_value = 0.00, step = 0.01)
    p4 = st.number_input("Schlusskurs heute Abend ($)", min_value = 0.00, step = 0.01)

# Eingabefelder rechte Spalte
with right_column:
    p5 = st.number_input("Handelsvolumen heute ($)", min_value = 0)
    p6 = st.number_input("Prozentuale Veränderung des NASDAQ Composite Index", step = 0.01)
    p7 = st.number_input("20 Tage EMA der Apple Aktie", min_value = 0.00, step = 0.01)
    
    # Abstand für den Button 
    st.write("")
    st.write("")

    # Vorhersage Button
    if st.button("Vorhersage"):
        new_data = pd.DataFrame({
            "Open": p1,
            "High": p2,
            "Low": p3,
            "Close": p4,
            "Volume": p5,
            "IXIC": p6,
            "ema_20": p7,
        }, index=[0])

        new_data_scaled = scaler.transform(new_data)
        pred = svr_model.predict(new_data_scaled)
        st.success("Der Schlusskurs der Apple Aktie wird morgen Abend {:.2f}$ betragen".format(pred[0]))

        if pred > p4:
            st.success("Laut dieser Prognose ist es sinnvoll in die Apple Aktie zu investieren, da der morgige Schlusskurs höher ist als der von heute Abend!")          
        else: 
            st.warning("Der Schlusskurs von morgen Abend ist niedriger oder gleich hoch wied der Schlusskurs von heute Abend. Daher scheint es nicht sinnvoll zu sein, in die Apple Aktie zu investieren!")
