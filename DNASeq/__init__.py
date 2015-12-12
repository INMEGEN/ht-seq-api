from sh import which, mkdir, ln
from jinja2 import Environment, PackageLoader




class Sample:

    def __init__(self, id, path):
        self.id   = id
        self.path = path

    def __unicode__(self):
        return "%s %s" % (self.sample, self.path)


        
class Reads:
    paths  = {}
   
    def __init__(self, sample):
        self.sample = sample

        self.jobs_path = "%/jobs" % sample.path
        self.env = Environment(loader=PackageLoader('DNASeq'))
        self.discover_paths()
        
    def discover_paths(self):
        self.paths['bwa'] = which('bwa')
        self.paths['fastqc'] = which('fastqc')        


    def create_fastqc_lsf_jobs(self, queue, threads):
        template = self.env.get_template('fastqc.lsf')

        lane = 0
        for pair in self.fastqs:
            job_id = "qualimap_%s" % self.sample
            with open("%s/%s.lsf_job" % (self.jobs_path, job_id), 'w') as job_file:
                job_file.write(template.render( job_id    = job_id,
                                                fastqc_path  = self.paths['fastqc'],
                                                pair      = pair,
                                                queue     = queue,
                                                threads   = threads,
                                                fastqc_outdir = fastqc_outdir ))
                               


    def create_bwa_lsf_jobs(self, queue, threads, reference, jobs_path):
        template = self.env.get_template('bwa.lsf')

        lane = 0
        for pair in self.fastqs:
            job_id = "%s_L%s" % (self.sample, lane)
            lane  += 1
            with open("%s/bwa_%s.lsf_job" % (jobs_path, job_id), 'w') as job_file:
                job_file.write(template.render( job_id    = job_id,
                                                bwa_path  = self.paths['bwa'],
                                                pair      = pair,
                                                queue     = queue,
                                                threads   = threads,
                                                reference = reference,
                                                jobs_path = jobs_path ))
                               

                
    def rename_files(self):
        pass
        

class SequenceAlignmentMap:
    paths  = {}
    status = "bam"
    
    def __init__(self, sample):
        self.sample   = sample
        self.jobs_dir = "%s/jobs" % sample.path
        mkdir('-p', self.jobs_dir)
        self.qc_dir   = "%s/qc" % sample.path
        self.sam_path = "%s/maps/%s.%s" % (sample.path, sample.id, self.status)
        
        self.env       = Environment(loader=PackageLoader('DNASeq'))
        self.discover_paths()


    def discover_paths(self):
        self.paths['freebayes'] = which('freebayes')
        self.paths['samtools']  = which('samtools')
        self.paths['java']      = which('java')
        self.paths['qualimap']  = which('qualimap')

    def import_map(self, path, mode='symlink'):
        """
        will populate the maps dir with a SAM or BAM file.
        TODO: other modes might be: copy, move
        """
        mkdir('-p', "%s/maps" % self.sample.path)
        if mode == 'symlink':
            ln('-s', path, self.sam_path)

    def sniff_metadata():
        pass

        
    def create_qualimap_lsf_job(self, queue, threads, outformat='HTML'):
        template = self.env.get_template('qualimap.lsf')
        job_id = "qualimap_%s" % (self.sample.id)
        mkdir('-p', self.qc_dir)
        
        with open("%s/%s.lsf_job" % (self.jobs_dir, job_id), 'w') as job_file:
            job_file.write(template.render( job_id    = job_id,
                                            queue     = queue,
                                            threads   = threads,
                                            qualimap  = self.paths['qualimap'],
                                            sam       = self.sam_path,
                                            outformat = outformat,
                                            outdir    = "%s/qualimap" % self.qc_dir ))



        
class VariantCalls:

    def discover_paths(self):
        self.paths['vep.pl'] = which('vep.pl')





class PredictedEffects:
    pass
    #def discover_paths(self):
        # self.paths['mongo_etl'] = which('vep.pl')






class Variants:
    paths  = {}
   
    def __init__(self, sample, vcf_path=None, reference=None, genome=None):
        self.sample   = sample
        self.vcf_path = vcf_path
        self.reference = reference
        self.genome    = genome        
        self.env      = Environment(loader=PackageLoader('DNASeq'))
        self.discover_paths()

    def discover_paths(self):
        self.paths['java']   = which('java')
        self.paths['snpeff'] = None
        self.paths['vep']    = which('variant_effect_predictor.pl')        

    def sniff_reference(self):
        '''
        reads vcf header to determine path to reference and it's genome
        '''
        pass
    
    def create_snpeff_lsf_job(self, queue, threads, jobs_path, outdir):
        template = self.env.get_template('snpeff.lsf')
        job_id   = "%s" % (self.sample)
        with open("%s/snpeff_%s.lsf_job" % (jobs_path, job_id), 'w') as job_file:
            job_file.write(template.render( job_id          = job_id,
                                            java_path       = self.paths['java'],
                                            snpeff_jar_path = self.paths['snpeff'],
                                            vcf_path        = self.vcf_path,
                                            queue           = queue,
                                            threads         = threads,
                                            genome          = self.genome,
                                            outdir          = outdir))



    def create_snpeff_local_job(self, threads, jobs_path, outdir):
        template = self.env.get_template('snpeff.local')
        job_id   = "%s" % (self.sample)
        with open("%s/snpeff_%s.sh" % (jobs_path, job_id), 'w') as job_file:
            job_file.write(template.render( job_id          = job_id,
                                            java_path       = self.paths['java'],
                                            snpeff_jar_path = self.paths['snpeff'],
                                            vcf_path        = self.vcf_path,
                                            threads         = threads,
                                            genome          = self.genome,
                                            outdir          = outdir))
            


    # def create_vep_lsf_jobs(self, queue, threads, reference, jobs_path):
    #     template = self.env.get_template('vep.lsf')
                               


        
