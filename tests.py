import os

from DNASeq import *

# Capture our current directory
#THIS_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_PATH = u'/Users/hachepunto/test/'

reads_s01 = Reads(sample="S01")

reads_s01.fastqs = [
    ('/mnt/f/rgarcia/MCAC/fastq/500/S01_L001_R1.fastq.gz','/mnt/f/rgarcia/MCAC/fastq/500/S01_L001_R2.fastq.gz'),
    ('/mnt/f/rgarcia/MCAC/fastq/500/S01_L002_R1.fastq.gz','/mnt/f/rgarcia/MCAC/fastq/500/S01_L002_R2.fastq.gz'),
]

# fq.rename_files()


reads_s01.create_bwa_lsf_jobs( queue     = 'high',
                               threads   = 16,
                               reference = ROOT_PATH + 'reference/UCSC.fa',
                               jobs_path = ROOT_PATH + 'jobs')



reads_s01.create_fastqc_lsf_jobs( queue     = 'high',
                                  threads   = 16,
                                  jobs_path = ROOT_PATH + 'jobs',
                                  fastqc_outdir = '/mnt/f/rgarcia/MCAC/fastq/500/')
