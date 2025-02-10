import time
import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = os.getenv('CSV_FILE', '/app/logs/metric_log.csv')
IMG_FILE = os.getenv('IMG_FILE', '/app/logs/error_distribution.png')

while True:
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if 'absolute_error' in df.columns and not df['absolute_error'].empty:
                plt.figure(figsize=(8, 6))
                plt.hist(df['absolute_error'], bins=20, color='skyblue', edgecolor='black')
                plt.xlabel('Absolute Error')
                plt.ylabel('Frequency')
                plt.title('Distribution of Absolute Errors')
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(IMG_FILE)
                plt.close()
                print(f"Updated histogram saved as {IMG_FILE}")
            else:
                print("No data available for plotting.")
        except Exception as e:
            print(f"Error reading CSV or generating plot: {e}")
    else:
        print("CSV file not found.")
    
    time.sleep(10)