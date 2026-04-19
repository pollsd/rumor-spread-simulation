import random
import matplotlib.pyplot as plt
# creating a list to keep track of who has heard the rumor and how many times they have heard it
def run_simulation(N, T):
    heard = []
    hear_count = []
    percentage_history = []

    #Initializing the heard and hear_count lists
    for i in range(N):
        heard.append(False)
        hear_count.append(0)

    # Randomly shuffle the participants and divide them into 4 rooms
    participants = list(range(N))
    random.shuffle(participants)

    room_size = N // 4
    room1 = participants[0 : room_size]
    room2 = participants[room_size : 2*room_size]
    room3 = participants[2*room_size : 3*room_size]
    room4 = participants[3*room_size : N]

    rooms = [room1, room2, room3, room4]

    for room in rooms:
        person = random.choice(room)
        heard[person] = True
        hear_count[person] = 1

    for minute in range(T):
        for room in rooms:
            random.shuffle(room)   # shuffle people inside this room for new pairings

            for k in range(0, len(room), 2):
                person1 = room[k]
                person2 = room[k + 1]

                chance_of_hearing = 0.5

                # Save starting state for this pair before making updates
                person1_can_spread = heard[person1] and hear_count[person1] < 2
                person2_can_spread = heard[person2] and hear_count[person2] < 2

                # person1 -> person2
                if person1_can_spread:
                    if random.random() < chance_of_hearing:
                        heard[person2] = True
                        hear_count[person2] += 1

                # person2 -> person1
                if person2_can_spread:
                    if random.random() < chance_of_hearing:
                        heard[person1] = True
                        hear_count[person1] += 1

        percent_heard=sum(heard) / N
        percentage_history.append(percent_heard)
        
    return percentage_history


# Helper function to find the first minute when a certain percentage threshold is reached
def first_time_reaching_threshold(percentage_history, threshold):
    for minute, percent in enumerate(percentage_history, start=1):
        if percent >= threshold:
            return minute
    return None


# Run many simulations and average results. This is our Monte Carlo Engine so that we can get a good average.
def run_experiments(N_values, T, num_runs):
    results_summary = {}
    for N in N_values:
        all_histories = []
        for run in range(num_runs):
            history = run_simulation(N, T)
            all_histories.append(history)
        # Average percentage heard at each minute
        average_history = []
        for minute in range(T):
            total = 0
            for history in all_histories:
                total += history[minute]
            minute_average = total / num_runs
            average_history.append(minute_average)
        # Store averages at required times
        results_summary[N] = {
            "avg_10": average_history[9],   # minute 10
            "avg_30": average_history[29],  # minute 30
            "avg_60": average_history[59],  # minute 60
            "average_history": average_history
        }
        # For N = 10000, also compute average time to reach 10% and 50%
        if N == 10000:
            times_to_10 = []
            times_to_50 = []
            for history in all_histories:
                t10 = first_time_reaching_threshold(history, 0.10)
                t50 = first_time_reaching_threshold(history, 0.50)
                if t10 is not None:
                    times_to_10.append(t10)
                if t50 is not None:
                    times_to_50.append(t50)
            avg_time_10 = sum(times_to_10) / len(times_to_10) if times_to_10 else None
            avg_time_50 = sum(times_to_50) / len(times_to_50) if times_to_50 else None
            results_summary[N]["avg_time_10_percent"] = avg_time_10
            results_summary[N]["avg_time_50_percent"] = avg_time_50
    return results_summary


# Main experiment settings
N_values = [1000, 10000]
T = 60
num_runs = 100
results = run_experiments(N_values, T, num_runs)
# Print results
for N, data in results.items():
    print(f"\nResults for N = {N}")
    print(f"Average % heard at 10 minutes: {data['avg_10'] * 100:.2f}%")
    print(f"Average % heard at 30 minutes: {data['avg_30'] * 100:.2f}%")
    print(f"Average % heard at 60 minutes: {data['avg_60'] * 100:.2f}%")
    if N == 10000:
        print(f"Average time to reach 10% heard: {data['avg_time_10_percent']:.2f} minutes")
        print(f"Average time to reach 50% heard: {data['avg_time_50_percent']:.2f} minutes")



minutes = list(range(1, T + 1))

for N in N_values:
    plt.plot(minutes, results[N]["average_history"], label=f"N = {N}")

plt.title("Average Rumor Spread Over Time")
plt.xlabel("Minute")
plt.ylabel("Average Fraction Heard")
plt.legend()
plt.grid(True)
plt.show()

print("\nSummary Table")
print(f"{'N':<10}{'Avg % at 10':<15}{'Avg % at 30':<15}{'Avg % at 60':<15}")

# Creating a summary table using pandas for better visualization

import pandas as pd

summary_table = pd.DataFrame({
    "N": N_values,
    "Avg % at 10 min": [results[N]["avg_10"] * 100 for N in N_values],
    "Avg % at 30 min": [results[N]["avg_30"] * 100 for N in N_values],
    "Avg % at 60 min": [results[N]["avg_60"] * 100 for N in N_values]
})

print(summary_table)

threshold_table = pd.DataFrame({
    "Metric": ["Avg time to 10% heard", "Avg time to 50% heard"],
    "Value": [
        results[10000]["avg_time_10_percent"],
        results[10000]["avg_time_50_percent"]
    ]
})

print(threshold_table)

summary_table.to_csv("summary.csv", index=False)
threshold_table.to_csv("threshold.csv", index=False)