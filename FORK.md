# Zakura Iroh compatibility branch

This branch starts at upstream Iroh 1.1.0, revision
`fddf1a4ce29f92c6651eccff68fb366007b9be7d`. It retains published
`ed25519-dalek 2.2.0` and `curve25519-dalek 4.1.3` so applications using BIP32's
exact prerelease digest dependencies can resolve Iroh without changing their
cryptographic packages. The fork retains those dependency requirements and
pins relay LRU to 0.18.3.
Release candidate 1 also lets consumers disable QUIC NAT traversal with
`max_remote_nat_traversal_addresses(0)`. This disables candidate-address exchange
and peer-directed UDP probes without disabling direct connections. The upstream
nonzero defaults are preserved for consumers that do not opt out.

## Consumption

The maintained workspace uses the four `zakura-iroh*` package names directly.
Version `1.1.0-rc.2` adds connection ownership and admission before QUIC
handshakes. Rust library names and imports stay unchanged.

Until compatible packages are published, consumers can patch the complete
package family to a reviewed source commit. The transport family also needs
its own root patches. Publication and consumer wiring are documented in
[PUBLICATION.md](PUBLICATION.md). Published `1.1.0-rc.1` remains unchanged.

## Maintenance

Zakura maintainers own this compatibility branch. Review upstream Iroh and
Dalek security changes before each update, preserve strict signature
verification and existing feature flags, and rerun key/serialization tests,
authenticated connection tests, and consuming workspace checks. Do not infer
production equivalence from successful dependency resolution alone.

Remove the compatibility patch when upstream Iroh and the consuming dependency
graph resolve together and pass the same interoperability checks. Do not mix
BIP32 or Zcash cryptographic implementation changes into this branch.
