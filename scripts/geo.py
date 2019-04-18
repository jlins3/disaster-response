import geopandas as gpd
import random
from shapely.geometry import Point
import math
import pandas as pd
import glob
import csv
import sys

# import US states shape file get california geo coordinate outline
state_boundary_us = gpd.read_file("./Data/spacial-data/usa/usa-states-census-2014.shp")
state_boundary = state_boundary_us[['NAME', 'geometry']]
states_agg = state_boundary.dissolve(by='NAME', aggfunc='sum')
cali = states_agg[3:4]
cali.reset_index(level=0, inplace=True)
cal = cali.envelope  # california outline


# generates random coordinates and writes to napa_coordinates.txt
def generate_random(num, filename):
    """This function take in a number of points to be generated and a polygon outline of the state in which you wish
    to generate data. The polygon for the state of california was generated above."""
    list_of_points = []
    vals = cali.bounds
    minx = int(vals['minx'].values)
    miny = int(vals['miny'].values)
    maxx = int(vals['maxx'].values)
    maxy = int(vals['maxy'].values)
    counter = 0
    num_one = round(int(num) * .5)  # .5 for the state
    num_two = round(int(num) * .5)  # .5 for the concentrated radius

    for i in range(num_one):
        while counter < num_one:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

            if cali['geometry'].loc[0].contains(pnt):
                list_of_points.append(pnt)
                counter += 1

    geopoint = sum(map(list, (p.coords for p in list_of_points)), [])

    # randomly generated points around a focused radius
    radius = 160934  # Choose radius
    radius_in_degrees = radius / 111300
    r = radius_in_degrees
    x0 = 38.557428
    y0 = -121.501336

    for i in range(num_two):
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))

        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        x_lat = x + x0
        xlong = y + y0
        geopoint.append(tuple((xlong, x_lat)))
    geopoint = random.sample(geopoint, len(geopoint))
    with open(filename, 'w') as fp:
        fp.write('\n'.join('{}, {}'.format(str(x[1]), str(x[0])) for x in geopoint))


if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        generate_random(sys.argv[1], sys.argv[2])
    else:
        print("Error - Command line args missing")
