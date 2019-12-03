#!/usr/bin/perl -w
use strict;

my $num_string = 0;
my $num_escaped = 0;
while (my $line = <>) {
    chomp($line);
    $num_string += length($line);
    my $escaped = '"' . quotemeta($line) . '"';
    $num_escaped += length($escaped);
}

print "num_escaped: $num_escaped\n";
print "num_string: $num_string\n";
my $answer = $num_escaped - $num_string;
print "Answer: $answer\n";

