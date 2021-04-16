# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 19:45:44 2021

@author: Michael Lin
"""
import numpy as np
import copy
# Implementation of the closest set of two points in a plane


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MinimumDistanceCalculator:
    def __init__(self, point_list):
        self.point_list = point_list

    def __len__(self):
        return len(self.point_list)

    def minimum_dist_brute_force(self, point_list):
        """
        Return the smallest distance between two points
        :param point_list: list of points
        :return: smallest distance
        """
        min_val = float('inf')
        n = len(point_list)
        for i in range(n):
            for j in range(i+1, n):
                if dist(point_list[i], point_list[j]) < min_val:
                    min_val = dist(point_list[i], point_list[j])
        return min_val

    def strip_closest(self, strip_list, d):
        """
        Find the closest distance between the closest points in a strip
        :param strip_list: list of points in strip
        :param d: minimum distance in the recursive halves
        :return: smallest distance
        """
        minimum = d
        size = len(strip_list)
        for i in range(size):
            j = i + 1
            # Need to make sure the difference between the two points in strip list
            # have a distance less than the minimum distance in the recursive halves
            # else there is no point is doing the comparison
            while j < size and strip_list[j].y - strip_list[i].y < minimum:
                if dist(strip_list[i], strip_list[j]) < minimum:
                    minimum = dist(strip_list[i], strip_list[j])
                j += 1
        return minimum

    def _minimum_distance(self, point_list):
        # Variable initiation
        n = len(point_list)
        point_list_x_sort = copy.deepcopy(point_list)
        point_list_x_sort.sort(key=lambda val: val.x)
        point_list_y_sort = copy.deepcopy(point_list)
        point_list_y_sort.sort(key=lambda val: val.y)

        # If length is less than 3, calculate the minimum distance
        if n <= 3:
            return self.minimum_dist_brute_force(point_list_x_sort)

        midpoint = n // 2
        benchmark = point_list_x_sort[midpoint].x
        # Find the minimum distance for both recursive halves
        left, right = point_list_x_sort[:midpoint], point_list_x_sort[midpoint:]
        minimum_dist_left = self._minimum_distance(left)
        minimum_dist_right = self._minimum_distance(right)
        d = min(minimum_dist_left, minimum_dist_right)

        # Now that the minimum distance for both recursive halves are calculated,
        # collect the points that are closest to the strips using the difference between x coordinates
        strip_list = []
        for i in range(n):
            if abs(point_list_y_sort[i].x - benchmark) < d:
                strip_list.append(point_list_y_sort[i])

        return min(d, self.strip_closest(strip_list, d))

    def minimum_distance(self):
        """
        Trigger the implementation underneath
        :return: minimum_distance
        """
        return self._minimum_distance(self.point_list)


# Not part of any classes as this can be used elsewhere
def dist(p1, p2):
    """
    Find the distance between the two points
    :param p1: point 1
    :param p2: point 2
    :return: distance
    """
    return np.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


def main():
    point_list = [Point(2, 3), Point(12, 30), Point(40, 50), Point(5, 1), Point(12, 10), Point(3, 4)]
    calculator = MinimumDistanceCalculator(point_list)
    print(calculator.minimum_distance())


if __name__ == '__main__':
    main()
