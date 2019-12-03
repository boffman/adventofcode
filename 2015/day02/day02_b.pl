#!/usr/bin/perl -w
use strict;

sub min {
    my $min=undef;
    for (@_) {
        $min = $_ if (!defined($min) || $_ < $min);
    }
    return $min;
}

sub ribbon_bow {
    my ($l,$w,$h) = @_;
    return $l*$w*$h;
}

sub ribbon_wrap {
    my @sides = sort(@_);
    my $shortest_distance_sides = 2*$sides[0] + 2*$sides[1];
    my $smallest_face = min(2*$sides[0]+2*$sides[1], 2*$sides[0]+2*$sides[2], 2*$sides[1]+2*$sides[2]);
    return min($shortest_distance_sides, $smallest_face);
}


my $ribbon_sum=0;
while(my $line=<>) {
    chomp($line);
    my ($l,$w,$h) = split(/x/,$line);
    my $ribbon_bow = ribbon_bow($l,$w,$h);
    my $ribbon_wrap = ribbon_wrap($l,$w,$h);
    my $ribbon_needed = $ribbon_bow + $ribbon_wrap;
    print "$l x $w x $h ribbon wrap = $ribbon_wrap, ribbon bow=$ribbon_bow, total ribbon needed=$ribbon_needed\n";
    $ribbon_sum += $ribbon_needed;
}
print "Total ribbon needed: $ribbon_sum\n";

