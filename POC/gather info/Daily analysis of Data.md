**Daily analysis of Data**



I used a combined descriptive trend and forecast-validation methodology:

1\. Daily aggregation

&#x20;  I summed the ten receipt categories for each calendar day.

2\. Descriptive trend analysis

&#x20;  For each month, I calculated:

&#x20;  - Total, average, and median daily receipts

&#x20;  - Minimum and maximum days

&#x20;  - Standard deviation and coefficient of variation

&#x20;  - First-half versus second-half averages

&#x20;  - First seven versus last seven days

&#x20;  - Linear trend slope

&#x20;  - Seven-day period averages

&#x20;  - Weekday averages

&#x20;  - Category contribution and month-over-month change

3\. Linear trend estimation

&#x20;  I fitted a straight line:

&#x20;  \\\[

&#x20;  \\text{Daily receipts} = a + b \\times \\text{day number}

&#x20;  \\]The coefficient \\(b\\) measures the estimated daily increase or decrease. This is used to describe direction, not as the primary forecast.

4\. Forecast-model comparison

&#x20;  I used June as the initial history and tested one-day-ahead predictions against actual July results. Models compared included:

&#x20;  - Previous-day value

&#x20;  - Seven-day moving average

&#x20;  - Same weekday from the previous week

&#x20;  - Simple exponential smoothing

&#x20;  - Damped Holt trend

&#x20;  - Holt-Winters weekly seasonality

5\. Model selection

&#x20;  I compared models using:

&#x20;  - MAE: average number of receipts by which predictions were wrong

&#x20;  - MAPE: average percentage forecast error

&#x20;  - RMSE: gives more weight to large errors

&#x20;  - Forecast bias

Simple exponential smoothing produced the lowest July MAPE at approximately 7.13%, so I recommended it for daily forecasts. The seven-day moving average is used as a supporting visualization because it makes the underlying trend easier to interpret.

One limitation is that May data is absent. Therefore, the available history is too short and discontinuous to establish dependable monthly or weekly seasonality.

