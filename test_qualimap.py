

from DNASeq import SequenceAlignmentMap, Sample

jaca = Sample('JACA', '/home/rodrigo/tmp/jaca')

jaca_bam = SequenceAlignmentMap( jaca )

jaca_bam.link_import_sam('/home/rgarcia/tmp/file_jaca.bam')
jaca_bam.create_qualimap_lsf_job('max', 16)
