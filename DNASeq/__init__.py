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


    def create_bwa_lsf_jobs(self, queue, threads, reference, jobs_path):
        template = self.env.get_template('bwa.lsf')

        lane = 0
        for pair in self.fastqs:
            job_id = "%s_L%s" % (self.sample, lane)
            lane  += 1
            with open("%s.lsf_job" % job_id, 'w') as job_file:
                job_file.write(template.render( job_id    = job_id,
                                                bwa_path  = self.paths['bwa'],
                                                pair      = pair,
                                                queue     = queue,
                                                threads   = threads,
                                                reference = reference,
                                                jobs_path = jobs_path ))
                               

    def rename_files(self):
        pass
        

class SequenceAlignmentMaps:

    def __init__(self):
        self.status = []


    def sniff_metadata():
        pass

    def discover_paths(self):
        self.paths['freebayes'] = which('freebayes')
        self.paths['samtools'] = which('samtools')
        self.paths['java'] = which('java')
        self.paths['qualimap'] = which('qualimap')        

    
class VariantCalls:

    def discover_paths(self):
        self.paths['vep.pl'] = which('vep.pl')





class PredictedEffects:
    pass
    #def discover_paths(self):
        # self.paths['mongo_etl'] = which('vep.pl')


