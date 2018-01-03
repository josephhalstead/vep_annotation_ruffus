#bash script to apply the pipeline to multiple folders

source myvenv/bin/activate

folders=/home/cuser/Documents/Project/DatabaseData/old_runs/output_dirs/*

for f in $folders; do

	directory=$f/vcfs*/

	python vep_annotate_pipeline.py --input_dir $directory --config_file config.txt --vcf_header_file header_file.txt

done