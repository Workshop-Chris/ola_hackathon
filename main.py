import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
### functions ###


locations = ["Hamburg","Berlin","Rostock", "Dresden"]
geoDataLat = [53.5511, 52.5200, 54.0924, 51.0504]
geoDataLon = [9.9937, 13.4050, 12.0991, 13.7373]
ShareRE = [0.5, 0.6, 0.7, 0.6]
attractivityIndex = [0.8, 0.9, 0.5, 0.6]
gridConnectionCost = [0.3, 0.2, 0.9, 0.5, 0.5, 0.4]
energyCosts = [1, 1, 1, 1]
rd_cost = [0.6, 0.5, 0.1, 0.2, 0.4, 0.7] #redispatch costs
flex_earning = [0.6, 0.7, 0.1, 0.5, 0.4, 0.8]

def Calculation(weightedParametersRd_cost=0,weightedParametersFlex_earning=0, statusQuo = 1):
    result = []
    st.write(weightedParametersRd_cost)
    for counter in range(len(locations)):
        indicator = weightedParametersEE * ShareRE[counter] + weightedParametersAttractivity * attractivityIndex[counter] +\
                    weightedParametersGridConnectionCost * gridConnectionCost[counter] + weightedParametersRd_cost * weightedParametersEnergyCosts * rd_cost[counter] +\
                    weightedParametersFlex_earning * weightedParametersEnergyCosts * flex_earning[counter] +\
                    statusQuo * weightedParametersEnergyCosts * energyCosts[counter]
        result.append(indicator)
    maxValue = max(result)
    maxIndex = result.index(maxValue)
    return result, maxValue, maxIndex


### streamlit ###

weightedParametersEE = 0.5
weightedParametersAttractivity = 0.25
weightedParametersEnergyCosts = 0
weightedParametersGridConnectionCost = 0.25
weightedParametersRd_cost = 0
weightedParametersFlex_earning = 0
weightedParametersStatusQuo = 0

st.header("Optimal Location Assessment Tool")
st.text("find out where you can save the most with your flexibility potential - Ola larun ")

option = st.selectbox(
    'Choose the scenario',
    ('Status Quo', 'Consider grid conguestions in location planning', 'Consider flexibility potential in conguestion planning'))

col1, col2, col3, col4 = st.columns(4)
weightedParametersEE =  col1.number_input("CO2")
weightedParametersAttractivity =  col2.number_input("Actractivity of Location")
weightedParametersEnergyCosts =  col3.number_input("Energy Cost")
weightedParametersGridConnectionCost = col4.number_input("grid connection cost")




def locationUpdate():
    weightedParametersRd_cost = 0
    weightedParametersFlex_earning = 0
    weightedParametersStatusQuo = 0
    #st.write(option)
    if option == 'Consider grid conguestions in location planning':
        weightedParametersRd_cost = 1
        st.write(option)
        st.write(weightedParametersRd_cost)
    elif option == 'Consider flexibility potential in conguestion planning':
        weightedParametersFlex_earning = 1
    else:
        weightedParametersStatusQuo = 1
    result, maxValue, maxIndex = Calculation(weightedParametersRd_cost=weightedParametersRd_cost,weightedParametersFlex_earning=weightedParametersFlex_earning, statusQuo = weightedParametersStatusQuo)
    st.write(result)
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
    weightedParametersRd_cost = 0
    weightedParametersFlex_earning = 0
    weightedParametersStatusQuo = 0

if st.button("Calculate"):
    #Calculation()
    locationUpdate()


