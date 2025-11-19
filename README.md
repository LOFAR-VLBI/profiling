This repository holds profiling data and analysis scripts to characterise resource usage of the LOFAR2.0 pipelines.


# Toil statistics

Main Toil stats reference: https://toil.readthedocs.io/en/master/running/utils.html

When running pipelines with Toil, statistics can be recorded by using `toil-cwl-runner --stats <rest of the options/inputs>`. This makes it leave the jobstore behind, after which statistics of the idividual steps can be extracted via

```bash
toil stats --raw /path/to/jobstore > stats.json
```

A human-readable version can be produced via

```bash
toil stats --pretty /path/to/jobstore > stats.txt
```
