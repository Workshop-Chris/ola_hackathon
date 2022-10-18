import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
### functions ###


locations = ["Hamburg","Berlin","Rostock","Altenfeld", "Wolkramshausen", "Dresden"]
geoDataLat = [53.5511, 52.5200, 54.0924, 50.5639, 51.4232, 51.0504]
geoDataLon = [9.9937, 13.4050, 12.0991, 10.9625, 10.7380, 13.7373]
ShareRE = [0.5, 0.6, 0.7, 0.6, 0.4, 0.3]
attractivityIndex = [0.8, 0.9, 0.4, 0.3, 0.5, 0.7]
gridConnectionCost = [0.3, 0.2, 0.9, 0.5, 0.5, 0.4]
energyCosts = [1, 1, 1, 1, 1, 1]
rd_cost = [0.6, 0.5, 1, 0.2, 0.4, 0.7] #redispatch costs
flex_earning = [0.6, 0.7, 1, 0.5, 0.4, 0.8]

def Calculation(weightedParametersRd_cost=0,weightedParametersFlex_earning=0, statusQuo = 0):
    result = []
    #st.write(weightedParametersRd_cost)
    for counter in range(len(locations)):
        indicator = weightedParametersEE * ShareRE[counter] + weightedParametersAttractivity * attractivityIndex[counter] +\
                    weightedParametersGridConnectionCost * gridConnectionCost[counter] + weightedParametersRd_cost * weightedParametersEnergyCosts * rd_cost[counter] +\
                    weightedParametersFlex_earning * weightedParametersEnergyCosts * flex * flex_earning[counter] +\
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
global flex
flex = 0
col0_1, col0_2, col0_3 = st.columns([1,4,1])
col0_2.image('logo.png')
#st.title("Optimal Location Assessment Tool")
#col0_1, col0_2 = st.columns([4,1])
#col0_2.image('logo.png')
col0_2.markdown("**_Find out where you can save the most with your flexibility potential_**")
#col0_1, col0_2 = st.columns(2, gap = 'small')
st.text_input(label = 'Estimated consumption: ', value =  '1000 MW')
flex = st.select_slider("Choose the share of flexibility of the consumption:",
                         options = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
option = st.selectbox(
    'Choose the scenario',
    ('Present regulatory framework', 'Consider grid congestions in location planning',
     'Consider flexibility potential in location planning'))

col1, col2, col3, col4 = st.columns(4)
weightedParametersEE = col1.number_input(r'''CO2 Emissions''')
weightedParametersAttractivity = col2.number_input("Attractivity of location")
weightedParametersEnergyCosts = col3.number_input("Energy cost")
weightedParametersGridConnectionCost = col4.number_input("Grid connection cost")




def locationUpdate():
    weightedParametersRd_cost = 0
    weightedParametersFlex_earning = 0
    weightedParametersStatusQuo = 0
    #st.write(option)
    if option == 'Consider grid congestions in location planning':
        weightedParametersRd_cost = 1
        #st.write(option)
        #st.write(weightedParametersRd_cost)
    elif option == 'Consider flexibility potential in location planning':
        weightedParametersFlex_earning = 1


    else:
        weightedParametersStatusQuo = 1
    result, maxValue, maxIndex = Calculation(weightedParametersRd_cost=weightedParametersRd_cost,weightedParametersFlex_earning=weightedParametersFlex_earning, statusQuo = weightedParametersStatusQuo)
    #st.write(result)
    lat, lon = geoDataLat[maxIndex], geoDataLon[maxIndex]

    df = pd.DataFrame(data = {"lat":[lat], "lon":[lon]})
    st.caption("Optimal location:")
    st.map(df)

    gridConnectionResult = round(random.random(), 2)
    emissionResult = round(random.random() * 100, 2)

    col1_1,col1_2, col1_3 = st.columns(3, gap = 'small')
    col1_1.subheader("Estimated emissions: ")
    col1_1.subheader("Estimated grid connection cost: ")
    col1_2.title(str(emissionResult) + ' t ')
    col1_2.title(str(gridConnectionResult) + ' M€')

    sizes = [ShareRE[maxIndex], 1 - ShareRE[maxIndex]]
    labels = ["EE infeed", "Other"]
    myexplode = [0.1, 0]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels = labels, explode = myexplode, autopct='%1.1f%%')
    #plt.show()
    col1_3.pyplot(fig)


if st.button("Calculate"):
    #Calculation()
    locationUpdate()


