#!/usr/bin/env python

import glob
import math
import os
import re
import sys

from Pegasus.DAX3 import *

top_dir = os.getcwd()

dax = ADAG("kimetrica")

# common library
geospatial = File('geospatial.py')
geospatial.addPFN(PFN('file://' + top_dir + '/geospatial.py', 'local'))
dax.addFile(geospatial)

# config file
config = File('county_cohort_pop_config.ini')
config.addPFN(PFN('file://' + top_dir + '/config/county_cohort_pop_config.ini', 'local'))
dax.addFile(config)

# shapefile (set of files)
shapefiles = []
basename = "SouthSudan_CountyPopulation"
for fname in glob.glob('data/' + basename + '.*'):
    # do not include data/ in the lfn
    fname = re.sub('data/', '', fname)
    f = File(fname)
    f.addPFN(PFN('file://' + top_dir + '/data/' + fname, 'local'))
    dax.addFile(f)
    shapefiles.append(f)

# distribution tif
dist_tif = File('ss_pop_spatial_dist.tif')
dist_tif.addPFN(PFN('file://' + top_dir + '/data/ss_pop_spatial_dist.tif', 'local'))
dax.addFile(dist_tif)

# legend
legend = File('legend.png')
legend.addPFN(PFN('file://' + top_dir + '/graphics/legend.png', 'local'))
dax.addFile(legend)


# animate - this is the final job, but will be built up in the loops below
animate = Job("animate")
out_anim = File('animation.gif')
animate.uses(out_anim, link=Link.OUTPUT, transfer=True)
dax.addJob(animate)

# add one job per year
for year in range(2017, 2030 + 1):

    # create a job to process the shape file
    j1 = Job("county_population_raster")

    # we need the geospatial lib
    j1.uses(geospatial, link=Link.INPUT)
    
    # config file
    j1.uses(config, link=Link.INPUT)
    j1.addArguments('--config', config)

    # shape file
    for f in shapefiles:
        j1.uses(f, link=Link.INPUT)
    j1.addArguments('--shapefile', basename + '.shp')

    # year
    j1.addArguments('--year', str(year))

    # outputs
    tif = File('county_level_pop_' + str(year) + '.tif')
    j1.uses(tif, link=Link.OUTPUT, transfer=True)
    j1.addArguments('--outfile', tif)

    dax.addJob(j1)

    # create a full res distribution of the population
    j2 = Job('full_res_pop_raster')
    j2.uses(tif, link=Link.INPUT)
    j2.uses(dist_tif, link=Link.INPUT)
    pop_dist_tif = File('pop_dist_' + str(year) + '.tif')
    j2.uses(pop_dist_tif, link=Link.OUTPUT, transfer=True)
    j2.addArguments('--population-file', tif, 
                    '--dist-file', dist_tif, 
                    '--out-file', pop_dist_tif) 
    dax.addJob(j2)
    dax.depends(parent=j1, child=j2)

    # second job to convert the raster tif to an annotated png
    j3 = Job("raster_to_png")
    j3.uses(pop_dist_tif, link=Link.INPUT)
    j3.uses(legend, link=Link.INPUT)
    png = File('pop_dist_' + str(year) + '.png')
    j3.uses(png, link=Link.OUTPUT, transfer=True)
    j3.addArguments(pop_dist_tif, png, str(year))
    dax.addJob(j3)
    dax.depends(parent=j2, child=j3)

    # add to animate job
    animate.uses(png, link=Link.INPUT)
    dax.depends(parent=j3, child=animate)

# Write the DAX to stdout
dax.writeXML(sys.stdout)

