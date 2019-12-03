#!/usr/bin/perl -w
use strict;

my %map;
my $xpos=0;
my $ypos=0;
my $num_moves=0;

my $position = "$xpos,$ypos";
$map{$position}++;

while (my $line = <>) {
    chomp($line);
    while ($line =~ /(.)/g) {
        my $move = $1;
        if ($move eq '<') {
            $xpos--;
        }
        elsif ($move eq '>') {
            $xpos++;
        }
        elsif ($move eq 'v') {
            $ypos--;
        }
        elsif ($move eq '^') {
            $ypos++;
        }
        $position = "$xpos,$ypos";
        $map{$position}++;
        $num_moves++;
    }
}
print "Number of moves: $num_moves, number of houses receving presents: " . scalar(keys(%map)) . "\n";


