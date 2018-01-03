from ruffus import *
import os
import glob
import argparse
import re

####################################################################
#Read in config file
config_dict ={}

with open('config.txt', 'r') as config_file:

	for line in config_file:

		line = line.strip().split(':',1)

		config_dict[line[0]] = line[1]



####################################################################
#parse arguments

parser = argparse.ArgumentParser(description='A pipeline')
parser.add_argument('--input_dir', nargs='?')
parser.add_argument('--output_dir', nargs='?')
parser.add_argument('--config_file', nargs='?')
parser.add_argument('--vcf_header_file', nargs='?')
args= parser.parse_args()


####################################################################
#get initial files

initial_files = glob.glob('{input_dir}*.vcf.gz'.format(input_dir=args.input_dir))

print initial_files


####################################################################
#Add headers
@transform(initial_files, suffix('.vcf.gz'), '.headers.vcf')
def add_headers(infile,outfile):
	"""
	Add headers to the vcf file. VEP breaks if we don't do this.

	"""

	command = 'bcftools annotate --header-lines {header_file} {inputfile} >  {outfile}'.format(inputfile=infile, outfile=outfile, header_file=args.vcf_header_file)

	os.system(command)

	#print command

####################################################################
#Remove annotations
@transform(add_headers, suffix('.headers.vcf'), '.headers.remove.vcf')
def remove_annotations(infile,outfile):
	"""
	Remove the INFO/END, INFO/START and INFO/SVLEN annotations.

	"""
	command = 'bcftools annotate -x INFO/END,INFO/START,INFO/SVLEN {infile} >  {outfile}'.format(infile=infile, outfile=outfile)

	os.system(command)

####################################################################
#Annotate with VEP
@transform(remove_annotations, suffix('.headers.remove.vcf'), '.headers.remove.vep.vcf')
def annotate_with_vep(infile,outfile):
	"""
	Annotate with VEP.

	"""

	vep_location = config_dict['vep']
	reference_genome = config_dict['ref']

	command = ('{vep_location} -i {inputfile} -o {outputfile} --cache --fork 4 --refseq --vcf --flag_pick --exclude_predicted --everything --dont_skip --total_length  --offline --fasta {reference_genome}'
			.format(vep_location= vep_location,
			inputfile=infile,
			outputfile=outfile,
			reference_genome=reference_genome))


	os.system(command)

####################################################################
#Compress and index the files (bgzip and tabix)
@transform(annotate_with_vep, suffix('.headers.remove.vep.vcf'), '.headers.remove.vep.vcf.gz')
def compress_and_index(infile,outfile):
	"""
	Compress and index the VEP annotated files.

	"""

	command = 'bgzip {infile}'.format(infile=infile)

	os.system(command)

	command = command = 'tabix {infile}'.format(infile=infile+'.gz')

	os.system(command)


####################################################################
#Clean up unneeded files
@follows(compress_and_index)
def clean_up():
	"""
	Delete the intermediate files

	"""

	output_dir = args.input_dir.split('/')[-2]+'_vep'

	command = 'rm {input_dir}*header*.vcf'.format(input_dir =args.input_dir)

	os.system(command)

	command = 'mkdir {output_dir}'.format(output_dir=output_dir)

	os.system(command)

	command = 'mv {input_dir}*vep* {output_dir}'.format(input_dir=args.input_dir, output_dir=output_dir)

	os.system(command)

pipeline_run()