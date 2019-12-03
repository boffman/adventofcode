#!/usr/bin/perl -w
use strict;

sub look_and_say {
    my $input = shift;
    my @result;
    my $ix = 0;
    my $input_len = scalar(@$input);
    while ($ix < $input_len) {
        my $value = $input->[$ix];
        my $occurances = 1;
        my $ix2 = $ix+1;
        while ($ix2 < $input_len && $input->[$ix2] eq $value) {
            $occurances++;
            $ix2++;
        }
        push(@result, $occurances);
        push(@result, $value);
        $ix = $ix2;
    }
    return \@result;
}

while (my $line = <>) {
    chomp($line);
    my @input = split('', $line);

    my $ref = \@input;
    for (1 .. 40) {
        $ref = look_and_say($ref);
    }
    print "Length: " . scalar(@$ref);
}
