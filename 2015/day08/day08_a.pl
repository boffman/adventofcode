#!/usr/bin/perl -w
use strict;

my $num_string = 0;
my $num_memory = 0;
while (my $line = <>) {
    chomp($line);
    $num_string += length($line);
    my $unescaped = eval $line;
    $num_memory += length($unescaped);
}

print "num_string: $num_string\n";
print "num_memory: $num_memory\n";
my $answer = $num_string - $num_memory;
print "Answer: $answer\n";

