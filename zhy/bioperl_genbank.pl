use Bio::SeqIO;
my $seqio_object = Bio::SeqIO->new(-file => "gbvrl1.seq", -format => "genbank");
my $seq_object = $seqio_object->next_seq;
print ref($seq_object);
print "\n";

for my $feat_object ($seq_object->get_SeqFeatures) {          
   print "primary tag: ", $feat_object->primary_tag, "\n";          
   for my $tag ($feat_object->get_all_tags) {             
      print "  tag: ", $tag, "\n";             
      for my $value ($feat_object->get_tag_values($tag)) {                
         print "    value: ", $value, "\n";             
      }          
   }       
}

for my $feat_object ($seq_object->get_SeqFeatures) {        
   push @ids, $feat_object->get_tag_values("db_xref") if ($feat_object->has_tag("db_xref"));     
}

print $seq_object->annotation();
print "\n";
