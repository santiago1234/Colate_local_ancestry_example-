# Reproducible example to run Colate local ancestry mode

A reproducible example showing how to run Colate with the local ancestry mode.


Clonning the repo:


```bash
git clone https://github.com/santiago1234/Colate_local_ancestry_example-.git
# to get the Relate genealogies
git lfs pull
git restore --staged   data/example_chr22.anc  data/example_chr22.mut
```


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

```bash
/data/users/smedina/software/Colate-devel/binaries/v0.1.4_x86_64_static/bin/Colate --mode local_ancestry \
  -i data/example \
  -o output \
  --chr chr.txt \
  --bins 2,7,0.2 \
  --num_bootstraps 100 \
  --poplabels data/assignment.txt
```
