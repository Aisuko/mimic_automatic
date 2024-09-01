

# How to load data into your PgSQL?

```bash
sudo apt install postgresql-client -y
```

```bash
make up
```

### Create table
```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d mimiciv -f mimic-iv/buildmimic/postgres/create.sql
```

### Load data
```bash
psql -h 127.0.0.1 -p 5432 -U postgres -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=/home/ec2-user/raw_data/mimiciv/2.0 -f mimic-iv/buildmimic/postgres/load_gz.sql


psql -h 127.0.0.1 -p 5432 -U postgres -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=/home/ec2-user/raw_data/mimiciv/2.0 -f mimic-iv/buildmimic/postgres/constraint.sql

psql -h 127.0.0.1 -p 5432 -U postgres -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=/home/ec2-user/raw_data/mimiciv/2.0 -f mimic-iv/buildmimic/postgres/index.sql
```




## Navigating this repository

This repository contains code for five databases on PhysioNet:

- [MIMIC-III](https://physionet.org/content/mimiciii/) - critical care data for patients admitted to ICUs at the BIDMC between 2001 - 2012
- [MIMIC-IV](https://physionet.org/content/mimiciv/) - hospital and critical care data for patients admitted to the ED or ICU between 2008 - 2019
- [MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/) - emergency department data for individuals attending the ED between 2011 - 2019
- MIMIC-IV Waveforms (TBD) - this dataset has yet to be published.
- [MIMIC-CXR](https://physionet.org/content/mimic-cxr/) - chest x-ray imaging and deidentified free-text radiology reports for patients admitted to the ED from 2012 - 2016

The repository contains one top-level folder containing community developed code for each datasets:

- [mimic-iii](/mimic-iii) - build scripts for MIMIC-III, derived concepts which are available on the `physionet-data.mimiciii_derived` dataset on BigQuery, and tutorials.
- [mimic-iv](/mimic-iv) - build scripts for MIMIC-IV, derived concepts which are available on the `physionet-data.mimic_derived` dataset on BigQuery, and tutorials.
- [mimic-iv-cxr](/mimic-iv-cxr) - code for loading and analyzing both dicom (mimic-iv-cxr/dcm) and text (mimic-iv-cxr/txt) data. In order to clearly indicate that MIMIC-CXR can be linked with MIMIC-IV, we have named this folder mimic-iv-cxr, and any references to MIMIC-CXR / MIMIC-IV-CXR are interchangeable.
- [mimic-iv-ed](/mimic-iv-ed) - build scripts for MIMIC-IV-ED.
- mimic-iv-waveforms - TBD

Each subfolder has a README with further detail regarding its content.


## Other useful tools

* [Bloatectomy](https://github.com/MIT-LCP/bloatectomy) ([paper](https://github.com/MIT-LCP/bloatectomy/blob/master/paper/paper.md)) - A python based package for removing duplicate text in clinical notes
* [Medication categories](https://github.com/mghassem/medicationCategories) - Python script for extracting medications from free-text notes
* [MIMIC Extract](https://github.com/MLforHealth/MIMIC_Extract) ([paper](https://doi.org/10.1145/3368555.3384469)) - A python based package for transforming MIMIC-III data into a machine learning friendly format
* [FIDDLE](https://github.com/MLD3/FIDDLE) ([paper](https://doi.org/10.1093/jamia/ocaa139)) - A python based package for a FlexIble Data-Driven pipeLinE (FIDDLE), transforming structured EHR data into a machine learning friendly format

* [tmux](https://tmuxcheatsheet.com)

## Acknowledgement

If you use code or concepts available in this repository, we would be grateful if you would:

- cite the dataset(s) you use as described in the PhysioNet project page: [MIMIC-III](https://physionet.org/content/mimiciii/), [MIMIC-IV](https://physionet.org/content/mimiciv/), [MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/) , and/or [MIMIC-CXR](https://physionet.org/content/mimic-cxr/)
- include a DOI for the code rather than a direct link to the GitHub repo, i.e. https://doi.org/10.5281/zenodo.821872
- cite the MIMIC code repository paper: [The MIMIC Code Repository: enabling reproducibility in critical care research](https://doi.org/10.1093/jamia/ocx084)

```bibtex
@article{johnson2018mimic,
  title={The MIMIC Code Repository: enabling reproducibility in critical care research},
  author={Johnson, Alistair E W and Stone, David J and Celi, Leo A and Pollard, Tom J},
  journal={Journal of the American Medical Informatics Association},
  volume={25},
  number={1},
  pages={32--39},
  year={2018},
  publisher={Oxford University Press}
}
```


### License

By committing your code to the [MIMIC Code Repository](https://github.com/mit-lcp/mimic-code) you agree to release the code under the [MIT License attached to the repository](https://github.com/mit-lcp/mimic-code/blob/main/LICENSE).

