#!/usr/bin/perl -w
use strict;

my %grid;

sub set_grid {
    my ($x1, $y1, $x2, $y2, $value) = @_;
    for my $y ($y1 .. $y2) {
        for my $x ($x1 .. $x2) {
            $grid{"$x,$y"} += $value;
            $grid{"$x,$y"} = 0 if $grid{"$x,$y"} < 0;
        }
    }
}

sub count_total_brightness {
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
        set_grid($x1, $y1, $x2, $y2, -1);
    }
    if ($cmd eq 'toggle') {
        set_grid($x1, $y1, $x2, $y2, 2);
    }
}

print "Total brightness: " . count_total_brightness() . "\n";

