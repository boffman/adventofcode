#!/usr/bin/perl -w
use strict;

my %map;
my $xpos=0;
my $ypos=0;
my $xpos_santa=0;
my $ypos_santa=0;
my $xpos_robo=0;
my $ypos_robo=0;
my $num_moves=0;
my $robo_turn=0;

my $position = "$xpos_santa,$ypos_santa";
$map{$position}++;
$position = "$xpos_robo,$ypos_robo";
$map{$position}++;

while (my $line = <>) {
    chomp($line);
    while ($line =~ /(.)/g) {
        my $move = $1;
        if ($robo_turn) {
            $xpos = $xpos_santa;
            $ypos = $ypos_santa;
        }
        else {
            $xpos = $xpos_robo;
            $ypos = $ypos_robo;
        }

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

        if ($robo_turn) {
            $xpos_santa = $xpos;
            $ypos_santa = $ypos;
        }
        else {
            $xpos_robo = $xpos;
            $ypos_robo = $ypos;
        }
        $robo_turn = !$robo_turn;
    }
}
print "Number of moves: $num_moves, number of houses receving presents: " . scalar(keys(%map)) . "\n";


