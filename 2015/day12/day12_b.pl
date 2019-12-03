#!/usr/bin/perl -w
use strict;
use JSON::PP;

sub traverse {
    my $ref = shift;
    my $ref_type = ref($ref);

    my $sum = 0;
    if ($ref_type eq 'HASH') {
        for my $value (values(%$ref)) {
            if ($value eq 'red') {
                return 0;
            }
            elsif (ref($value)) {
                $sum += traverse($value);
            }
            elsif ($value =~ /\d/) {
                $sum += $value;
            }
        }
    }
    elsif ($ref_type eq 'ARRAY') {
        for my $value (@$ref) {
            if (ref($value)) {
                $sum += traverse($value);
            }
            elsif ($value =~ /\d/) {
                $sum += $value;
            }
        }
    }
    return $sum;
}

my $sum = 0;
while (my $line = <>) {
    chomp($line);
    my $json = JSON::PP->new;
    my $perl_json  = $json->decode($line);
    $sum += traverse($perl_json);
}
print "Sum: $sum\n";
