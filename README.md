# Reproducible example to run Colate local ancestry mode

A reproducible example showing how to run Colate with the local ancestry mode.

## Data

- [See data folder](data/README.md)


## Local ancestry

[Gnomix](https://github.com/AI-sandbox/gnomix) was used to infer local ancestry
with K = 3 (European, African, and Native American ancestries).

Convert [Gnomix output](data/example.msp) to Colate local ancestry input [assignment.txt](data/assignment.txt)


```bash
python gnomix_to_colate.py
```

## Run Colate
