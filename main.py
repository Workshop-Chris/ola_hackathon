import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
### functions ###


locations = ["Hamburg","Berlin","Rostock", "Dresden"]
geoDataLat = [53.5511, 52.5200, 54.0924, 51.0504]
geoDataLon = [9.9937, 13.4050, 12.0991, 13.7373]
ShareRE = [0.5, 0.6, 0.7, 0.6]
attractivityIndex = [0.8, 0.9, 0.5, 0.6]
energyCosts = [0.5, 0.4, 0.3, 0.6]

def Calculation():
    result = []
    for counter in range(len(locations)):
        indicator = weightedParametersEE * ShareRE[counter] + weightedParametersAttractivity * attractivityIndex[counter] + weightedParametersEnergyCosts * energyCosts[counter]
        result.append(indicator)
    maxValue = max(result)
    maxIndex = result.index(maxValue)
    return result, maxValue, maxIndex


### streamlit ###

weightedParametersEE = 0.5
weightedParametersAttractivity = 0.25
weightedParametersEnergyCosts = 0.25

st.header("Optimal Location Assessment Tool")

col1, col2, col3 = st.columns(3)
weightedParametersEE =  col1.number_input("Renewables")
weightedParametersAttractivity =  col2.number_input("Actractivvity")
weightedParametersEnergyCosts =  col3.number_input("Energy Cost")


locations = ["Hamburg","Berlin","Rostock", "Dresden"]
geoDataLat = [53.5511, 52.5200, 54.0924, 51.0504]
geoDataLon = [9.9937, 13.4050, 12.0991, 13.7373]
ShareRE = [0.5, 0.6, 0.7, 0.6]
attractivityIndex = [0.8, 0.9, 0.5, 0.6]
energyCosts = [0.5, 0.4, 0.3, 0.6]


def locationUpdate():
    result, maxValue, maxIndex = Calculation()
    lat, lon = geoDataLat[maxIndex], geoDataLon[maxIndex]

    df = pd.DataFrame(data = {"lat":[lat], "lon":[lon]})
    st.map(df)



    sizes = [ShareRE[maxIndex], 1 - ShareRE[maxIndex]]
    labels = ["Anteil EE", "Anteil Rest"]
    myexplode = [0.1, 0]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels = labels, explode = myexplode, autopct='%1.1f%%')
    #plt.show()
    st.pyplot(fig)

if st.button("Calculate"):
    #Calculation()
    locationUpdate()


