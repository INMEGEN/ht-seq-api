
from sh import which


class Study:

    def __init__(self):
        self.paths = dict()

    def discover_paths(self):
        self.paths['bwa'] = which('bwa')




class Sample:

    def __init__(self, fastqs=None, sams=None):
        self.fastqs = fastqs



class Fastq:

    def __init__(self):
        pass





class SequenceAlignmentMap:

    def __init__(self):
        pass


    
