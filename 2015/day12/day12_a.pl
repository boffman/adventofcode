#!/usr/bin/perl -w
use strict;

my $sum = 0;
while (my $line = <>) {
    chomp($line);
    while ($line =~ /(-*\d+)/g) {
        my $num = int($1);
        $sum += $num;
    }
}
print "Sum: $sum\n";

