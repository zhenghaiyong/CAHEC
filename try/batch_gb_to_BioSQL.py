#!/usr/bin/env python
"""Load multiple genbankfiles into BioSQL

You will need to adjust the database parameters and have a BioSQL database set
up. See:    http://biopython.org/wiki/BioSQL

adapted from bchapmanns github script
https://github.com/chapmanb/bcbb > gff > Scripts > gff > gff_to_biosql.py
https://gist.github.com/zachcp/1919989

and from single upload script:
https://gist.github.com/1919511

Usage:
    python batch_gb_to_biosql.py

"""
from __future__ import with_statement
import os, sys
from BioSQL import BioSeqDatabase
from Bio import SeqIO

driver = "MySQLdb"
user   = "root"
passwd = "pwd"
host   = "localhost"
dbname = "bioseqdb"
 
 
def main():
    gbdir=os.listdir(os.getcwd())
    inputfiles = [ file for file in gbdir if (".gbk" in file or ".GBK" in file or ".gb" in file or ".GB" in file or ".seq" in file) ]
    inputfiles.sort()
    print "Starting Batch Processing .....  "  
    for inputfile in inputfiles:
        genbanktoBioSql(inputfile)
    

def genbanktoBioSql(gbfile, length=10000):
    print "Parsing Genbank file sequence file...."
    with open(gbfile) as gb_handle:
        records = list(SeqIO.parse(gb_handle, "genbank"))
    print "%s: %d" % (gbfile, len(records))
    #zhy#print "Sorting by size and name......."
    #zhy#longrecords = [record for record in records if len(record) > length]
    #zhy#longrecords.sort(key=lambda x: x.name) #sort by name
    
    #the following is to avoid duplciate entry names.
    # Writes a temp file. is there a better way to do this?  
    ##zhy#for record in longrecords:
    #for record in records:
    #    record.id = "{0}".format(record.name)
    #    print record.id
    ##zhy#SeqIO.write(longrecords, "temp.gbk", "gb")
    #SeqIO.write(records, "temp.gbk", "gb")
    #with open("temp.gbk") as gb_handle:
    #     records = list(SeqIO.parse(gb_handle, "genbank"))
        
    print "Writing to BioSQL database..."
    server = BioSeqDatabase.open_database(driver=driver, user=user,
                                          passwd=passwd, host=host, db=dbname)
    try:
        ##zhy# gbfile[:-4] => gbfile[2:5]
        if gbfile[2:5] not in server.keys():
            server.new_database(gbfile[2:5])
        #else:
        #    server.remove_database(gbfile[2:5])
        #    server.adaptor.commit()
        #    server.new_database(gbfile[2:5])
        db = server[gbfile[2:5]]
        db.load(records)
        server.adaptor.commit()
    except:
        server.adaptor.rollback()
        raise
    
    ##zhy#if os.path.exists("temp.gbk"): os.remove("temp.gbk")    
    
if __name__ == "__main__":
    if  len(sys.argv) >1:
        print __doc__
        sys.exit()
    main()
