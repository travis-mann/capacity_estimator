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
import numpy as np


# --- func ---
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