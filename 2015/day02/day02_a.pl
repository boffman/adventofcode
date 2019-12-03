#!/usr/bin/perl -w
use strict;

sub min {
    my $min=undef;
    for (@_) {
        $min = $_ if (!defined($min) || $_ < $min);
    }
    return $min;
}

sub smallest_area {
    my ($l,$w,$h) = @_;
    my $a1 = $l*$w;
    my $a2 = $l*$h;
    my $a3 = $w*$h;
    return min($a1,$a2,$a3);
}

sub surface_area {
    my ($l,$w,$h) = @_;
    return 2*$l*$w + 2*$w*$h + 2*$h*$l;
}


my $paper_sum=0;
while(my $line=<>) {
    chomp($line);
    my ($l,$w,$h) = split(/x/,$line);
    my $smallest_area = smallest_area($l,$w,$h);
    my $surface_area = surface_area($l,$w,$h);
    my $paper_needed = $smallest_area + $surface_area;
    print "$l x $w x $h surface area = $surface_area, smallest area=$smallest_area, total paper needed=$paper_needed\n";
    $paper_sum += $paper_needed;
}
print "Total paper needed: $paper_sum\n";

