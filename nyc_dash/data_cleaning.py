"""
data_cleaning.py

Process massive datafile nyc_311_filtered.csv.

Make it tidy, with one zipcode-month per row, and the
average incident create-to-closed time (in hours) per
that month. Additionally, the last row should be the
average of all averages, which is the average create-to-closed
time (in hours) for all of 2020.

main.py should then load a copy of this cleaned dataset,
and when users toggle a zipcode, it will filter the data
to just that zipcode and graph x = month, y = create_to_closed_average
for that zipcode. Plus, the graph should always graph 
the averages for all of 2020 (that last row of the dataframe).
"""

import pandas
import os.path as osp

def main():

    # read csv to dataframe
    df = pandas.read_csv(osp.join(osp.dirname(__file__), "..", "data", "nyc311.csv"))

    # add columns
    df.columns = ['created_date', 'closed_date', 'incident_zip']

    # select rows for which closed_date is not NaN, i.e., select rows for CLOSED incidents (ones that have closed dates)
    df_zip_closed = df[df['closed_date'].notnull()]

    # remove NaN zips
    df_fin = df_zip_closed[df_zip_closed['incident_zip'].notnull()]

    # Calculate the hours elapsed per row

    days_elapsed = ()
    days_elapsed = (pandas.to_datetime(df_fin['closed_date']) - (pandas.to_datetime(df_fin['created_date'])))

    hours_elapsed = days_elapsed.apply(lambda x: x.total_seconds() / 3600)

    df_fin['hours_elapsed'] = hours_elapsed

    # filter out negative hours_elapsed, which arise from input errors where closed_date is before created_date

    df_fin_correct = df_fin[df_fin['hours_elapsed'] >= 0.0]

    # Create month column
    df_fin_correct['month'] = pandas.to_datetime(df_fin_correct['closed_date']).dt.month

    # Create copy so that df_overall can group properly (because df_months alters df_fin)
    df_fin_correct_cpy = df_fin_correct.copy()

    # Group by zipcode and month, get average hours per month
    df_months = df_fin_correct.groupby(['incident_zip', 'month']).mean()

    # Calculate total 2020 average per month
    df_overall = df_fin_correct_cpy.groupby(['month']).mean()

    # Export data to CSVs for bokeh (to outside of the nyc_dash dir, because bokeh called in hw/hw4
    df_months.to_csv("nyc_311_months_closed.csv")
    df_overall.to_csv("nyc_311_overall_closed.csv")

if __name__ == '__main__':
    main()
