#!/bin/bash

cat <<EOF

# image comes from Singularity Hub
cont gis {
    type "singularity"
    image "shub://pegasus-isi/darpa_population_modeling"
}

tr county_population_raster {
    site condor_pool {
        type "STAGEABLE"
        container "gis"
        pfn "file://$PWD/county_population_raster.py"
    }
}

EOF

