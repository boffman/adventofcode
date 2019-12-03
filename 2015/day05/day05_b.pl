#!/usr/bin/perl -w
use strict;

sub has_a_non_overlapping_pair {
    my $str = shift;
    return $str =~ /(..).*\g1/;
}

sub has_repeating_letter_with_one_between {
    my $str = shift;
    return $str =~ /(.).\g1/;
}

sub is_nice {
    my $str = shift;
    return has_a_non_overlapping_pair($str) &&
        has_repeating_letter_with_one_between($str);
}


my $num_nice = 0;
while (my $line = <>) {
    chomp($line);
    $num_nice++ if (is_nice($line));
}
print "Number of nice strings: $num_nice\n";

