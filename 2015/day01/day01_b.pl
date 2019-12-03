#!/usr/bin/perl -w
use strict;
my $line = <>;
my $floor=0;
my $position=0;
while ($line =~ /(.)/g) {
    $position++;
    my $c = $1;
    if ($c eq '(') {
        $floor++;
    }
    elsif ($c eq ')') {
        $floor--;
    }
    if ($floor == -1) {
        print "Floor $floor at position $position\n";
    }
}
