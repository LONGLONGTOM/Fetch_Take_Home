from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from statsmodels.tsa.arima.model import ARIMAResults

app = Flask(__name__)
sarima_result = ARIMAResults.load('sarima_result.pkl')

def create_plot(data, forecast_df ,title, xlabel, ylabel):
    plt.figure(figsize=(15, 6))
    
    data['Date'] = pd.to_datetime(data['Date'])
    
    if xlabel == 'Month':
        # monthly_data_2021 = data.groupby(data['Date'].dt.to_period('M'))['Receipt_Count'].sum()

        monthly_data_2021 = data.groupby(data['Date'].dt.to_period('M')).sum().to_timestamp()
        monthly_data_2021.index = monthly_data_2021.index.to_series().dt.strftime('%Y-%m')

        forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
        monthly_forecast_2022 = forecast_df.groupby(forecast_df['Date'].dt.to_period('M')).sum().to_timestamp()
        monthly_forecast_2022.index = monthly_forecast_2022.index.to_series().dt.strftime('%Y-%m')
        
        # Plot 2021 data
        plt.plot(monthly_data_2021.index, monthly_data_2021['Receipt_Count'], label='2021 Monthly Data', marker='o', linestyle='-', color='orange')

        # Plot 2022 forecast
        plt.plot(monthly_forecast_2022.index, monthly_forecast_2022['Forecast'], label='2022 Monthly Forecast', marker='x', linestyle='-')

        plt.plot([monthly_data_2021.index[-1], monthly_forecast_2022.index[0]], 
                 [monthly_data_2021['Receipt_Count'][-1], monthly_forecast_2022['Forecast'][0]], 
                 marker='', linestyle='-', color='orange')

        plt.title('Monthly Receipt Counts: 2021 and Forecast for 2022')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
    elif xlabel == 'Day':
        plt.plot(data['Date'], data['Receipt_Count'], label='2021 Data', color='orange')
        plt.plot(forecast_df['Date'], forecast_df['Forecast'], label='2022 Forecast')
        plt.title('2021 Receipt Counts and 2022 Forecast')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    plt.legend()
    plt.xticks(rotation=45)  
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(plot_url)

@app.route('/')
def index():
    """Page showing both monthly and daily data visualizations."""
    # Load and preprocess the data
    data = pd.read_csv('data_daily.csv', parse_dates=['# Date'])
    data = data.rename(columns={'# Date': 'Date'})
    forecast_days = 365  

    # Generating the forecast
    forecast = sarima_result.get_forecast(steps=forecast_days)
    forecast_index = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')
    forecast_values = forecast.predicted_mean

    # Creating a DataFrame for the forecast
    forecast_df = pd.DataFrame({'Date': forecast_index, 'Forecast': forecast_values})

    # Monthly data
    monthly_plot_url = create_plot(data, forecast_df,'Monthly Scanned Receipts: 2021 and 2022 Forecasted', 'Month', 'Number of Receipts')

    # Daily data
    daily_plot_url = create_plot(data, forecast_df,'Daily Scanned Receipts: 2021 and 2022 Forecasted', 'Day', 'Number of Receipts')

    return render_template('index.html', monthly_plot_url=monthly_plot_url, daily_plot_url=daily_plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
