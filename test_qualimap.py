
from DNASeq import SequenceAlignmentMap, Sample

jaca_bam = SequenceAlignmentMap( Sample('JACA', '/home/rodrigo/tmp/jaca') )
jaca_bam.import_map('/home/rgarcia/tmp/file_jaca.bam')
jaca_bam.create_qualimap_lsf_job('max', 16)




#    Id       working_path              bam_file
samples = [
    ('JACA', '/home/rodrigo/tmp/jaca', '/home/rgarcia/tmp/file_jaca.bam'),
]

for sample in samples:
    bam = SequenceAlignmentMap( Sample(sample[0], sample[1]) ) )
    bam.import_map(sample[2])
    bam.create_qualimap_lsf_job('max', 16)
