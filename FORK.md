# Zakura Iroh compatibility branch

This branch starts at upstream Iroh 1.1.0, revision
`fddf1a4ce29f92c6651eccff68fb366007b9be7d`. It retains published
`ed25519-dalek 2.2.0` and `curve25519-dalek 4.1.3` so applications using BIP32's
exact prerelease digest dependencies can resolve Iroh without changing their
cryptographic packages. The fork retains those dependency requirements and pins relay LRU to 0.18.3.
Release candidate 1 also lets consumers disable QUIC NAT traversal with
`max_remote_nat_traversal_addresses(0)`. This disables candidate-address exchange
and peer-directed UDP probes without disabling direct connections. The upstream
nonzero defaults are preserved for consumers that do not opt out.

## Consumption

The four `zakura-iroh*` packages at `1.1.0-rc.0` are published on crates.io.
The `1.1.0-rc.1` package set adds the NAT traversal opt-out. Package preparation,
publication order and registry dependency wiring are in [PUBLICATION.md](PUBLICATION.md).
Use the published packages with exact sibling versions. Applications do not need
root Git patches for these registry packages.

## Maintenance

Zakura maintainers own this compatibility branch. Review upstream Iroh and
Dalek security changes before each update, preserve strict signature
verification and existing feature flags, and rerun key/serialization tests,
authenticated connection tests, and consuming workspace checks. Do not infer
production equivalence from successful dependency resolution alone.

Remove the compatibility patch when upstream Iroh and the consuming dependency
graph resolve together and pass the same interoperability checks. Do not mix
BIP32 or Zcash cryptographic implementation changes into this branch.
