# darpa_population_modeling

This is a sample workflow to demonstrate how Pegasus can be used to
manage the population modeling tools in the MINT project.

The tools have been converted to command line tools.

A Singularity image, based on Ubuntu Xenial Xerus and with Python3 and
GIS tools and libraries, are used for the compute environment for the
jobs.

The workflow is currently set up to run on the ISI testbed, but can
be moved to more powerful execution environments if needed.

## Submitting

Check out this repository on `workflow.isi.edu` and run:

```
./workflow/submit.sh
```



