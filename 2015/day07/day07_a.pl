#!/usr/bin/perl -w
use strict;
no warnings 'recursion';

my %wires;

sub debug {
    if ($ENV{DEBUG}) {
        print @_;
    }
}

sub get_value {
    my $def = shift;
    if ($def =~ /^[a-z]/) {
        return $wires{$def};
    }
    return int($def);
}

sub do_assign {
    my ($input, $dst_wire) = @_;
    $wires{$dst_wire} = {};
    if ($input =~ /\d/) {
        $wires{$dst_wire}->{value} = $input;
    }
    else {
        $wires{$dst_wire}->{lval} = $input;
    }
}

sub do_not {
    my ($input, $dst_wire) = @_;
    $wires{$dst_wire} = {};
    $wires{$dst_wire}->{gate} = 'NOT';
    $wires{$dst_wire}->{rval} = $input;
}

sub do_gate {
    my ($input1, $gate, $input2, $dst_wire) = @_;
    $wires{$dst_wire} = {};
    $wires{$dst_wire}->{gate} = $gate;
    $wires{$dst_wire}->{lval} = $input1;
    $wires{$dst_wire}->{rval} = $input2;
}

sub evaluate_circuit {
    my $dst_wire = shift;
    my $indent = shift;
    $indent = 0 unless($indent);
    debug " " x $indent . "evaluate_circuit: $dst_wire IN {\n";
    $indent += 2;
    my $wire = $wires{$dst_wire};
    my $value;
    if (!defined($wire->{gate})) {
        if (defined($wire->{value})) {
            debug " " x $indent . "value\n";
            $value = int($wire->{value});
        }
        else {
            debug " " x $indent . "lval\n";
            $value = evaluate_circuit($wire->{lval}, $indent);
        }
    }
    elsif ($wire->{gate} eq 'NOT') {
        debug " " x $indent . "NOT\n";
        my $rval = $wire->{rval} =~ /\d/ ? int($wire->{rval}) : evaluate_circuit($wire->{rval}, $indent);
        $value = ~$rval ^ ~65535;
    }
    else {
        my $gate = $wire->{gate};
        debug " " x $indent . $gate . "\n";
        my $rval = $wire->{rval} =~ /\d/ ? int($wire->{rval}) : evaluate_circuit($wire->{rval}, $indent);
        my $lval = $wire->{lval} =~ /\d/ ? int($wire->{lval}) : evaluate_circuit($wire->{lval}, $indent);
        if ($gate eq 'AND') {
            $value = ($lval & $rval);
        }
        elsif ($gate eq 'OR') {
            $value = ($lval | $rval);
        }
        elsif ($gate eq 'LSHIFT') {
            $value = ($lval << $rval);
        }
        elsif ($gate eq 'RSHIFT') {
            $value = ($lval >> $rval);
        }
        else {
            die("Unknown gate: $gate");
        }
    }
    $indent -= 2;
    debug " " x $indent . "} evaluate_circuit: $dst_wire OUT: $value\n";
    $wire->{value} = $value;
    $wire->{gate} = undef;
    return $value;
}

while (my $line = <>) {
    chomp($line);
    debug "$line\n";
    my ($instr, $dst_wire) = ($line =~ /^(.+) -> (.+)/);
    my @instr_parts = split(' ', $instr);
    my $num_parts = scalar(@instr_parts);
    if ($num_parts == 1) {
        do_assign($instr_parts[0], $dst_wire);
    }
    elsif ($num_parts == 2) {
        do_not($instr_parts[1], $dst_wire);
    }
    elsif ($num_parts == 3) {
        my ($op1, $gate, $op2) = @instr_parts;
        do_gate($op1, $gate, $op2, $dst_wire);
    }
    else {
        die("Parsing failed");
    }
}

debug "\nWires:\n";
for my $wire (reverse sort keys(%wires)) {
    print "$wire: " . evaluate_circuit($wire) . "\n";
    debug "-" x 100 . "\n";
}
