#!/usr/bin/perl -w
use strict;

sub has_atleast_three_vowels {
    my $str = shift;
    my $num_vowels = 0;
    while ($str =~ /(.)/g) {
        $num_vowels++ if ($1 =~ /[aeiou]/);
    }
    return $num_vowels >= 3;
}

sub has_twice_in_a_row {
    my $str = shift;
    return $str =~ /(.)\g1/;
}

sub contains_forbidden_combos {
    my $str = shift;
    return $str =~ /ab|cd|pq|xy/;
}

sub is_nice {
    my $str = shift;
    return has_atleast_three_vowels($str) && 
        has_twice_in_a_row($str) && 
        !contains_forbidden_combos($str);
}


my $num_nice = 0;
while (my $line = <>) {
    chomp($line);
    $num_nice++ if (is_nice($line));
}
print "Number of nice strings: $num_nice\n";

