import sys  
import math  
import random  
from datetime import datetime  
import matplotlib.pyplot as plt 
  
def main(pattern, num_datapoints):  
    on_duration = 5  # on for 5 seconds  
    off_duration = 10  # off for 10 seconds  
    data_points = []  
  
    for i in range(num_datapoints):  
        if pattern == "bursting":  
            # Predictable Bursting Pattern  
            x = int(50 * (math.sin(i / 200 * 2 * math.pi) + 1) + 5)
            if x < 70:  
                x = x * random.uniform(0.2, 1.1)  # increase rate of change when x < 30  
            else:
                x = x * random.uniform(1, 1.1)
        elif pattern == "variations":  
            # Variations Pattern  
            x = random.randint(5, 45)  
        elif pattern == "onoff":  
            # On Off Pattern  
            if i % (on_duration + off_duration) < on_duration:  
                x = 20  # peak traffic  
            else:  
                x = 0  # no traffic  
        else:  
            print("Unknown pattern. Please specify either 'bursting', 'variations', or 'onoff'.")  
            sys.exit(1)  
  
        # Add x (number of requests) to data_points list  
        data_points.append(x)  
  
    # Generate file name  
    file_name = "{}-{}.txt".format(pattern, datetime.now().strftime('%y%m%d-%H%M%S'))  
  
    # Write all data points to file  
    with open(file_name, 'w') as file:  
        file.write('\n'.join(map(str,data_points)))  

    # Plot line chart  
    plt.figure(figsize=(10, 5))  
    plt.plot(data_points)  
    plt.title('Number of Requests Over Time')  
    plt.xlabel('Time (seconds)')  
    plt.ylabel('Number of Requests')  
    plt.show()  
  
  
if __name__ == "__main__":  
    if len(sys.argv) != 3:  
        print(f"Usage: {sys.argv[0]} <pattern> <num_datapoints>")  
        sys.exit(1)  
  
    main(sys.argv[1], int(sys.argv[2]))  
