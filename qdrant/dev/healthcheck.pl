#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket::INET;

my $socket = IO::Socket::INET->new(
    PeerAddr => 'localhost',
    PeerPort => '6333',
    Proto    => 'tcp',
    Timeout  => 10
);

unless ($socket) {
    print "Cannot connect to qdrant\n";
    exit(1);
}

print $socket "GET / HTTP/1.1\nHost: localhost\n\n";
my $response = <$socket>;
close($socket);

if ($response =~ m|^HTTP/1.1 200|) {
    exit(0);
} else {
    print "Service is down\n";
    exit(1);
}
