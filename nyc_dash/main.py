from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
import pandas as pd

# IMPORT DATA
df_month = pd.read_csv("nyc_311_months_closed.csv")
df_overall = pd.read_csv("nyc_311_overall_closed.csv")

# FILTER DATA BASED ON USER INPUT

x_overall = df_overall['month']
y_overall = df_overall['hours_elapsed']

# GENERATE STARTING GRAPHS

source_overall = ColumnDataSource(df_overall)

source_zip1 = ColumnDataSource(data = {
    'x': [0],
    'y': [0]
})

source_zip2 = ColumnDataSource(data = {
    'x': [0],
    'y': [0]
})

p = figure(title = "Average 311 Response Times by Month of Incident Creation", x_axis_label = "Month", y_axis_label = "Average Response Time (Hours)")

# ADD INITIAL LINES

p.line(source = source_overall, x = 'month', y = 'hours_elapsed', line_color = "black", legend_label = "All Zipcodes")
p.line('x', 'y', source = source_zip1, line_color = "blue", legend_label = "Zipcode 1")
p.line('x', 'y', source = source_zip2, line_color = "orange", legend_label = "Zipcode 2")

# HANDLE CALLBACKS ... user choice of incident_zip from dropdown

def update_zip1(attr, old, new):
    df_zip1 = df_month[df_month['incident_zip'] == float(select_zip1.value)]
    source_zip1.data = {
            'x': df_zip1['month'],
            'y': df_zip1['hours_elapsed']
    }

def update_zip2(attr, old, new):
    df_zip2 = df_month[df_month['incident_zip'] == float(select_zip2.value)]
    source_zip2.data = {
            'x': df_zip2['month'],
            'y': df_zip2['hours_elapsed']
    }

# list of zipcodes to display in dropdown
zipcodes = df_month.incident_zip.unique().tolist()
string_zipcodes = [str(zipcode) for zipcode in zipcodes]

# CREATE DROPDOWN WIDGET
select_zip1 = Select(title = "zipcode 1", options = string_zipcodes, value = None)
select_zip2 = Select(title = "zipcode 2", options = string_zipcodes, value = None)

# ATTACH UPDATE_ZIP1 CALLBACK TO 'VALUE' PROPERTY OF SELECT_ZIP1
select_zip1.on_change('value', update_zip1)
select_zip2.on_change('value', update_zip2)

# FORMAT/CREATE THE DOCUMENT TO RENDER
# curdoc().add_root(column(p))
curdoc().add_root(column(select_zip1, select_zip2, p))
