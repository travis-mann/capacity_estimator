#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
main.py: generates example data set and searches for a capacity
         which includes required_data percent of the total area
         underneath the curve generated by the example data set.
         Can also extract an array from a column in an .xlsx file
         called input.xlsx within the same folder.
"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "1.0"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from bisection import bisection

from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import simps
from random import randint


# --- funcs ---
def generate_data_set(length: int, max_value: int) -> tuple:
    """
    purpose: generate 2 arrays or n length
    :param length: length of arrays to generate
    :param max_value: max y value to generate
    :return:
    """
    print(f'generating data set with {length} elements and {max_value} max value...')
    # get x values
    x_set = np.linspace(0, length - 1, length)

    # generate smooth curve y values
    y_set = np.array([])

    for idx, x_value in enumerate(x_set):
        # 1st value boundary condition
        if idx == 0:
            y_set = np.append(y_set, max_value / 2)  # 1st element is half max value
            continue

        y = randint(0, 1)
        # next value is randomly 1 value up or down from last value to
        # generate smooth curve
        last_value = y_set[idx - 1]
        if y == 0:  # next value is less
            # don't go below 0
            y_set = np.append(y_set, max(last_value - 1, 0))
        elif y == 1:  # next value is more
            # don't exceed max value
            y_set = np.append(y_set, min(last_value + 1, max_value))
        else:
            raise ValueError("Invalid randint")

    # output dataset
    return x_set, y_set


def get_adjusted_data(given_array: np.array, max_value: float) -> np.array:
    """
    purpose: cap array at given value
    """
    return np.array([min(value, max_value) for value in given_array])


def get_percent_covered(array1: np.array, array2: np.array) -> float:
    """
    purpose: get percent of area covered by 2nd array compared to 1st array
    """
    area1 = simps(array1, dx = 1)
    area2 = simps(array2, dx = 1)
    percent_covered = area2 / area1
    return percent_covered


def get_flat_value(required_coverage: float) -> None:
    """
    purpose: high level logic for finding flat value where
    """
    # get dataset
    # generates test curve
    # x, y = generate_data_set(100, 10)

    # extracts dataset from csv
    data = np.genfromtxt('input.csv', delimiter=',')
    x = np.array([row[0] for row in data])
    y = np.array([row[1] for row in data])

    # helper function for bisection search
    def coverage_difference(flat_value: float) -> float:
        """
        purpose:  calculate percent area covereage from curve under flat value
        """
        adjusted_values = get_adjusted_data(y, flat_value)
        percent_covered = get_percent_covered(y, adjusted_values)
        return percent_covered - required_coverage  # area coverage difference from ideal

    # binary search
    # start search with half the max value
    ideal_flat_value = bisection(coverage_difference, 0, max(y))[0]
    print(f'ideal_flat_value: {ideal_flat_value}')
    print(f'percent coverage: {(coverage_difference(ideal_flat_value) + required_coverage) * 100}%')
    flat_values = np.array([ideal_flat_value for i in range(len(x))])

    # plot values
    plt.plot(x, y)  # energy curve
    plt.plot(x, flat_values)  # flat cap
    plt.plot(x, get_adjusted_data(y, ideal_flat_value))  # capped energy curve
    plt.show()


# --- main ---
if __name__ == "__main__":
    get_flat_value(0.7)