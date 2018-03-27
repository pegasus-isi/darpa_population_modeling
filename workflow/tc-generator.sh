#!/bin/bash

cat <<EOF
cont gis {
    type "singularity"
    image "file:///lizard/projects/MINT/Kimetrica/container/gis.simg"
    image_site "local"
}

tr county_population_raster {
    site condor_pool {
        type "STAGEABLE"
        container "gis"
        pfn "file://$PWD/county_population_raster.py"
    }
}

EOF

