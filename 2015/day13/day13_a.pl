#!/usr/bin/perl -w
use strict;

my %unit_mapping;
my %person_map;
my @person_list;

sub check_happiness {
    my $index_list = shift;
    my @persons = map { $person_list[$_] } @$index_list;
    
    print "Check " . join(" -> ", @persons) . "\n";
    my @keys;
    push(@keys, $persons[-1] . " " . $persons[0];
    push(@keys, $persons[0] . " " . $persons[-1];
    for my $ix (0 .. scalar(@persons)-2) {
        push(@keys, $persons[$ix] . " " . $persons[$ix+1];
        push(@keys, $persons[$ix+1] . " " . $persons[$ix];
    }
    for my 
}

sub permutate {
    my $levels = shift;
    my $callback = shift;
    my $index_hash = shift;
    my $index_list = shift;
    my $depth = shift;
    $index_hash = {} unless ($index_hash);
    $index_list = [] unless ($index_list);
    $depth = 0 unless ($depth);
    for my $ix (0 .. $levels-1) {
        next if (defined($index_hash->{$ix}));
        last if ($ix>0) && $depth == 0;
        $index_hash->{$ix} = 1;
        push(@$index_list, $ix);
        if (scalar(@$index_list) == $levels) {
            $callback->($index_list);
        }
        else {
            permutate($levels, $callback, $index_hash, $index_list, $depth+1);
        }
        delete $index_hash->{$ix};
        pop(@$index_list);
    }
}


while (my $line = <>) {
    if ($line =~ /^(\S+) would (\S+) (\d+) happiness units by sitting next to (\S+)\./) {
        my ($person1, $gain_lose, $units, $person2) = ($1,$2,$3,$4);
        my $key = "$person1 $person2";
        $units = -$units if ($gain_lose eq 'lose');
        $unit_mapping{$key} = $units;
        $person_map{$person1} = 1;
        $person_map{$person2} = 1;
    }
}

@person_list = keys(%person_map);

permutate(scalar(@person_list), \&check_happiness);


