import os
import matplotlib.pyplot as plt

def analyze_patents(query):
    os.makedirs("output", exist_ok=True)

    data = {"AI": 30, "IoT": 20, "Robotics": 10}

    plt.figure()
    plt.bar(data.keys(), data.values())
    plt.savefig("output/chart.png")

    return {
        "total_patents": 60,
        "top_keywords": ["AI", "Sensor", "Cloud"],
        "distribution": data
    }
