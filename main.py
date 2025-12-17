import pandas as pd
import matplotlib.pyplot as plt
import os

# PEOPLE_TO_PLOT = ['Colby', 'Eva']
PEOPLE_TO_PLOT = ['Eva']

def main():
    # Define the path to the data file
    data_file = os.path.join('data', 'data1.csv')

    # Read the CSV file
    if not os.path.exists(data_file):
        print(f"Error: The file {data_file} was not found.")
        return

    df = pd.read_csv(data_file)

    # Convert 'Session Time' to datetime objects
    # Format in CSV example: 12/14/2025 6:30 PM
    df['Session Time'] = pd.to_datetime(df['Session Time'], format='%m/%d/%Y %I:%M %p')

    # Sort by date and attempt
    df = df.sort_values(['Session Time', 'Consecutive Attempt #'])

    # Plotting
    plt.figure(figsize=(12, 7))

    # Define distinct, complementary color palettes for each person
    person_attempt_colors = {
        'Colby': {1: 'teal', 2: 'red', 3: 'slateblue', 4: 'forestgreen', 5: 'chocolate'},
        'Eva': {1: 'magenta', 2: 'darkorange', 3: 'mediumseagreen', 4: 'deeppink', 5: 'darkcyan'}
    }
    # Define line styles for each person
    person_linestyles = {'Colby': '-', 'Eva': '--'}
    person_markers = {'Colby': 'o', 'Eva': 's'}
    
    people = df['Person'].unique()
    attempts = sorted(df['Consecutive Attempt #'].unique())
    
    # Define colors for session averages
    person_avg_colors = {'Colby': 'black', 'Eva': 'dimgray'}
    
    for person in people:
        if person not in PEOPLE_TO_PLOT:
            continue

        linestyle = person_linestyles.get(person, '-')
        marker = person_markers.get(person, 'o')
        colors = person_attempt_colors.get(person, {})
        
        for attempt in attempts:
            # Filter data for this person and attempt number
            df_subset = df[(df['Person'] == person) & (df['Consecutive Attempt #'] == attempt)]
            
            if df_subset.empty:
                continue
            
            color = colors.get(attempt, 'gray')
            
            # Plot line connecting points for this person/attempt combo
            plt.plot(df_subset['Session Time'], df_subset['Time (s)'], 
                     color=color, linestyle=linestyle, marker=marker,
                     label=f'{person} set {attempt}', alpha=0.8)
        
        # Calculate and plot session averages for this person
        df_person = df[df['Person'] == person]
        session_avg = df_person.groupby('Session Time')['Time (s)'].mean().reset_index()
        session_avg = session_avg.sort_values('Session Time')
        
        avg_color = person_avg_colors.get(person, 'gray')
        plt.plot(session_avg['Session Time'], session_avg['Time (s)'], 
                 color=avg_color, linestyle=linestyle, marker='D', markersize=8,
                 linewidth=2.5, label=f'{person} session avg', alpha=0.9)

    plt.title('Breath Hold Progression')
    plt.xlabel('Date')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
