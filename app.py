import numpy as np
import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash

from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


response_p1 = """
There are so many conflicting claims that are made on gender wage gap and poeple have different questions about this matter. 
This epi.org ["What is the gender pay gap and is it real?"](https://www.epi.org/publication/what-is-the-gender-pay-gap-and-is-it-real/) article tries to answe some of the commen questions people ask about this matter. The questions and a summary of
the answers are provided below.

1. How much do womenn make compared to men?

This is one of the most commenly asked question in this space and people usually mentions numbers that are adjusted one way or another to fit their narrative.
In this article the wage gap is, "for every dollar a man makes a women makes only 80 cents" when this number is calculated in an hourly basis the number increases slightly.
There variations of this numbers but the 80 to 85 cent range is the most commen and reliable. 



2. Does the wage gap vary base on the type of job?
The writting states that the wage gap is much higher for workers who are at the lower end of the wage distribution that it is in the higher end. This is usually attributed 
to the minimum wage. It is also stated that the wage gap for the higher 5 percentile of the distribution is 0.92 and the lower percentile is 0.76. This shows even for high
level jobs such as excutives women are paid way less than their male counter parts and this gap gets even larger for the bottom 5 percent workers in the wage distribution. 


The other important resource on gender wage gap is  [payscale.com](https://www.payscale.com/data/gender-pay-gap). Ths resource have a number of usefully data on their website.
The most interesting one explores the impact of covid-19 layoff and its current and future effects on the wage gap. Eventhough the lay of is impacting everybody across the board 
Women have a higher number interms of layoff. Thsi number maybe attributed to the time of jobs where women are traditionally concentrated.

There is also data that show the gender gap overtime. There definatly is an upward trend but the the improvement is definaly not enough to fill the enourmous gap that was created
over seveall centuries. The current UN secretary stated this on an article on this issue [Women and Girls – Closing the Gender Gap] (https://www.un.org/en/un75/women_girls_closing_gender_gap) , saying that with the current trend the wage gap will not be closed in the next 100 years.

"""

sex_group =gss_clean.groupby('sex').agg({ 'income':'mean','job_prestige':'mean', 'socioeconomic_index':'mean', 'education':'mean'}).reset_index().round(2)
sex_group = sex_group[['income','job_prestige','socioeconomic_index','education']].round(2)
table =ff.create_table(sex_group, colorscale=[[0, '#5B172C'],[.5, '#000000'],[1, 'blue']], font_colors=['#ffffff', '#ffffff','#ffffff'])


anes_goupbar = gss_clean.groupby(['sex','male_breadwinner']).agg({'sex':'count'}).reset_index('male_breadwinner')
new_groupss = gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index()
anes_goupbar =anes_goupbar.rename_axis('sex_c').reset_index()
new_groupss.columns = ['Sex', 'Male Breadwinner', 'size']
fig_bar = px.bar(new_groupss, y = 'size', x='Male Breadwinner', color='Sex',opacity=0.5,
                 color_discrete_map = {'male':'#000000', 'female':'blue'})
fig_bar.update_layout({
    'plot_bgcolor':'#5B172C',
    'paper_bgcolor':"#5B172C"
})
fig_bar.update_yaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)
fig_bar.update_xaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)

fig_bar.update_layout(
    font_family="Rockwell",
    legend=dict(
        title="", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center",font=dict(
            family="Courier",
            size=15,
            color="#ffffff")
    )
)


fig_scatter = px.scatter(gss_clean, x = 'job_prestige', y ='income', color='sex',
                         trendline='ols',
                         labels = {'job_prestige':'Occupational Presige','income':'Annual Income'} ,
                        hover_data = ['education','socioeconomic_index'],
                         color_discrete_map = {'male':'#000000', 'female':'blue'})
fig_scatter.update(layout=dict(title=dict(x=0.5)))

fig_scatter.update_layout({
    'plot_bgcolor':'#5B172C',
    'paper_bgcolor':"#5B172C"
})

fig_scatter.update_yaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)
fig_scatter.update_xaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)

fig_scatter.update_layout(
    font_family="Rockwell",
    legend=dict(
        title="", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center",font=dict(
            family="Courier",
            size=15,
            color="#ffffff")
    )
)


fig_box = px.box(gss_clean, x='income', y ='sex', color='sex',
             labels = {'income':'Annual Income', 'sex':''},
                 color_discrete_map = {'male':'#000000', 'female':'blue'})

fig_box.update_layout(showlegend=False)
fig_box.update_layout({
    'plot_bgcolor':'#5B172C',
    'paper_bgcolor':"#5B172C"
})

fig_box.update_yaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)
fig_box.update_xaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)


fig_box2 = px.box(gss_clean, x='job_prestige', y ='sex', color='sex', 
             labels={'job_prestige':'Occupational Prestige', 'sex':''},
                 color_discrete_map = {'male':'#000000', 'female':'blue'})

fig_box2.update_layout(showlegend=False)
fig_box2.update_layout({
    'plot_bgcolor':'#5B172C',
    'paper_bgcolor':"#5B172C"
})

fig_box2.update_yaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)
fig_box2.update_xaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)




new_gss_clean = gss_clean[['income', 'sex','job_prestige']]
new_gss_clean['job_pre_category']= pd.cut(new_gss_clean.job_prestige,bins=6, labels=('Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6') )
new_gss_clean.dropna(inplace=True)
fig_fac_box = px.box(new_gss_clean, x='income', y='sex', color='sex',
                    labels={'income':'Annual Income', 'job_pre_category':'Job Prestige'},
                     facet_col='job_pre_category', facet_col_wrap=2,
                     color_discrete_map = {'male':'#000000', 'female':'blue'},
                    )

fig_fac_box.update_layout({
    'plot_bgcolor':'#5B172C',
    'paper_bgcolor':"#5B172C"
})
fig_fac_box.update_yaxes(
    tickprefix="", showgrid=False, color='#ffffff'
   
)
fig_fac_box.update_xaxes(
    tickprefix="", showgrid=False, color='#ffffff' 
)

fig_fac_box.update_layout(
    font_family="Rockwell",
    legend=dict(
        title="", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center",font=dict(
            family="Courier",
            size=15,
            color="#ffffff")
    ))


subset =gss_clean[['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']]
all_cat = []
for i, col in enumerate([x for x in subset]):
    temp =subset[col].unique()
    for x in temp:
        all_cat.append(x)
all_cat = [all_cat for all_cat in all_cat if str(all_cat) != 'nan']

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
        'crossorigin': 'anonymous'
    }
]


appe = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])
server = appe.server
appe.layout = html.Div(
    [
        html.H1(children ="General Social Servey Data Dahboard",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),

                html.Div([
               
       dcc.Markdown(children=response_p1)
            
        ], style = {'width':'48%', 'float':'right'} ),
        html.Div([
               
       dcc.Markdown(children=response_p1)
            
        ], style = {'width':'48%', 'float':'right'} ),
        
        
        html.H3("The difference in occupational prestige, income, socioeconomic status and education between men and women",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
        
        dcc.Graph(figure=table),
        
        html.H3("Response for the question everybody is better off if men are bread winners and women take care of the house",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
        
    
        
        
        html.H3("All Categories"),
    
    dcc.Dropdown(id='x-axis',
        options=[{'label': i, 'value': i} for i in all_cat],
        value='agree'),
            
    html.H3("Choose Sex"),
            
    dcc.Dropdown(id='y-axis',
        options=[{'label': i, 'value': i} for i in ['male', 'female']],
        value='female'),
        
        dcc.Graph(id ='fig_bar'),
        
        
        
        
        
        
        html.H3(" Relationship between occupational prestige and income for men and women",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
        
        dcc.Graph(figure=fig_scatter),
        

        
        html.Div([
            html.H2("Distribution of annual income for women and men",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
            dcc.Graph(figure=fig_box)          
        ],  style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2(" Distribution of occupational prestige for women and men",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
            
            dcc.Graph(figure=fig_box2)
            
        ], style = {'width':'48%', 'float':'right'} ),
        
        
        html.H1("Distribution of income in prestige catagories for women and men",style={
            'textAlign': 'center',
            'color': '#6D71BC'
        }),
        dcc.Graph(figure=fig_fac_box)
    ]
)

@appe.callback(Output(component_id="graph",component_property="figure"), 
             [Input(component_id='x-axis',component_property="value"),
              Input(component_id='y-axis',component_property="value"),
              Input(component_id='color',component_property="value")])


# fig_bar = px.bar(new_groupss, y = 'size', x='Male Breadwinner', color='Sex',opacity=0.5,
#                  color_discrete_map = {'male':'#000000', 'female':'blue'})

def make_figure(x, y, color):
    return px.bar(
        gss_clean,
        x=x,
        y=y,
        color=color,
        trendline='ols',
        hover_data=['sex', 'partyID', 'vote', 'ideology'],
        height=700,
        opacity = .25
)

if __name__ == '__main__':
    appe.run_server(debug=True)
