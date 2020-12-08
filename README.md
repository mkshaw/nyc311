# NYC 311 Response Time Dashboard

Create a dashboard displaying 311 response times for incidents filed in 2020. Assess whether there are response time discrepancies by viewing response time (hours elapsed between complaint filing and closing) for up to two zip codes in New York City, as well as the average response time across all zip codes.

Run the dashboard by executing the following code from outside of `nyc_dash`. 

`bokeh serve --address='*' --port=port_number --allow-websocket-origin=IP_address:port_number --auth=auth.py nyc_dash`
