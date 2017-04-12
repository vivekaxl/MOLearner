# import pylab and numpy
import numpy as np
import pylab as pl

# define datasets
parameters = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
mean_1 = [10.1, 12.1, 13.6, 14.5, 18.8, 11.8, 28.5]
std_1 = [2.6, 5.7, 4.3, 8.5, 11.8, 5.3, 2.5]

mean_2 = [10.1, 12.1, 13.6, 14.5, 18.8, 11.8, 28.5]
std_2 = [2.6, 5.7, 4.3, 8.5, 11.8, 5.3, 2.5]

mean_3 = [10.1, 12.1, 13.6, 14.5, 18.8, 11.8, 28.5]
std_3 = [2.6, 5.7, 4.3, 8.5, 11.8, 5.3, 2.5]


# here comes the plotting;
# to achieve a grouping, two things are extra here:
# 1. Don't use line plot but circular markers and different marker color
# 2. slightly displace the datasets in x direction to avoid overlap
#    and create visual grouping
pl.errorbar(np.array(parameters)-0.01, mean_1, yerr=std_1, fmt='bo')
pl.errorbar(parameters, mean_2, yerr=std_2, fmt='go')
pl.errorbar(np.array(parameters)+0.01, mean_3, yerr=std_3, fmt='ro')
pl.show()