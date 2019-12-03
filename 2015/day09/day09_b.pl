#!/usr/bin/perl -w
use strict;

my %places_hash;
my %distance;

while (my $line = <>) {
    chomp($line);
    my ($from, $to, $distance) = ($line =~ /^(\S+) to (\S+) = (\d+)/);
    $places_hash{$_} = 1 for ($from, $to);
    $distance{"$from to $to"} = $distance;
    $distance{"$to to $from"} = $distance;
}
my @places = keys(%places_hash);
my $max_distance = undef;

sub check_distance {
    my $index_list = shift;
    my @values = map { $places[$_] } @$index_list;
    my $total_distance = 0;
    for my $ix (0 .. scalar(@values)-2) {
        my $key = $values[$ix] . " to " . $values[$ix+1];
        $total_distance += $distance{$key};
    }
    #print join('->', @values) . " = $total_distance\n";
    if (!defined($max_distance) || $total_distance > $max_distance) {
        $max_distance = $total_distance;
    }
}

sub permutate {
    my $levels = shift;
    my $callback = shift;
    my $index_hash = shift;
    my $index_list = shift;
    $index_hash = {} unless ($index_hash);
    $index_list = [] unless ($index_list);
    for my $ix (0 .. $levels-1) {
        next if (defined($index_hash->{$ix}));
        $index_hash->{$ix} = 1;
        push(@$index_list, $ix);
        if (scalar(@$index_list) == $levels) {
            $callback->($index_list);
        }
        else {
            permutate($levels, $callback, $index_hash, $index_list);
        }
        delete $index_hash->{$ix};
        pop(@$index_list);
    }
}

permutate(scalar(@places), \&check_distance);

print "Distance of longest route: $max_distance\n";

