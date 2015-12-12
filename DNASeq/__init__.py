from sh import which
from jinja2 import Environment, PackageLoader




class Sample:

    def __init__(self, sample):
        self.sample = sample

    def __unicode__(self):
        return "%s" % self.sample


        
class Reads:
    paths  = {}
   
    def __init__(self, sample):
        self.sample = sample
        self.env = Environment(loader=PackageLoader('DNASeq'))
        self.discover_paths()
        
    def discover_paths(self):
        self.paths['bwa'] = which('bwa')
        self.paths['fastqc'] = which('fastqc')        


    def create_fastqc_lsf_jobs(self, queue, threads, jobs_path, fastqc_outdir):
        template = self.env.get_template('fastqc.lsf')

        lane = 0
        for pair in self.fastqs:
            job_id = "%s_L%s" % (self.sample, lane)
            lane  += 1
            with open("%s/fastqc_%s.lsf_job" % (jobs_path, job_id), 'w') as job_file:
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
    
    def __init__(self):
        self.status = []


    def sniff_metadata():
        pass

    def discover_paths(self):
        self.paths['freebayes'] = which('freebayes')
        self.paths['samtools'] = which('samtools')
        self.paths['java'] = which('java')
        self.paths['qualimap'] = which('qualimap')        


    def create_qualimap_lsf_job(self, queue, threads, reference, jobs_path):
        template = self.env.get_template('qualimap.lsf')
        job_id = "%s" % (self.sample)
        
        with open("%s/bwa_%s.lsf_job" % (jobs_path, job_id), 'w') as job_file:
            job_file.write(template.render( job_id    = job_id,
                                            bwa_path  = self.paths['bwa'],
                                            pair      = pair,
                                            queue     = queue,
                                            threads   = threads,
                                            reference = reference,
                                            jobs_path = jobs_path ))


        
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
                               


        
