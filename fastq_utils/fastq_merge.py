#!/usr/bin/env python
'''
Merges two (or more) paired end FASTQ files together for combined mapping. 
The files need to have the paired reads in the same order. They will be 
written out as:

@name1 pair1
seq
+
qual
@name1 pair2
seq
+
qual
...

The merged file is written to stdout.
'''

import os,sys,gzip

from fastq_utils import read_fastq

def fastq_merge(fnames,split_slashes=False):
    infiles = []
    
    first = True
    for fname in fnames:
        gen = read_fastq(fname, quiet = not first)
        infiles.append((fname,gen))
        first = False

    while True:
        lastname = None
        
        for fname,generator in infiles:
            try:
                name,seq,qual = generator.next()
            except:
                break
            
            if split_slashes and '/' in name:
                spl = name.split('/',1)
                name = spl[0]
                desc = ' /%s' % spl[1]
            else:
                desc = ''

            if not lastname:
                lastname = name
            elif name != lastname:
                sys.stderr.write('Files are not paired! (error in: %s)\nExpected: %s\nGot     : %s\n' % (fname,lastname,name))
                sys.exit(1)
        
            sys.stdout.write('%s%s\n%s\n+\n%s\n' % (name,desc,seq,qual))

def usage():
    print __doc__
    print """Usage: %s {-slash} file1.fastq{.gz} file2.fastq{.gz} ... 

-slash    Split the read name at a '/' (Illumina paired format)
    
    """ % os.path.basename(sys.argv[0])
    sys.exit(1)

if __name__ == '__main__':
    fnames = []
    split_slashes = False
    for arg in sys.argv[1:]:
        if arg == '-slash':
            split_slashes = True
        elif os.path.exists(arg):
            fnames.append(arg)

    if not fnames:
        usage()
        
    fastq_merge(fnames,split_slashes)
