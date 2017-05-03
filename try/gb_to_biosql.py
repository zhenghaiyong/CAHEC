#!/usr/bin/env python
"""Load a genbankfile into BioSQL

You will need to adjust the database parameters and have a BioSQL database set
up. See:

http://biopython.org/wiki/BioSQL

adapted from bchapmanns github script
https://github.com/chapmanb/bcbb > gff > Scripts > gff > gff_to_biosql.py
https://gist.github.com/zachcp/1919511

Depending on the size of the sequences being loaded, you may also get errors on
loading very large chromosome sequences. Updating these options can help:

    set global max_allowed_packet=1000000000;
    set global net_buffer_length=1000000;

Usage:
    gb_to_biosql.py <genbank file>
"""

from __future__ import with_statement
import sys
from BioSQL import BioSeqDatabase
from Bio import SeqIO


#zhy#biodb_name = str(sys.argv[1])[:4]
biodb_name = str(sys.argv[1])[2:5]

def main(gbfile, length=10000):
    driver = "MySQLdb"
    user   = "root"
    passwd = "iplouc"
    host   = "localhost"
    dbname = "bioseqdb"
    
    print "Parsing Genbank file sequence file...."
    with open(gbfile) as gb_handle:
        records = list(SeqIO.parse(gb_handle, "genbank"))
    print "%s: %d" % (gbfile, len(records))
    #zhy#print "Sorting by size and name......."
    #zhy#longrecords = [record for record in records if len(record) > length]
    #zhy#longrecords.sort(key=lambda x: x.name) #sort by name
    
    print "Writing to BioSQL database..."
    server = BioSeqDatabase.open_database(driver=driver, user=user,
            passwd=passwd, host=host, db=dbname)
    
    try:
        if biodb_name not in server.keys():
            server.new_database(biodb_name)
        else:
            server.remove_database(biodb_name)
            server.adaptor.commit()
            server.new_databse(biodb_name)
        db = server[biodb_name]
        #zhy#db.load(longrecords)
        db.load(records)
        server.adaptor.commit()
    except:
        server.adaptor.rollback()
        raise

if __name__ == "__main__":
    if  len(sys.argv) !=2:
        print __doc__
        sys.exit()
    main(sys.argv[1])
