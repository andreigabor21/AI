from __future__ import annotations
from utils import *
import operator
import math
from random import sample
from typing import List, Tuple


CONVERGENCE = 0.000001

class Point:
    def __init__(self, x: float, y: float, label: str) -> None:
        self.x = x
        self.y = y
        self.label = label
        self.cluster = None

    def distance(self, other_x: float, other_y: float) -> float:
        current_point = (self.x, self.y)
        other_point = (other_x, other_y)
        return math.dist(current_point, other_point)

    def closest_cluster(self, clusters: List[Cluster]) -> Cluster:
        return min(clusters, key = lambda centroid: self.distance(centroid.mean_x, centroid.mean_y))


class Cluster:
    def __init__(self, label: str) -> None:
        self.label = label
        self.points = []
        self.mean_x = 0
        self.mean_y = 0

    def addPoint(self, point: Point):
        self.points.append(point)
        if point.cluster:
            point.cluster.points.remove(point)
        point.cluster = self
        return self.update_means()

    def update_means(self) -> bool:
        self.mean_x = sum(list(map(lambda point: point.x, self.points))) / len(self.points)
        self.mean_y = sum(list(map(lambda point: point.y, self.points))) / len(self.points)

        old_centroid_x = self.mean_x
        old_centroid_y = self.mean_y
        if abs(self.mean_x - old_centroid_x) <= CONVERGENCE and abs(self.mean_y - old_centroid_y) <= CONVERGENCE:
            return False
        return True

    def update_label(self) -> None:
        freq = { 'A':0, 'B':0, 'C':0, 'D':0 }
        for point in self.points:
            freq[point.label] += 1
        self.label = max(freq.items(), key=operator.itemgetter(1))[0]

    def compute_statistics(self, points: List[Point]) -> Tuple[float, float, float, float]:
        '''
        TP is the number of true positives
        TN is the number of true negatives
        FP is the number of false positives
        FN is the number of false negatives
        '''
        TP = FP = TN = FN = 0
        for point in self.points:
            if point.label == self.label:
                TP += 1
            else:
                FP += 1
        for point in points:
            if point not in self.points:
                if point.cluster.label != self.label:
                    if point.label != self.label:
                        TN += 1
                    else:
                        FN += 1
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        precision = TP / (TP + FP)
        rappel = TP / (TP + FN)
        score = 2 * precision * rappel / (precision + rappel)
        return accuracy, precision, rappel, score


if __name__ == '__main__':
    clusters = []
    points = read_points()
    clusters.append(Cluster('A'))
    clusters.append(Cluster('B'))
    clusters.append(Cluster('C'))
    clusters.append(Cluster('D'))
    random_points = sample(points, 4)
    for i in range(0, 4):
        clusters[i].mean_x = random_points[i].x
        clusters[i].mean_y = random_points[i].y

    ok = True
    while ok:
        ok = False
        for p in points:
            optimal_cluster = p.closest_cluster(clusters)
            if optimal_cluster.addPoint(p):
                ok = True
    for i in clusters:
        i.update_label()

    print_statistics(clusters, points)
    plot(clusters)
