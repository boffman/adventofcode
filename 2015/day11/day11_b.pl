#!/usr/bin/perl -w
use strict;

sub has_three_increasing {
    my $str = shift;
    for (my $ix=0; $ix<length($str)-3; $ix++) {
        my $current = substr($str, $ix, 1);
        if ($current eq chr(ord(substr($str, $ix+1, 1))-1) &&
            $current eq chr(ord(substr($str, $ix+2, 1))-2)) {
            return 1;
        }
    }
    return 0;
}

sub has_no_forbidden_chars {
    my $str = shift;
    return $str !~ /[iol]/;
}

sub has_two_different_pairs {
    my $str = shift;
    my %pair_chars;
    while ($str =~ /(.)\g1/g) {
        my $c = $1;
        $pair_chars{"$c"} = 1;
    }
    my $has_two = scalar(keys(%pair_chars)) > 1;
    return $has_two ? 1 : 0;
}

sub valid_password {
    my $pwd = shift;

    return has_no_forbidden_chars($pwd) &&
        has_three_increasing($pwd) &&
        has_two_different_pairs($pwd);
}

sub find_next_password {
    my $pwd = shift;
    my $cnt = 0;
    print "Testing $pwd ...\n";
    while (!valid_password($pwd)) {
        $pwd++;
        if (++$cnt == 1000000) {
            print "Testing $pwd ...\n";
            $cnt = 0;
        }
    }
    return $pwd;
}

while (my $line = <>) {
    chomp($line);

    my $pwd = $line;

    $pwd = find_next_password($pwd);
    print "Next password is: $pwd\n";
    $pwd++;
    $pwd = find_next_password($pwd);
    print "Next password is: $pwd\n";
}

