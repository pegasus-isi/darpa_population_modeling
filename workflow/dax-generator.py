#!/usr/bin/env python

import glob
import math
import os
import re
import sys

from Pegasus.DAX3 import *

top_dir = os.getcwd()


def add_shapefile_files(basename):
    '''
    Adds a set of shapefile files to a job
    '''

dax = ADAG("kimetrica")

# common library
geospatial = File('geospatial.py')
geospatial.addPFN(PFN('file://' + top_dir + '/geospatial.py', 'local'))
dax.addFile(geospatial)

# add one job per shapefile
for shapefile in glob.glob('data/*.shp'):

    # just want the basename
    shapefile = re.sub('data/|\.shp$', '', shapefile)

    # create a job to process the shape file
    job = Job("county_population_raster")

    # we need the geospatial lib
    job.uses(geospatial, link=Link.INPUT)
    
    # config file
    config = File('county_cohort_pop_config.ini')
    config.addPFN(PFN('file://' + top_dir + '/config/county_cohort_pop_config.ini', 'local'))
    dax.addFile(config)
    job.uses(config, link=Link.INPUT)
    job.addArguments('--config', config)

    # shape file
    for fname in glob.glob('data/' + shapefile + '.*'):
        # do not include data/ in the lfn
        fname = re.sub('data/', '', fname)
        f = File(fname)
        f.addPFN(PFN('file://' + top_dir + '/data/' + fname, 'local'))
        dax.addFile(f)
        job.uses(f, link=Link.INPUT)
        if re.search('\.shp$', fname):
            job.addArguments('--shapefile', f)

    # outputs
    out = File('county_level_pop_out.tif')
    job.uses(out, link=Link.OUTPUT, transfer=True)
    job.addArguments('--outfile', out)

    dax.addJob(job)

# Write the DAX to stdout
dax.writeXML(sys.stdout)


