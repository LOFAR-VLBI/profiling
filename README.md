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


The JSON file contains three "main" entries:

* `worker`: resources used by Toil worker processes.
* `jobs`: cumulative resources used by the jobs.
* `job_types`: resource breakdown by individual jobs.


In `jobs` and `job_types` the field names have the following meanings:

|Field|Meaning|
|-----|-------|
|total_number|The number of jobs or jobs of this type that ran.|
|name|Name of the job that ran.|
|total_time|Total *wall clock time* consumed by the job(s).|
|median_time|Median *wall clock time* consumed by the job(s).|
|average_time|Maximum *wall clock time* consumed by the job(s).|
|min_time|Minimum *wall clock time* consumed by the job(s).|
|max_time|Maximum *wall clock time* consumed by the job(s).|
|total_clock|Total *core seconds* consumed by the job(s).|
|median_clock|Median *core seconds* consumed by the job(s).|
|average_clock|Maximum *core seconds* consumed by the job(s).|
|min_clock|Minimum *core seconds* consumed by the job(s).|
|max_clock|Maximum *core seconds* consumed by the job(s).|
|total_wait|Total CPU time reserved for but not consumed by the job(s).|
|median_wait|Median CPU time reserved for but not consumed by the job(s).|
|average_wait|Average CPU time reserved for but not consumed by the job(s).|
|min_wait|Minimum CPU time reserved for but not consumed by the job(s).|
|max_wait|Maximum CPU time reserved for but not consumed by the job(s).|
|total_memory|Total memory in kB consumed by the job(s).|
|median_memory|Median memory in kB consumed by the job(s).|
|average_memory|Maximum memory in kB consumed by the job(s).|
|min_memory|Minimum memory in kB consumed by the job(s).|
|max_memory|Maximum memory in kB consumed by the job(s).|
|total_disk|Total disk usage by the job(s).|
|median_disk|Median disk usage by the job(s).|
|average_disk|Maximum disk usage by the job(s).|
|min_disk|Minimum disk usage by the job(s).|
|max_disk|Maximum disk usage by the job(s).|
|total_core|Total cores requested by the job(s).|
|median_core|Median cores requested by the job(s).|
|average_core|Maximum cores requested by the job(s).|
|min_core|Minimum cores requested by the job(s).|
|max_core|Maximum cores requested by the job(s).|
|excess_cpu|Flag indicating if a job used more CPU than requested.|
