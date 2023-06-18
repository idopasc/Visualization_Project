# -*- coding: utf-8 -*-
"""Visualization Final Project.ipynb
"""
####################################### Imports #######################################
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

####################################### Intro #######################################



st.set_page_config(page_title="Streamlit Project",
                   page_icon=":bar_chart:",
                  layout="wide")


with st.container():
    col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
    col2.title('Visualization Final Project')
with st.container():
    col1, col2, col3 = st.columns([0.30, 0.5, 0.20])
    col2.header('Beni Ifland - 208906255')
with st.container():
    col1, col2, col3 = st.columns([0.32, 0.5, 0.20])
    col2.header(' Bar Dolev - 318419512')
st.header("Intro")

st.subheader("""The subject of our visualization is the relationship between music consumption habits and preferences and their self reported mental health state.""")
st.subheader("""Mental health is an issue that affects millions of people around the world, with no signs of improvement and becoming increasingly alarming. According to the World Health Organization, mental health disorders have become the leading cause of disability, affecting a staggering 450 million people.""")
st.subheader("""Music, often revered as a universal language, has been used for centuries to convey emotions and thoughts. Music is valued, among other things, for its therapeutic potential, especially in the treatment of mental health problems in situations such as depression, anxiety, post-traumatic stress disorder (PTSD) and more. However, the mechanisms underlying music's apparent positive effects on mental health remain elusive and unclear to this day.""")
st.subheader("""The main question we chose is whether there is a connection between the nature of a certain person's music consumption and his mental health? We want to allow through visualization a critical observation of the connections between the consumption characteristics and the personal characteristics of the listeners and their mental health.""")
st.markdown("---")  
color_blind = st.radio("This Project is Color-blind friendly, Are you color blind?",['No','Yes'],key=51) # Did you know that 9% of men are color blind?
if color_blind == 'Yes': 
  cmap_graph_4 = "balance" # graph 4
  color_map_graphs12 = {
        "Classical":  px.colors.qualitative.Dark24[19],  # Blue
        "EDM":  px.colors.qualitative.Dark2[4], # Green
        "Folk":  px.colors.qualitative.Antique[5], # Purple
        "Hip hop": px.colors.qualitative.Dark24[14], # Olive
        "Metal": px.colors.qualitative.Set1[5],  # Yellow
        "Pop": px.colors.qualitative.Set1[0],  # Red
        "R&B": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Dark2[0], # Dark Green
        "Video game music":  px.colors.qualitative.Plotly[8] # Pink
    }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Dark24[5],  # Black
        "Depression": px.colors.qualitative.Set1[0],  # Red
        "Insomnia": px.colors.qualitative.Set1[1],  # Blue
        "OCD": px.colors.qualitative.Set1[5]  # Yellow
    } 
else:
  cmap_graph_4 = "Tempo" # graph 4
  color_map_graphs12 = {
        "Classical": px.colors.qualitative.Dark24[19], # Deep Blue
        "EDM":  px.colors.qualitative.D3[5], # Brown
        "Folk":  px.colors.qualitative.T10[9], # Grey
        "Hip hop": px.colors.qualitative.Alphabet[6], # Light Green
        "Metal": px.colors.qualitative.Alphabet[24], # Yellow
        "Pop": px.colors.qualitative.Light24[0], # Red
        "R&B": px.colors.qualitative.Dark24[5], # Black
        "Rock": px.colors.qualitative.Dark2[0], # Dark Green
        "Video game music":  px.colors.qualitative.Prism[6], # Orange
      }
  color_map_graph3 = {
        "Anxiety": px.colors.qualitative.Bold[2],  # Blue
        "Depression": px.colors.qualitative.Bold[3],  # Pink
        "Insomnia": px.colors.qualitative.Bold[4],  # Yellow
        "OCD": px.colors.qualitative.Bold[5]  # Green
    }
  
##################################### Pre-Process ###################################### 
df = pd.read_csv('lending_club_loan_two_shorten.csv', encoding='utf-8') # read csv
df = df.sort_values('emp_title')
df = df.rename(columns={"Fav genre": "Favorite Genre"})

genres_to_remove = ['Jazz', 'Lofi', 'Gospel', 'Latin','Rap','Country','K pop'] # remove genres with num of records < 30
df = df[~df['Favorite Genre'].isin(genres_to_remove)]


genres_to_keep = ['Rock','Pop','Metal','Classical','Video game music','EDM','R&B','Hip hop','Folk']  # remove people that are not listening to thier fav genre (112 records removed)
for idx, row in df.iterrows():
    fav = row['Favorite Genre']
    if row[f'Frequency [{fav}]'] not in ['Sometimes','Very frequently']:
      df = df.drop(idx)

def apply_bins_hours(time): # divide to hour bins for graph number 4
  if time <= 2:
    return "[0-2]"
  if time < 3:
    return "(2-3]"
  if time < 5:
    return "(3-4]"
  return "(4-24]"
df['Hours bins'] = df['Hours per day'].apply(apply_bins_hours)

# calculate the mean of targets for graph number 4
df['Average Score'] = df.apply(lambda row: row[['Anxiety', 'Depression', 'Insomnia', 'OCD']].mean(), axis=1)
          
# make a DF for graph number 3 : 
third_graph_df = pd.DataFrame(columns=['Genre','Mental Disorder', 'Average Score'])
targets = ['Anxiety','Depression','Insomnia','OCD']
names = sorted(['Rock','Video game music','R&B','EDM', 'Hip hop','Pop','Classical', 'Metal', 'Folk'])
j=0
for name in names:
    curr_df = df[df['Favorite Genre']==name]
    for target in targets:
        j+=1
        curr_avg = np.mean(curr_df[target])
        third_graph_df.loc[j] = [name ,target, curr_avg]

    
    
    
    
    
    
    
    
st.markdown("---")  
####################################### OUR GRAPHS ####################################### 


##################################### First Graph #####################################

    
st.subheader('Age & Mental Health Disorders scores - Scatter plot')
st.text('Would you like to see how age affects the Average of the Mental health scores? Or compare between two or more specific scores?')
comparison = st.radio("Choose one of:", ['None', 'Average', 'Comparison'], key=50)
  
if comparison == 'Comparison':
    st.text("Which Mental Health Disorders would you like to compare?")
    with st.container():
        col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])
        checkbox1 = col1.checkbox('Anxiety', key=1)
        checkbox2 = col2.checkbox('Depression', key=2)
        checkbox3 = col3.checkbox('Insomnia', key=3)    
        checkbox4 = col4.checkbox('OCD', key=4) 
     
    list_of_trues = [False, False, False, False]
    if (checkbox1):
        list_of_trues[0] = True
    else:
        list_of_trues[0] = False
          
    if (checkbox2):
        list_of_trues[1] = True
    else:
        list_of_trues[1] = False
          
    if (checkbox3):
        list_of_trues[2] = True
    else:
        list_of_trues[2] = False
          
    if (checkbox4):
        list_of_trues[3] = True
    else:
        list_of_trues[3] = False
          
    true_indices = [index for index, value in enumerate(list_of_trues) if value]
    graphs_amount = sum(list_of_trues)
      
     
  
    if sum(list_of_trues) > 0:

      bool_genres = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=777)
      if bool_genres=='I prefer to choose the genres manually':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical', key=9)
          edm = col2.checkbox('EDM', key=10)
          folk = col3.checkbox('Folk', key=11)    
          hiphop = col4.checkbox('Hip hop', key=12) 
          metal = col5.checkbox('Metal', key=13)
          pop = col6.checkbox('Pop', key=14)  
          rnb = col7.checkbox('R&B', key=15)    
          rock = col8.checkbox('Rock', key=16) 
          videogame = col9.checkbox('Video game music', key=17) 
      elif bool_genres=='Select all genres':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical',value=True, key=956555)
          edm = col2.checkbox('EDM',value=True, key=10555)
          folk = col3.checkbox('Folk',value=True, key=155551)    
          hiphop = col4.checkbox('Hip hop',value=True, key=125555) 
          metal = col5.checkbox('Metal',value=True, key=1555553)
          pop = col6.checkbox('Pop',value=True, key=145555)  
          rnb = col7.checkbox('R&B',value=True, key=15555)    
          rock = col8.checkbox('Rock',value=True, key=165555) 
          videogame = col9.checkbox('Video game music',value=True, key=15557) 
      check_box_booleans_graph_1 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
      genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
      to_show_graph1 =[]
      for i in range(len(genres)):
          if check_box_booleans_graph_1[i]:
              to_show_graph1.append(genres[i])   
  
      to_show_df_graph1 = df[df["Favorite Genre"].isin(to_show_graph1)]
  
    
      Anxiety = px.scatter(to_show_df_graph1,x="Age", y = 'Anxiety',
                          color="Favorite Genre",
                          title="Age Vs. Anxiety",
                          color_discrete_map = color_map_graphs12)
  
      
      Depression = px.scatter(to_show_df_graph1,x="Age", y = 'Depression',
                          color="Favorite Genre",
                          title="Age Vs. Depression",
                          color_discrete_map = color_map_graphs12)
      
      Insomnia = px.scatter(to_show_df_graph1,x="Age", y = 'Insomnia',
                          color="Favorite Genre",
                          title="Age Vs. Insomnia",
                          color_discrete_map = color_map_graphs12)
      
      OCD = px.scatter(to_show_df_graph1,x="Age", y = 'OCD',
                          color="Favorite Genre",
                          title="Age Vs. OCD",
                          color_discrete_map = color_map_graphs12)


                                            








      
      
      graphs = [Anxiety, Depression, Insomnia, OCD]
      for g in graphs:
          g.update_xaxes(tickmode='linear', dtick=10)
          g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
          g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
          g.update_layout(font=dict(size=28))
                  


        
          for trace in g.data:
              trace.update(marker=dict(size=10, opacity=0.7))
      if graphs_amount == 0:
          pass
      
      elif graphs_amount == 1:
          for i in range(len(list_of_trues)):
              if list_of_trues[i]:
                  st.plotly_chart(graphs[i], use_container_width=True)
                  
      elif graphs_amount == 2:
            col1, col2 = st.columns(2, gap="large")
            g1_idx = true_indices[0]
            g2_idx = true_indices[1]
            with col1:
              st.plotly_chart(graphs[g1_idx], use_container_width=False)
            with col2:
              st.plotly_chart(graphs[g2_idx], use_container_width=False)
      elif graphs_amount == 3:
            col1, col2 = st.columns(2, gap="large")
            g1_idx = true_indices[0]
            g2_idx = true_indices[1]
            g3_idx = true_indices[2]
            with col1:
              st.plotly_chart(graphs[g1_idx], use_container_width=False)
            with col2:
              st.plotly_chart(graphs[g2_idx], use_container_width=False)
            col3, _ = st.columns(2, gap="large")
            with col3:
              st.plotly_chart(graphs[g3_idx], use_container_width=False)
  
      elif graphs_amount == 4:
          col1, col2 = st.columns(2, gap="large")
  
          with col1:
              st.plotly_chart(graphs[0], use_container_width=False)
          with col2:
              st.plotly_chart(graphs[1], use_container_width=False)
              
          col3, col4 = st.columns(2, gap="large")
          with col3:
              st.plotly_chart(graphs[2], use_container_width=False)   
          with col4:
              st.plotly_chart(graphs[3], use_container_width=False)   
  
  
elif comparison == 'Average':
      bool_genres = st.radio("Choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=779)
      if bool_genres=='I prefer to choose the genres manually':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical', key=93)
          edm = col2.checkbox('EDM', key=1330)
          folk = col3.checkbox('Folk', key=1331)    
          hiphop = col4.checkbox('Hip hop', key=1332) 
          metal = col5.checkbox('Metal', key=13333)
          pop = col6.checkbox('Pop', key=1334)  
          rnb = col7.checkbox('R&B', key=1335)    
          rock = col8.checkbox('Rock', key=333333) 
          videogame = col9.checkbox('Video game music', key=1337) 
      elif bool_genres=='Select all genres':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical',value=True, key=95653355)
          edm = col2.checkbox('EDM',value=True, key=1053355)
          folk = col3.checkbox('Folk',value=True, key=1555331)    
          hiphop = col4.checkbox('Hip hop',value=True, key=33333333333333333) 
          metal = col5.checkbox('Metal',value=True, key=155533553)
          pop = col6.checkbox('Pop',value=True, key=145333555)  
          rnb = col7.checkbox('R&B',value=True, key=15553335)    
          rock = col8.checkbox('Rock',value=True, key=165533355) 
          videogame = col9.checkbox('Video game music',value=True, key=1533557) 
      check_box_booleans_graph_1 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
      genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
      to_show_graph1 =[]
      for i in range(len(genres)):
          if check_box_booleans_graph_1[i]:
              to_show_graph1.append(genres[i])
   
  
      to_show_df_graph1 = df[df["Favorite Genre"].isin(to_show_graph1)]
  
      g = px.scatter(to_show_df_graph1, x="Age", y="Average Score",
                           color="Favorite Genre",
                           title="Age Vs. Average of scores",
                          color_discrete_map = color_map_graphs12)
      for trace in g.data:
            trace.update(marker=dict(size=10, opacity=0.7))
      g.update_layout(yaxis_title='Average of Mental Health Scores')
      g.update_xaxes(range=[-0.5, 90.5], tickmode='linear', dtick=10)  
      g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
      g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
      st.plotly_chart(g, use_container_width=True)
  

st.markdown("---")     
  
  
  
  
  
  
##################################### Second Graph #####################################
st.subheader('Hours of listening (Daily) & Mental Health Disorders scores - Scatter plot')
st.text('Would you like to see how Hours of listening affects the Average of the Mental health scores? Or compare between two or more specific scores?')

comparison = st.radio("Choose one of:", ['None', 'Average', 'Comparison'], key=52)
if comparison == 'Comparison':
    st.text("Which Mental Health Disorders would you like to compare?")
    with st.container():
        col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])
        checkbox5 = col1.checkbox('Anxiety', key=5)
        checkbox6 = col2.checkbox('Depression', key=6)
        checkbox7 = col3.checkbox('Insomnia', key=7)    
        checkbox8 = col4.checkbox('OCD', key=8) 
        
    list_of_trues = [False, False, False, False]
    if (checkbox5):
        list_of_trues[0] = True
    else:
        list_of_trues[0] = False
        
    if (checkbox6):
        list_of_trues[1] = True
    else:
        list_of_trues[1] = False
        
    if (checkbox7):
        list_of_trues[2] = True
    else:
        list_of_trues[2] = False
        
    if (checkbox8):
        list_of_trues[3] = True
    else:
        list_of_trues[3] = False
        
    true_indices = [index for index, value in enumerate(list_of_trues) if value]
    graphs_amount = sum(list_of_trues)



    if sum(list_of_trues) > 0:
      

      bool_genres2 = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=877)
      if bool_genres2=='I prefer to choose the genres manually':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical', key=29)
          edm = col2.checkbox('EDM', key=210)
          folk = col3.checkbox('Folk', key=211)    
          hiphop = col4.checkbox('Hip hop', key=212) 
          metal = col5.checkbox('Metal', key=213)
          pop = col6.checkbox('Pop', key=214)  
          rnb = col7.checkbox('R&B', key=125)    
          rock = col8.checkbox('Rock', key=216) 
          videogame = col9.checkbox('Video game music', key=217) 
      elif bool_genres2=='Select all genres':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical',value=True, key=9256555)
          edm = col2.checkbox('EDM',value=True, key=120555)
          folk = col3.checkbox('Folk',value=True, key=1552551)    
          hiphop = col4.checkbox('Hip hop',value=True, key=1252555) 
          metal = col5.checkbox('Metal',value=True, key=1555253)
          pop = col6.checkbox('Pop',value=True, key=1455255)  
          rnb = col7.checkbox('R&B',value=True, key=155255)    
          rock = col8.checkbox('Rock',value=True, key=1652555) 
          videogame = col9.checkbox('Video game music',value=True, key=125557) 



      check_box_booleans_graph_2 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
      genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
      to_show_graph2 =[]
      for i in range(len(genres)):
          if check_box_booleans_graph_2[i]:
              to_show_graph2.append(genres[i])
 

      to_show_df_graph2 = df[df["Favorite Genre"].isin(to_show_graph2)]

    
    
      Anxiety = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Anxiety',
                        color="Favorite Genre",
                        title="Hours per day Vs. Anxiety",
                        color_discrete_map = color_map_graphs12)
      Depression = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Depression',
                        color="Favorite Genre",
                        title="Hours per day Vs. Depression",
                        color_discrete_map = color_map_graphs12)
      Insomnia = px.scatter(to_show_df_graph2,x="Hours per day", y = 'Insomnia',
                        color="Favorite Genre",
                        title="Hours per day Vs. Insomnia",
                        color_discrete_map = color_map_graphs12)
      OCD = px.scatter(to_show_df_graph2,x="Hours per day", y = 'OCD',
                        color="Favorite Genre",
                        title="Hours per day Vs. OCD",
                        color_discrete_map = color_map_graphs12)

      graphs = [Anxiety, Depression, Insomnia, OCD]
      for g in graphs:
        g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=2)  
        g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
        g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))
        for trace in g.data:
            trace.update(marker=dict(size=10, opacity=0.7))
      if graphs_amount == 0:
          pass
    
      elif graphs_amount == 1:
          for i in range(len(list_of_trues)):
              if list_of_trues[i]:
                  st.plotly_chart(graphs[i], use_container_width=True)
                
      elif graphs_amount == 2:
           col1, col2 = st.columns(2, gap="large")
           g1_idx = true_indices[0]
           g2_idx = true_indices[1]
           with col1:
              st.plotly_chart(graphs[g1_idx], use_container_width=False)
           with col2:
              st.plotly_chart(graphs[g2_idx], use_container_width=False)
      elif graphs_amount == 3:
           col1, col2 = st.columns(2, gap="large")
           g1_idx = true_indices[0]
           g2_idx = true_indices[1]
           g3_idx = true_indices[2]
           with col1:
              st.plotly_chart(graphs[g1_idx], use_container_width=False)
           with col2:
              st.plotly_chart(graphs[g2_idx], use_container_width=False)
           col3, _ = st.columns(2, gap="large")
           with col3:
              st.plotly_chart(graphs[g3_idx], use_container_width=False)

      elif graphs_amount == 4:
          col1, col2 = st.columns(2, gap="large")

          with col1:
              st.plotly_chart(graphs[0], use_container_width=False)
          with col2:
              st.plotly_chart(graphs[1], use_container_width=False)
            
          col3, col4 = st.columns(2, gap="large")
          with col3:
              st.plotly_chart(graphs[2], use_container_width=False)   
          with col4:
              st.plotly_chart(graphs[3], use_container_width=False)   


elif comparison == 'Average':
    
    bool_genres2 = st.radio("Please choose view method for genres:",['I prefer to choose the genres manually','Select all genres'],key=77229)
    if bool_genres2=='I prefer to choose the genres manually':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical', key=943)
          edm = col2.checkbox('EDM', key=13340)
          folk = col3.checkbox('Folk', key=13431)    
          hiphop = col4.checkbox('Hip hop', key=14332) 
          metal = col5.checkbox('Metal', key=133433)
          pop = col6.checkbox('Pop', key=14334)  
          rnb = col7.checkbox('R&B', key=13435)    
          rock = col8.checkbox('Rock', key=3343333) 
          videogame = col9.checkbox('Video game music', key=14337) 
    elif bool_genres2=='Select all genres':
        with st.container():
          col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
          classical = col1.checkbox('Classical',value=True, key=956543355)
          edm = col2.checkbox('EDM',value=True, key=10534355)
          folk = col3.checkbox('Folk',value=True, key=15545331)    
          hiphop = col4.checkbox('Hip hop',value=True, key=333334333333333333) 
          metal = col5.checkbox('Metal',value=True, key=1555335543)
          pop = col6.checkbox('Pop',value=True, key=1453335455)  
          rnb = col7.checkbox('R&B',value=True, key=155533435)    
          rock = col8.checkbox('Rock',value=True, key=1655343355) 
          videogame = col9.checkbox('Video game music',value=True, key=15334557) 
    check_box_booleans_graph_2 = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
    genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
    to_show_graph2 =[]
    for i in range(len(genres)):
        if check_box_booleans_graph_2[i]:
            to_show_graph2.append(genres[i])
 

    to_show_df_graph22 = df[df["Favorite Genre"].isin(to_show_graph2)]
    g = px.scatter(to_show_df_graph22, x="Hours per day", y="Average Score",
                         color="Favorite Genre",
                         title="Hours per day Vs. Average of scores",
                        color_discrete_map = color_map_graphs12)
    for trace in g.data:
        trace.update(marker=dict(size=10, opacity=0.7))
    g.update_layout(yaxis_title='Average of Mental Health Scores')
    g.update_xaxes(range=[-0.5, 24.5], tickmode='linear', dtick=1)
    g.update_xaxes(title_font=dict(size=20), tickfont=dict(size=14))
    g.update_yaxes(title_font=dict(size=20), tickfont=dict(size=14))

    st.plotly_chart(g, use_container_width=True)#fix this


st.markdown("---") 
  
  
  
  
  
##################################### Third Graph #####################################

st.subheader('Genres & Mental Health Scores, by Mental Health Disorder - Histogram')
order = st.radio("Which type of view would you prefer?",['Overall view (Compare all 4 disorders)','Specific view (Zoom in on one disorder)'],key=40000)
if order != 'Overall view (Compare all 4 disorders)':
  disorder = st.radio("Please choose disorder to view:",['Anxiety','Depression','Insomnia','OCD'],key=40001)
  
st.text("Would you like to view all Genres at once?")
select_all = st.radio("Choose one of: ",['Yes please.','No, I will choose myself.'])
if select_all == 'Yes please.': 
  with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical',value=True, key=9999699)
      edm = col2.checkbox('EDM',value=True, key=10999999)
      folk = col3.checkbox('Folk',value=True, key=11999999)    
      hiphop = col4.checkbox('Hip hop',value=True, key=12999999) 
      metal = col5.checkbox('Metal',value=True, key=139999999)
      pop = col6.checkbox('Pop',value=True, key=1499999)
      rnb = col7.checkbox('R&B',value=True, key=159999999)    
      rock = col8.checkbox('Rock',value=True, key=16999999) 
      videogame = col9.checkbox('Video game music',value=True, key=17999999) 
else:
  with st.container():
      col1, col2, col3, col4,col5, col6, col7, col8 ,col9 = st.columns(9)
      classical = col1.checkbox('Classical', key=97777777777)
      edm = col2.checkbox('EDM', key=1077777777)
      folk = col3.checkbox('Folk', key=117777777777)    
      hiphop = col4.checkbox('Hip hop', key=12777777) 
      metal = col5.checkbox('Metal', key=1377777777)
      pop = col6.checkbox('Pop', key=14777777777)
      rnb = col7.checkbox('R&B', key=159595)    
      rock = col8.checkbox('Rock', key=1677777777) 
      videogame = col9.checkbox('Video game music', key=7777777717) 

check_box_booleans = [classical,edm,folk,hiphop,metal,pop,rnb,rock,videogame]        
genres = ['Classical','EDM','Folk','Hip hop','Metal','Pop','R&B','Rock','Video game music'] 
to_show =[]
for i in range(len(genres)):
    if check_box_booleans[i]:
        to_show.append(genres[i])
 

to_show_df = third_graph_df[third_graph_df["Genre"].isin(to_show)]


if order == 'Overall view (Compare all 4 disorders)':
    third_graph_fig1 = px.histogram(to_show_df, x="Genre", y='Average Score',
               color='Mental Disorder', barmode='group',
               histfunc='avg',
               height=400,
               color_discrete_map=color_map_graph3)
    third_graph_fig1.update_layout(title="Histogram ordered Alphabetically",
                                 xaxis=dict(
                                         tickfont=dict(size=17),  # Set font size for x-axis tick numbers
                                         title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
                                          ),
                                 yaxis=dict(
                                         tickfont=dict(size=17),  # Set font size for y-axis tick numbers
                                         title=dict(text="Mental Health Score", font=dict(size=20))  # Set font size for y-axis label
                                          ))
    st.plotly_chart(third_graph_fig1, use_container_width=True)


elif order != 'Overall view (Compare all 4 disorders)':
  
  disorder_df = to_show_df[to_show_df['Mental Disorder']==disorder]
  third_graph_fig1 = px.histogram(disorder_df, x="Genre", y='Average Score',
               barmode='group',
               histfunc='avg',
               height=400,
               color_discrete_map=color_map_graph3)
  third_graph_fig1.update_layout(title=f'Histogram ordered by {disorder} Score',
                                 xaxis=dict(
                                         tickfont=dict(size=17),  # Set font size for x-axis tick numbers
                                         title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
                                          ),
                                 yaxis=dict(
                                         tickfont=dict(size=17),  # Set font size for y-axis tick numbers
                                         title=dict(text="Mental Health Score", font=dict(size=20))  # Set font size for y-axis label
                                          ))
  
  third_graph_fig1.update_xaxes(categoryorder="total descending")
  st.plotly_chart(third_graph_fig1, use_container_width=False)










st.markdown("---") 
##################################### Fourth Graph #####################################

st.subheader('Hours of listening per day & Genres, Aggregating Mental Health Scores - Heatmap')

hours_bins_order = ["[0-2]","(2-3]","(3-4]","(4-24]"]
df["Hours bins"] = pd.Categorical(df["Hours bins"], categories=hours_bins_order, ordered=True)

df_avg = df.groupby(["Hours bins", "Favorite Genre"]).mean().reset_index()
df_avg['Average Score'] = df_avg['Average Score'].apply(lambda x: round(x, 2))
fourth_graph_fig1 = px.density_heatmap(df_avg, x="Favorite Genre", y="Hours bins", z="Average Score",
                         labels=dict(x="Favorite Genre", y="Hours Bins", z="Average Score"),
                         text_auto ="Average Score",
                         color_continuous_scale=cmap_graph_4
                                      )
                                      
fourth_graph_fig1.update_layout(title="Average Mental Health Score by Hours Bins and Favorite Genre",
                               xaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for x-axis tick numbers
                                       title=dict(text="Favorite Genre",font=dict(size=20))  # Set font size for x-axis label
                                        ),
                               yaxis=dict(
                                       tickfont=dict(size=17),  # Set font size for y-axis tick numbers
                                       title=dict(text="Hours of listening (Daily)", font=dict(size=20))  # Set font size for y-axis label
                                        ),
                               coloraxis=dict(
                                      colorbar=dict(
                                            title="Mental Health Average Score",
                                            titleside="top",
                                            titlefont=dict(size=15),
                                            tickfont=dict(size=15))
                                              ),
                                font=dict(
                                      size=32  # Set the font size here
                                          )
                                 )

#fourth_graph_fig1.update_layout(uniformtext_minsize=20, uniformtext_mode='hide')      
st.plotly_chart(fourth_graph_fig1, use_container_width=True)
st.text("""
Note - the brackets we use indicate whether or not the number
near the bracket is included in the bin. Exmaple: (2,3] means 2 < x <= 3
""")
