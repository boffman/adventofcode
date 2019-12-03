#!/usr/bin/perl -w
use strict;
my $line = <>;
my $floor=0;
while ($line =~ /(.)/g) {
    my $c = $1;
    if ($c eq '(') {
        $floor++;
    }
    elsif ($c eq ')') {
        $floor--;
    }
    print "$floor\n";
}
