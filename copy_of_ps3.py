# -*- coding: utf-8 -*-
"""Copy of PS3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SuSTO0895xQiKaToaPDGdURPxemTEZ-N

# PS3 - Mapping International Application Conversion: Refined
**Erick Watt-Udogu**

## PS3 Addendum

For this problem set, I focused on the narrative and the outputs. This involved two main areas: the way the maps were displayed (e.g., color and titles) and the annotations. My goal was to create visualizations that could be easily shared with a chancellor, dean, or intern. Given the abundance of data, I prioritized making the most critical insights clear and impactful. I also reorganized the entire workbook to better achieve this goal. Lastly, I emphasized parsimony, eliminating some visualizations and removing the map of India.

**Method:** This project was an exercise in using AI and iterative refinement. Positioning the annotations required the precision of a computer, but it still took manual adjustments to ensure everything was to my liking. Personally, I love the power that coding provides. It feels as though the possibilities are endless, but it’s crucial to err on the side of simplicity rather than indulge in a showcase of the tool's capabilities.


**Limitations of this Project:** I still believe that application mailing data is a poor proxy for enrollment information. Because of my familiarity with the data, I know we have consistently had Nigerian students, yet this isn't always visible when we use mailing country as the metric. I also remained committed to the principle of parsimony. At one point, I considered adding conversion data (AC/App%) to the plots, but I felt that the existing data was already extensive and that adding more would obscure the main message.


**Future Projects:** I plan to disaggregate the data for the United States and India, as those countries warrant further analysis. I hypothesize that, despite our focus on countries like Paraguay and Nigeria (both of which I appreciate), certain states within the US and India contribute more students than entire countries do. Additionally, if the goal is to increase student numbers through targeted efforts, these efforts may not be yielding or may be unlikely to yield significant results for graduate programs. For instance, Korea has historically not produced many enrollments, and I am unsure why it remains a target.

## PS2 Overview

**Overview and Research Questions:** Over the past three years, both the campus and The Graduate School have seen a notable increase in international applications, admissions, and enrollments. This project disaggregates the application data to explore key research questions:

1.   Which countries contribute to graduate school enrollment?
2.   What are the conversion rates from application to enrollment across different countries?
3.   Do some countries show higher or lower conversion rates?
4.   Additionally, are there regional differences within countries like India, where most of our international students originate?

**Methodology:** Using accepted offers as a proxy for enrollment, student origin was determined based on mailing addresses. This data primarily focuses on new applicants from the past three academic years, providing insights into international application trends.

 AI tools were particularly useful in beautifying the visualizations, making the sizing and placement of elements much easier to handle. However, AI is not a replacement for the core narrative and data manipulation, which remain central to the analysis.


**Findings:**

* *Domestic vs. International Yield Rates:* The highest conversion rates come from
New Jersey, Pennsylvania, and New York—particularly New Jersey, where we yield 19% of applicants. International applications, especially from countries like India, show much lower yield rates (around 5%), while countries like Ghana and Nigeria yield as little as 3% to 5%, despite recent investment in those regions.
* *Regional and Programmatic Differences:* India is a consistent contributor, and regions like Telangana, Gujarat, and Andhra Pradesh produce more students than nearly any other international region. Indian students are heavily concentrated in Data Science and Computer Science programs, though recruitment efforts in South America don't align with this trend.
* *Unexpected Trends:* Bangladesh stands out for showing steady growth in student numbers despite little campus investment, whereas new initiatives to engage regions like Korea have yielded little traction in application or conversion data.

**Limitations:**

* *Admission vs. Enrollment Data:* This analysis uses admission data, which does not always reflect final enrollment. Enrollment data is more accurate but harder to access and requires specific requests.
* *Mailing Address as Proxy for Origin:* Using mailing addresses to determine origin can misrepresent students’ true backgrounds, as some applicants may be studying abroad when they apply, but are originally from different countries.
* *Focus on New Applicants:* The data focuses on new applicants, potentially underrepresenting programs such as PhD programs where students often remain in the program for multiple years.


**Future Study:** Future research should focus on domestic applications, particularly from New Jersey, to better understand trends in local conversion rates. Additionally, shifting from admission data to enrollment data will provide a more accurate picture of which applicants ultimately matriculate, offering a clearer understanding of conversion patterns.

# Set Up Code & Import Files
Run this for data and setup code.

aok: its a mess with repetition and disorganization (not an error though)
"""

# Import seaborn
import seaborn as sns

# Apply the default theme
sns.set_theme()

!pip install geopandas==1.0.1
import pandas as pd
import urllib.request
import numpy as np

#plotly
import plotly.express as px #a quick simple one
import plotly.graph_objects as go #can get convoluted

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install geopandas==1.0.1
# !pip install mapclassify

import time, webbrowser, zipfile

import pandas as pd
import geopandas as gpd

from google.colab import data_table
data_table.enable_dataframe_formatter()

from google.colab import files

import folium as f
from folium.plugins import MarkerCluster, HeatMap

#will display all output not just last command
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import os, zipfile #basics
import pandas as pd #data management
import matplotlib.pyplot as plt #vis

import geopandas as gpd #gis/maps

#will display all output not just last command
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from google.colab import files #to download from colab onto hd

from google.colab import data_table
data_table.enable_dataframe_formatter() #this enables spreadsheet view upon calling dataframe (without() )

#!python --version
gpd.__version__

!pip install mapclassify
import mapclassify #need for thematic map classification

"""# Map Data Import and Merge

## World Map Import
"""

#I uploaded a different world map shapfile, but I like htis one better.
! wget -q -O Countries.zip https://datacatalogfiles.worldbank.org/ddh-published/0038272/DR0046659/wb_countries_admin0_10m.zip

zip_ref = zipfile.ZipFile('Countries.zip', 'r'); zip_ref.extractall(); zip_ref.close() #just unzipping

Countries=gpd.read_file('/content/WB_countries_Admin0_10m/WB_countries_Admin0_10m.shp')

"""## Ad Map Import

"""

import urllib

import pandas as pd

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/GRE%20PhD%2020241110.csv", 'phd.csv')
phd = pd.read_csv('phd.csv')

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/Incomplete%20App%2020241110%20(1).csv", 'incomplete.csv')
incomplete = pd.read_csv('incomplete.csv')

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/UG%20-%20Jun%2020241110%20(3).csv", 'juniors.csv')
juniors = pd.read_csv('juniors.csv')

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/UG%20-%20Soph%2020241110.csv", 'sophmores.csv')
sophmores = pd.read_csv('sophmores.csv')

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gradschoolcam/main/UG%20-%20Sr%2020241110.csv", 'seniors.csv')
seniors = pd.read_csv('seniors.csv')

combined_df = pd.concat([phd, incomplete, juniors,sophmores, seniors], ignore_index=True)
combined_df.head()

"""### Getting to Know World Data"""

#I need to familiarize myself with the data for the merge. First I want to see how the country names are displayed, so I can merge based on country name.
Countries.head(3)

#WB_Name looks good, It's closest to the names I have in my files. I need to see a list of all the names in the file to see how they are presented.
print(Countries.WB_NAME.unique())

#renaming for merge
Countries = Countries.rename(columns={'WB_NAME':'Country'})

"""### Importing World Application Data"""

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gis/refs/heads/main/World%20AC.csv", "WorldApp.csv")

WorldApp = pd.read_csv('WorldApp.csv')

"""### Merging World Map Data"""

#Merging World Map with World AC Data
WORLDACMAP = pd.merge(Countries, WorldApp, on='Country',how='outer',indicator=True)
WORLDACMAP[['Country','2022-2023','2023-2024','2024-2025','Grand Total','_merge']]
#aok ok i skimmed thru _merge and a ton of left_only, but none right_only so we are probably good

#Need to get rid of the NaNs
WORLDACMAP['2022-2023'] = WORLDACMAP['2022-2023'].fillna(0)
WORLDACMAP['2023-2024'] = WORLDACMAP['2023-2024'].fillna(0)
WORLDACMAP['2024-2025'] = WORLDACMAP['2024-2025'].fillna(0)
WORLDACMAP['Grand Total'] = WORLDACMAP['Grand Total'].fillna(0)
#aok ok good; in general typically fillna(0) produces mistake as na is not 0
#but in this case it is probably correct as not having a country in admissions data
#probably means that nobody from that country

"""### Importing World Map Data for Program Analysis"""

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gis/refs/heads/main/downpipe.csv", "downpipe.csv")

Down = pd.read_csv('downpipe.csv')
#aok yes good substantive name; assuming down is meaningful here; defintely better than something like df

"""## US Map Import"""

! wget -q -O US.zip https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip

zip_ref = zipfile.ZipFile('US.zip', 'r'); zip_ref.extractall(); zip_ref.close() #just unzipping

US=gpd.read_file('/content/cb_2018_us_state_500k.shp')

"""## Getting to Know US Data"""

#I need to familiarize myself with the data for the merge. First I want to see how the State names are displayed, so I can merge based on state name.
US.head(1)

#Same as for World. Name field looks like state names. I'll merge based on the these.
print(US.NAME.unique())

#renaming for merge
US = US.rename(columns={'NAME':'State'})

"""### Importing US Application Data"""

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gis/refs/heads/main/State%20AC.csv", "USApp.csv")

USApp = pd.read_csv('USApp.csv')

"""### Merging US Map Data"""

#Merging US Map with US AC Data
USACMAP = pd.merge(US, USApp, on='State',how='outer',indicator=True)
USACMAP[['State','Total','_merge']]

#Need to get rid of the NaNs
USACMAP['Total'] = USACMAP['Total'].fillna(0)

# I just want the lower 48 since we don't have students in states like Alaska
LOWERACMAP = USACMAP[~USACMAP['State'].isin(['Alaska', 'Hawaii', 'Puerto Rico','American Samoa','United States Virgin Islands','Guam','Commonwealth of the Northern Mariana Islands'])]

"""## India Map Import"""

! wget -q -O India.zip https://github.com/datameet/maps/archive/master.zip

zip_ref = zipfile.ZipFile('India.zip', 'r'); zip_ref.extractall(); zip_ref.close() #just unzipping

India=gpd.read_file('/content/maps-master/States/Admin2.shp')

"""### Getting to Know India Data"""

print(India.ST_NM.unique())

#renaming for merge
India = India.rename(columns={'ST_NM':'State'})

"""### Importing Indian Application Data"""

urllib.request.urlretrieve("https://raw.githubusercontent.com/ewattudo/gis/refs/heads/main/Indian%20States.csv", "India.csv")

InApp = pd.read_csv('India.csv')

"""### Merging Indian Map Data"""

#Merging US Map with US AC Data
INACMAP = pd.merge(India, InApp, on='State',how='outer',indicator=True)
INACMAP[['State','Total','_merge']]

#Need to get rid of the NaNs
INACMAP['Total'] = INACMAP['Total'].fillna(0)

WORLDACTARGET=WORLDACMAP.query(("Country=='Nigeria' | Country=='Ghana'| Country=='Paraguay'| Country=='Korea, Republic of'"))

"""# Visualizations

aok yes visualcapitalist is great--ton of nice vis!
"""

#inspriation https://www.visualcapitalist.com/cp/international-students-in-the-u-s-come-from/#google_vignette,https://monitor.icef.com/2023/11/us-international-enrolment-passed-pre-pandemic-levels-for-near-record-high-in-2022-23/
#I tried to get the locations coded in the data, but found it easier to annotate. AI was helpful in placement of the annotations.
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, figsize=(25, 50))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Plot WORLDACMAP with the 'Grand Total' column
WORLDACMAP.plot(ax=ax, column='Grand Total', legend=True, cmap='Blues',
                scheme='natural_breaks', k=7, edgecolor='grey', linewidth=0.3,
                legend_kwds={"fmt": "{:,.0f}", 'loc': 'lower right', 'markerscale': 1.4})

# Overlay WORLDACTARGET with hatching
WORLDACTARGET.plot(ax=ax, edgecolor='black', linewidth=0.2, facecolor="none", alpha=1, hatch='///')
ax.text(-180, 93, "Rutgers Graduate School-Camden", fontsize=24, color='Black', fontweight='bold', ha='left')
ax.text(-180, 86, "Students by Application Mailing Location (2022 - Present)", fontsize=24, color='#cc0033', fontweight='bold', ha='left')

# Remove the border (spines) around the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Remove x and y ticks
ax.set_xticks([])
ax.set_yticks([])

# Coordinates for Nigeria, Ghana, Korea, and Paraguay
country_coords = {
    "Campus Target: Nigeria": (8.6753, 9.0820),  # (Longitude, Latitude)
    "Campus Target: Ghana": (-1.0232, 7.9465),
    "Campus Target: Korea": (127.7669, 35.9078),  # South Korea
    "Campus Target: Paraguay": (-58.4438, -23.4425)
}

# Add red arrows and country names
for country, (lon, lat) in country_coords.items():
    if country == "Campus Target: Nigeria":
        # Adjust arrow and text position for Nigeria
        ax.annotate(
            '', xy=(lon, lat), xytext=(lon + 15, lat + 5),
            arrowprops=dict(facecolor='#c00033', edgecolor='#c00033', arrowstyle='-|>', lw=2.5)
        )
        ax.text(lon + 16, lat + 5.5, country, fontsize=12, color='black', fontweight='bold')
    else:
        # Default arrow and text position for other countries
        ax.annotate(
            '', xy=(lon, lat), xytext=(lon + 10, lat + 10),
            arrowprops=dict(facecolor='#c00033', edgecolor='#c00033', arrowstyle='-|>', lw=2.5)
        )
        ax.text(lon + 11, lat + 11, country, fontsize=12, color='black', fontweight='bold')

# Add larger opaque red circles with text for the Northeast US and India
# Northeast US
circle_nj = mpatches.Circle((-74, 40), radius=15, color='red', alpha=0.8)  # Larger circle for NJ/NY/PA
ax.add_patch(circle_nj)
# Larger text for 70%
ax.text(-74, 45, "70%", fontsize=27, color='white', ha='center', va='center', fontweight='bold')
# Smaller text for the rest
ax.text(-74, 37, "of all students\nfrom NJ/NY/PA", fontsize=12, color='white', ha='center', va='center')

# India
circle_india = mpatches.Circle((78, 22), radius=15, color='red', alpha=0.8)  # Larger circle for India
ax.add_patch(circle_india)
# Larger text for 68%
ax.text(78, 27, "68%", fontsize=27, color='white', ha='center', va='center', fontweight='bold')
# Smaller text for the rest
ax.text(78, 19, "of intl students\nfrom India", fontsize=12, color='white', ha='center', va='center')

plt.show()

#I went back and forth on the horizontal versus vertical. I have settled on horizontal.
#I like the power of annotation. I am not sure I would do this if I didn't have a couple of points, but I like that I can tell the story.
# Create subplots with shared y-axis and a tight layout
fig, axs = plt.subplots(1, 3, figsize=(30, 15), sharey=True, tight_layout=True)

# --- First Map: 2022-2023 ---
WORLDACMAP.plot(ax=axs[0], column='2022-2023', legend=True, cmap='Blues', scheme='natural_breaks', k=7,
                edgecolor='grey', linewidth=0.2,
                legend_kwds={"fmt": "{:,.0f}", 'loc': 'lower right', 'title_fontsize': 'medium',
                             'fontsize': 'small', 'markerscale': 1.4})
axs[0].set_facecolor('white')
axs[0].set_title("Academic Year 2022-2023", fontsize=16, fontweight='bold', color='black', loc='left', pad=10)
axs[0].text(0, .98, "Students by Application Mailing Location", transform=axs[0].transAxes, fontsize=16, fontweight='bold', color='#cc0033', ha='left')

# Adjusted arrow placement to water areas
axs[0].annotate("Few students\ncome from S. America", xy=(-60, -20), xytext=(-130, -50),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

axs[0].annotate("Ghana is represented\nnot Nigeria", xy=(-5, 10), xytext=(-40, 40),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

axs[0].annotate("India & Bangladesh\nrepresentation is noticeable", xy=(80, 20), xytext=(30, -30),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

# --- Second Map: 2023-2024 ---
WORLDACMAP.plot(ax=axs[1], column='2023-2024', legend=True, cmap='Blues', scheme='natural_breaks', k=7,
                edgecolor='grey', linewidth=0.2,
                legend_kwds={"fmt": "{:,.0f}", 'loc': 'lower right', 'title_fontsize': 'medium',
                             'fontsize': 'small', 'markerscale': 1.4})
axs[1].set_facecolor('white')
axs[1].set_title("Academic Year 2023-2024", fontsize=16, fontweight='bold', color='black', loc='left', pad=10)
axs[1].text(0, .98, "Students by Application Mailing Location", transform=axs[1].transAxes, fontsize=16, fontweight='bold', color='#cc0033', ha='left')

# Adjusted arrow placement to water areas
axs[1].annotate("No students from\nS. America", xy=(-60, -20), xytext=(-130, -50),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

axs[1].annotate("More students\nfrom Western Africa", xy=(-5, 10), xytext=(-40, 40),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

axs[1].annotate("Consistent & Growing", xy=(80, 20), xytext=(30, -30),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

# --- Third Map: 2024-2025 ---
WORLDACMAP.plot(ax=axs[2], column='2024-2025', legend=True, cmap='Blues', scheme='natural_breaks', k=7,
                edgecolor='grey', linewidth=0.2,
                legend_kwds={"fmt": "{:,.0f}", 'loc': 'lower right', 'title_fontsize': 'medium',
                             'fontsize': 'small', 'markerscale': 1.4})
axs[2].set_facecolor('white')
axs[2].set_title("Academic Year 2024-2025", fontsize=16, fontweight='bold', color='black', loc='left', pad=10)
axs[2].text(0, .98, "Students by Application Mailing Location", transform=axs[2].transAxes, fontsize=16, fontweight='bold', color='#cc0033', ha='left')

# Adjusted arrow placement to water areas
axs[2].annotate("Paraguay & Brazil\non the map", xy=(-55, -15), xytext=(-130, -50),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

axs[2].annotate("Continued growth", xy=(80, 20), xytext=(30, -30),
                arrowprops=dict(facecolor='#cc0033', edgecolor='red', arrowstyle='->'), fontsize=10, color='black')

# New annotation for African growth with two arrows
axs[2].annotate("Student growth is occurring\non both coasts of Africa", xy=(0, 5), xytext=(-50, 40),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'), fontsize=10, color='black')

# Arrow to East African coast (Somalia/Kenya region)
axs[2].annotate('', xy=(45, 0), xytext=(-50, 40),
                arrowprops=dict(facecolor='#cc0033', edgecolor='#cc0033', arrowstyle='->'))

# Remove x and y ticks and spines
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

plt.show()

fig = px.treemap(WorldApp, path=[px.Constant("Accepted Offers by Country"), 'Continent', 'Country'], values='Grand Total',
                  color='AC/App%', hover_data=['Country'],
                  color_continuous_scale='RdBu_r',
                  color_continuous_midpoint=np.average(WorldApp['AC/App%'], weights=WorldApp['Grand Total']))
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

#I really like this. I haven't ever seen the data displayed like this. I think it always helps to disaggregate the data. This visualization also helped me to see the weakness of using application rather than enrollment data. This makes sense for applicationdata but it doesn't quite match enrollment trends. CCIB and Public Affairs are big programs in terms of enrollment because they have students whose time to completion is greatewr than 5 years. That's missing here.
import plotly.express as px
fig = px.sunburst(Down, path=['Country', 'Program'], values='Total')
fig.show()
import plotly.express as px
fig = px.sunburst(Down, path=['Program', 'Country'], values='Total')
fig.show()

!pip install leafmap

from geopy.geocoders import GoogleV3
import leafmap
#FASC Undergrads 20241020
# Initialize the geolocator with your Google Maps API key
geolocator = GoogleV3(api_key='AIzaSyDtYAQn3fciPuWXCB7RzRnv-vFstWrXaiY')

def get_lat_long(city, state):
  location = geolocator.geocode(f"{city}, {state}")
  if location:
      return location.latitude, location.longitude
combined_df[['Latitude', 'Longitude']] = combined_df.apply(
    lambda row: pd.Series(get_lat_long(row['CITY'], row['STATE'])), axis=1
)

m = leafmap.Map()

m.add_points_from_xy(
    combined_df,
    x="Longitude",
    y="Latitude",
    color_column="MARKET",
    icon_names=["gear", "map", "leaf", "diamond", 'cube', 'circle'],
    icon_colors = ['red', 'blue','green', 'orange', 'purple', 'black'],
    spin=False,
    add_legend=True,
    popup=["FIRST NAME", "LAST NAME", "CITY", "STATE", "COMP", "COMP2", "MEDIA"]
)
m