import pandas as pd
import streamlit as st
from math import radians, cos, sin, asin, sqrt
from streamlit_folium import folium_static
import folium
import time
import matplotlib.pyplot as plt

st.title ("Data Mining Assignment")
st.header("Question 2: Q2")
st.text('The map is showing the distribution of people.')

location1_business = pd.read_csv("location1_business.csv")
location2_business = pd.read_csv("location2_business.csv")
location3_business = pd.read_csv("location3_business.csv")
df = pd.read_csv("data.csv")
df = df[["Occupation","FamilyExpenses_monthly","lat","lon"]]
people_loc_df = df[["lat","lon"]]

#loc 1 - Bukit Bintang
BukitBintang_Loc = (3.147668, 101.705406)
#loc 2 - Petaling Jaya
PetalingJaya_Loc = (3.105427, 101.643554)
#loc 3 - Bangsar
Bangsar_Loc = (3.131643, 101.669772)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 

#Calculate the distance between the 3 loc and the people
for ind in df.index:
    target_lat = df.loc[ind, "lat"]
    target_lon = df.loc[ind, "lon"]
    target_loc = (target_lat, target_lon)
    distance_loc1 = round(haversine(101.705406, 3.147668, target_lon, target_lat),2)
    distance_loc2 = round(haversine(101.643554, 3.105427, target_lon, target_lat),2)
    distance_loc3 = round(haversine(101.669772, 3.131643, target_lon, target_lat),2)
    df.loc[ind , "distance_loc1"] = distance_loc1
    df.loc[ind , "distance_loc2"] = distance_loc2
    df.loc[ind , "distance_loc3"] = distance_loc3

#Count the top 5 retail/business at Location 1
location1_business_top5 = pd.DataFrame(location1_business.groupby(["business_name"]).size())
location1_business_top5.rename(columns={0: 'count'}, inplace=True)
location1_business_top5 = location1_business_top5.reset_index(level=0)
location1_business_top5 = location1_business_top5.sort_values(by="count", ascending=False )
location1_business_top5 = location1_business_top5.reset_index()
location1_business_top5.drop('index', inplace=True, axis=1)
location1_business_top5 = location1_business_top5.head()

#Count the top 5 retail/business at Location 2
location2_business_top5 = pd.DataFrame(location2_business.groupby(["business_name"]).size())
location2_business_top5.rename(columns={0: 'count'}, inplace=True)
location2_business_top5 = location2_business_top5.reset_index(level=0)
location2_business_top5 = location2_business_top5.sort_values(by="count", ascending=False )
location2_business_top5 = location2_business_top5.reset_index()
location2_business_top5.drop('index', inplace=True, axis=1)
location2_business_top5 = location2_business_top5.head()

#Count the top 5 retail/business at Location 3
location3_business_top5 = pd.DataFrame(location3_business.groupby(["business_name"]).size())
location3_business_top5.rename(columns={0: 'count'}, inplace=True)
location3_business_top5 = location3_business_top5.reset_index(level=0)
location3_business_top5 = location3_business_top5.sort_values(by="count", ascending=False )
location3_business_top5 = location3_business_top5.reset_index()
location3_business_top5.drop('index', inplace=True, axis=1)
location3_business_top5 = location3_business_top5.head()

#Select Location
Location = st.radio("Please select a location", ("All(Everyone in the data set)", "Location 1 - Bukit Bintang", "Location 2 - Petaling Jaya", "Location 3 - Bangsar"))

if Location == "All(Everyone in the data set)":
    #Get all rows in the data set
    people_loc_df = df[["lat","lon"]]
    #print "updating" message
    my_element = st.info("Updating...")
    for i in range(1):
        time.sleep(1)
    #Remove the message & others element
    my_element.empty()  
    #zoom level of the map
    zoom = 11
    #set map
    my_element = st.map(people_loc_df, zoom=zoom)
elif Location == "Location 1 - Bukit Bintang":
    #Get rows which their lat & lon is at Bukit Bintang
    target_people= df[df["distance_loc1"] <= 2]
    target_loc_people = target_people[["lat","lon"]]
    people_loc_df = target_loc_people
    #Get the monthly family expenses for address within 2km from the selected location and also the average
    FamExp_month =  target_people[["FamilyExpenses_monthly"]]
    average_FamExp_month =  round(target_people["FamilyExpenses_monthly"].mean(),2)
    FamExp_month =  FamExp_month.reset_index(level=0)
    FamExp_month = FamExp_month.reset_index()
    FamExp_month.drop('index', inplace=True, axis=1)
    fig = plt.figure(figsize = (10, 5))
    #Creating the bar plot for monthly family expenses
    plt.bar(FamExp_month["level_0"],FamExp_month["FamilyExpenses_monthly"], color ='blue',width = 0.4)
    plt.xlabel("People who lives 2km within the location")
    plt.ylabel("Monthly Family Expenses")
    plt.title("Bar chart for Average Monthly Family Expenses")
    plt.axhline(y=average_FamExp_month, color= 'red', linewidth=3.5)
    plt.text(x= 0, y=average_FamExp_month+1, s='Average Monthly Family Expenses-RM' + str(average_FamExp_month), fontsize=18, bbox=dict(facecolor='red', alpha=0.5))
    #Count the occupation
    occup_count = pd.DataFrame(target_people.groupby(["Occupation"]).size())
    occup_count.rename(columns={0: 'count'}, inplace=True)
    occup_count = occup_count.reset_index(level=0)
    occup_count = occup_count.sort_values(by="count", ascending=False )
    occup_count = occup_count.reset_index()
    occup_count.drop('index', inplace=True, axis=1)
    #print "updating" message
    my_element = st.info("Updating...")
    for i in range(1):
        time.sleep(1)
    #Remove the message & others element
    my_element.empty()  
    target_top5 = location1_business_top5
    #zoom level of the map
    zoom = 13 
    #set map
    my_element = st.map(people_loc_df, zoom=zoom)
    #set header
    my_element = st.subheader("Chart for Count of Top-5 Retail/Business")
    #set bar chart - top 5
    my_element = st.bar_chart(target_top5, x="business_name", y="count")
    #set header
    my_element = st.subheader("Chart for Monthly Family Expenses")
    my_element = st.text('The red line in the chart is the Average Monthly Family Expenses.')
    #set bar chart - monthly family expenses
    my_element = st.pyplot(fig)
    #set header
    my_element = st.subheader("Chart for Count for different types of occupation")
    #set bar chart - occupation
    my_element = st.bar_chart(occup_count, x="Occupation", y="count")
elif Location == "Location 2 - Petaling Jaya":
    #Get rows which their lat & lon is at Petaling Jaya
    target_people= df[df["distance_loc2"] <= 2]
    target_loc_people = target_people[["lat","lon"]]
    people_loc_df = target_loc_people
    #Get the monthly family expenses for address within 2km from the selected location and also the average
    FamExp_month =  target_people[["FamilyExpenses_monthly"]]
    average_FamExp_month =  round(target_people["FamilyExpenses_monthly"].mean(),2)
    FamExp_month =  FamExp_month.reset_index(level=0)
    FamExp_month = FamExp_month.reset_index()
    FamExp_month.drop('index', inplace=True, axis=1)
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot for monthly family expenses
    plt.bar(FamExp_month["level_0"],FamExp_month["FamilyExpenses_monthly"], color ='blue',width = 0.4)
    plt.xlabel("People who lives 2km within the location")
    plt.ylabel("Monthly Family Expenses")
    plt.title("Bar chart for Average Monthly Family Expenses")
    plt.axhline(y=average_FamExp_month, color= 'red', linewidth=3.5)
    plt.text(x= 0, y=average_FamExp_month+1, s='Average Monthly Family Expenses-RM' + str(average_FamExp_month), fontsize=18, bbox=dict(facecolor='red', alpha=0.5))
    #Count the occupation
    occup_count = pd.DataFrame(target_people.groupby(["Occupation"]).size())
    occup_count.rename(columns={0: 'count'}, inplace=True)
    occup_count = occup_count.reset_index(level=0)
    occup_count = occup_count.sort_values(by="count", ascending=False )
    occup_count = occup_count.reset_index()
    occup_count.drop('index', inplace=True, axis=1)
    #print "updating" message
    my_element = st.info("Updating...")
    for i in range(1):
        time.sleep(1)
    #Remove the message & others element
    my_element.empty()  
    target_top5 = location2_business_top5
    #zoom level of the map
    zoom = 13
    #set map
    my_element = st.map(people_loc_df, zoom=zoom)
    #set header
    my_element = st.subheader("Bar Chart for Count of Top-5 Retail/Business")
   #set bar chart - top 5
    my_element = st.bar_chart(target_top5, x="business_name", y="count")
    #set header
    my_element = st.subheader("Chart for Monthly Family Expenses")
    my_element = st.text('The red line in the chart is the Average Monthly Family Expenses.')
    #set bar chart - monthly family expenses
    my_element = st.pyplot(fig)
    #set header
    my_element = st.subheader("Chart for Count for different types of occupation")
    #set bar chart - occupation
    my_element = st.bar_chart(occup_count, x="Occupation", y="count")
elif Location == "Location 3 - Bangsar":
    #Get rows which their lat & lon is at Bangsar
    target_people= df[df["distance_loc3"] <= 2]
    target_loc_people = target_people[["lat","lon"]]
    people_loc_df = target_loc_people
    #Get the monthly family expenses for address within 2km from the selected location and also the average
    FamExp_month =  target_people[["FamilyExpenses_monthly"]]
    average_FamExp_month =  round(target_people["FamilyExpenses_monthly"].mean(),2)
    FamExp_month =  FamExp_month.reset_index(level=0)
    FamExp_month = FamExp_month.reset_index()
    FamExp_month.drop('index', inplace=True, axis=1)
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot for monthly family expenses
    plt.bar(FamExp_month["level_0"],FamExp_month["FamilyExpenses_monthly"], color ='blue',width = 0.4)
    plt.xlabel("People who lives 2km within the location")
    plt.ylabel("Monthly Family Expenses")
    plt.title("Bar chart for Average Monthly Family Expenses")
    plt.axhline(y=average_FamExp_month, color= 'red', linewidth=3.5)
    plt.text(x= 0, y=average_FamExp_month+1, s='Average Monthly Family Expenses-RM' + str(average_FamExp_month), fontsize=18, bbox=dict(facecolor='red', alpha=0.5))
    #Count the occupation
    occup_count = pd.DataFrame(target_people.groupby(["Occupation"]).size())
    occup_count.rename(columns={0: 'count'}, inplace=True)
    occup_count = occup_count.reset_index(level=0)
    occup_count = occup_count.sort_values(by="count", ascending=False )
    occup_count = occup_count.reset_index()
    occup_count.drop('index', inplace=True, axis=1)
    #print "updating" message
    my_element = st.info("Updating...")
    for i in range(1):
        time.sleep(1)
    #Remove the message & others element
    my_element.empty()  
    target_top5 = location3_business_top5
    #zoom level of the map
    zoom = 13
    #set map
    my_element = st.map(people_loc_df, zoom=zoom)
    #set header
    my_element = st.subheader("Bar Chart for Count of Top-5 Retail/Business")
    #set bar chart - top 5
    my_element = st.bar_chart(target_top5, x="business_name", y="count")
    #set header
    my_element = st.subheader("Chart for Monthly Family Expenses")
    my_element = st.text('The red line in the chart is the Average Monthly Family Expenses.')
    #set bar chart - monthly family expenses
    my_element = st.pyplot(fig)
    #set header
    my_element = st.subheader("Chart for Count for different types of occupation")
    #set bar chart - occupation
    my_element = st.bar_chart(occup_count, x="Occupation", y="count")




