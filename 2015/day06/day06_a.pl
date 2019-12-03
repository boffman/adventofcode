#!/usr/bin/perl -w
use strict;

my %grid;

sub set_grid {
    my ($x1, $y1, $x2, $y2, $value) = @_;
    for my $y ($y1 .. $y2) {
        for my $x ($x1 .. $x2) {
            if ($value == -1) {
                $grid{"$x,$y"} = !$grid{"$x,$y"};
            }
            else {
                $grid{"$x,$y"} = $value;
            }
        }
    }
}

sub count_lit {
    my $count = 0;
    for my $value (values(%grid)) {
        $count += $value;
    }
    return $count;
}

set_grid(0, 0, 999, 999, 0);

while (my $line = <>) {
    print $line;
    chomp($line);
    my ($cmd, $x1, $y1, $x2, $y2) = ($line =~ /^(.+) (\d+),(\d+) through (\d+),(\d+)/);
    if ($cmd eq 'turn on') {
        set_grid($x1, $y1, $x2, $y2, 1);
    }
    elsif ($cmd eq 'turn off') {
        set_grid($x1, $y1, $x2, $y2, 0);
    }
    if ($cmd eq 'toggle') {
        set_grid($x1, $y1, $x2, $y2, -1);
    }
}

print "Number of lit lights: " . count_lit() . "\n";

