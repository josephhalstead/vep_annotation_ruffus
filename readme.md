# Readme

## Introduction

A quick Ruffus script for annotating vcfs with VEP.

There are a few preprocessing steps required before annotation so decided to do as a pipeline.

Really just so I can learn a abit of Ruffus syntax.

## Running

```bash


python vep_annotate_pipeline.py --input_dir vcfs/ --config_file config.txt --vcf_header_file header_file.txt

```

### Options

* --input_dir = The folders with the vcfs in (.gz expected)
* --config_file = The file with the configuration information in e.g. location of folders, reference genom etc
* --vcf_header_file = The file with the vcf headers to add
