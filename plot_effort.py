import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

PERSON_NAME = 'Colby'

def main():
    data_file = os.path.join('data', 'data1.csv')
    if not os.path.exists(data_file):
        print(f"File not found: {data_file}")
        return

    df = pd.read_csv(data_file)
    
    df_person = df[df['Person'] == PERSON_NAME]

    if df_person.empty:
        print(f"No data found for {PERSON_NAME}")
        return

    x = df_person['Effort [0,1]']
    y = df_person['Time (s)']

    plt.figure(figsize=(10, 6))
    
    # Scatter plot
    plt.scatter(x, y, color='blue', label='Actual Data', s=100)

    # Linear Regression
    if len(df_person) > 1:
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        
        # Create a range for the line, extending from 0 to 1.0
        x_line = np.linspace(0, 1.0, 100)
        y_line = polynomial(x_line)
        
        predicted_max = polynomial(1.0)
        
        plt.plot(x_line, y_line, color='red', linestyle='--', label=f'Trend Line')
        
        # Mark the max effort point
        plt.plot(1.0, predicted_max, 'r*', markersize=15, label=f'Predicted Max: {predicted_max:.1f}s')
        
        # Add text annotation for the max value
        plt.annotate(f"{predicted_max:.1f}s", (1.0, predicted_max), 
                     xytext=(-20, 10), textcoords='offset points', color='red', fontweight='bold')

    plt.title(f'Breath Hold Time vs Effort ({PERSON_NAME})')
    plt.xlabel('Effort [0,1]')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1.1) # Set x-axis to show 0 to slightly past 1
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
