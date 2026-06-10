import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sqlalchemy import create_engine
from urllib.parse import quote_plus 

# Data Cleaning, Processing and Extracting------------------/

df=pd.read_csv(r"D:\Global_GDP_Analysis\data\2020-2025.csv")

print(df.head())

print(df.tail())

print(df.shape)

print(df.columns)

df.info()

print(df.isnull().sum())

print(df.duplicated().sum())

print(df.describe())

# Database Connection -----------------------------------------/

password=quote_plus("Omkar123")
engine=create_engine(f'postgresql://postgres:{password}@localhost:1112/Gdp_Analysis')

print("Connection Successful")

df.to_sql('2020-2025',engine,if_exists='replace',index=False)

query=""" Select "Country", SUM("GDP") AS Total_GDP
          From "Gdp_data"
          GROUP BY "Country"
          ORDER BY Total_GDP DESC
          LIMIT 10;
          """
Top10_sql=pd.read_sql(query,engine)

print(Top10_sql)

print(Top10_sql.columns)

Top10_sql['total_gdp']=Top10_sql['total_gdp']/1_000_000

plt.figure(figsize=(12,6))

ax=plt.bar(Top10_sql['Country'],
           Top10_sql['total_gdp'],
           color='skyblue'
           )

plt.title("Top 10 Countries by Total GDP (2020-2025)",fontsize=16)

plt.xlabel("Country")

plt.ylabel("GDP(Trillion USD)")

plt.gca().yaxis.set_major_formatter(

    FuncFormatter(
        lambda x, pos: f'${x:.0f} Trillion'
    )

)

plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()


plt.xticks(rotation=45)

plt.show()



# Top 10 countries with GDP for Year (2025)---------------------------------/

top10=df.groupby('Country')['GDP'].max().sort_values(ascending=False).head(10)

print(top10)
 
top10 = top10 / 1_000_000

plt.figure(figsize=(12,6))

ax = top10.plot(kind='bar')

plt.title('Top 10 Countries by Total GDP (2025)', fontsize=16)

plt.xlabel('Countries', fontweight=16,fontsize=15)

plt.ylabel('GDP (Trillion USD)', fontsize=12)

plt.xticks(rotation=45)

# Add labels on bars
for p in ax.patches:
    
    ax.annotate(
        f'${p.get_height():.2f} Trillion',
        
        (p.get_x() + p.get_width()/2,
         p.get_height()),
        
        ha='center',
        va='bottom',
        
        fontsize=10
    )

plt.tight_layout()

plt.show()

# GDP Trend Over Years--------------------------------------/

gdp_by_year = df.groupby('Year')['GDP'].sum()

gdp_by_year = gdp_by_year / 1_000_000

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(
    gdp_by_year.index,
    gdp_by_year.values,
    marker='o'
)

plt.title("Global Total GDP Trend (2020-2025)", fontsize=16)

plt.xlabel("Year", fontsize=12)

plt.ylabel("GDP (Trillion USD)", fontsize=12)

ax.yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f'${x:.2f}T')
)

plt.grid(True)

plt.show()

#-------------------GDP Growth Rate-------------------------/
 
df['GDP Growth %'] = (
    df.groupby('Country')['GDP']
      .pct_change() * 100
)

countries = ['India', 'China', 'United States']

filtered = df[df['Country'].isin(countries)]

plt.figure(figsize=(10,6))

for country in countries:

    data = filtered[filtered['Country'] == country]

    plt.plot(
        data['Year'],
        data['GDP Growth %'],
        marker='o',
        label=country
    )
    
plt.title('GDP Growth Rate Comparison', fontsize=16)

plt.xlabel("Year", fontsize=12)

plt.ylabel("GDP Growth (%)", fontsize=12)
 
plt.xticks(data['Year'])

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f'{x:.1f}%')
)

plt.legend()

plt.grid(True)

plt.show()