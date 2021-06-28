from __future__ import annotations

import csv
from typing import List
import matplotlib.pyplot as plt
from clustering import Point, Cluster


def read_points() -> List[Point]:
    points = []
    with open('dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                point = Point(float(row[1]), float(row[2]), row[0])
                points.append(point)
                line_count += 1
    return points

def print_statistics(clusters: List[Cluster], points: List[Point]):
    for c in clusters:
        accuracy, precision, rappel, score = c.compute_statistics(points)
        print(c.label)
        print("Accuracy " + str(accuracy))
        print("Precision " + str(precision))
        print("Rappel " + str(rappel))
        print("Score " + str(score))
        print("\n")

def plot(clusters: List[Cluster]):
    for cluster in clusters:
        x = [point.x for point in cluster.points]
        y = [point.y for point in cluster.points]
        symbol = ''
        if cluster.label == 'A':
            symbol = 'ro'
        if cluster.label == 'B':
            symbol = 'bo'
        if cluster.label == 'C':
            symbol = 'go'
        if cluster.label == 'D':
            symbol = 'yo'
        plt.plot(x, y, symbol, label = cluster.label)
    plt.legend()
    plt.show()