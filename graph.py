import plotly.express as px
import pandas as pd

''' 
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
print(df)
fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

fig = px.bar(df, x="Date", y="AAPL.High",  title="bar on Date Axes")
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
'''

def sleep_time_to_num(time_str, start):
    l = []
    for t in time_str:
        hh, mm  = map(int, t.split(':'))
        if start:
            l.append(mm + 60*hh - 24*60)
        else: 
            l.append(mm + 60*hh)
    return l


d = {'Date': ['2015-02-17', '2015-02-18', '2015-02-19', '2015-02-20'], 
     'Start sleep1': ['23:30', '23:10','23:40','23:00' ], 
     'End sleep1': ['8:30', '9:10','8:40','7:00' ]
     }
df = pd.DataFrame(data=d)
df['Start sleep'] = sleep_time_to_num(df['Start sleep1'], 1)
df['End sleep'] = sleep_time_to_num(df['End sleep1'], 0)
df['Duration'] = df['End sleep'] - df['Start sleep'] 

print(df)
fig = px.bar(df, x="Date", y=["Start sleep", 'End sleep'], color='Duration', title="Графики сна")
fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = [-180, -120, -60, 0, 60, 120, 180, 240, 300, 360, 420, 480, 540],
        ticktext = ['21:00', '22:00','23:00','0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00',]
    )
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

fig.show()
