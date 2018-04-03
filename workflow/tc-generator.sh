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

tr full_res_pop_raster {
    site condor_pool {
        type "STAGEABLE"
        container "gis"
        pfn "file://$PWD/full_res_pop_raster.py"
    }
}

tr raster_to_png {
    site condor_pool {
        type "STAGEABLE"
        container "gis"
        pfn "file://$PWD/raster_to_png.sh"
    }
}

tr animate {
    site condor_pool {
        type "STAGEABLE"
        container "gis"
        pfn "file://$PWD/animate.sh"
    }
}

EOF

