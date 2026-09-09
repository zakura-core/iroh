# Zakura Iroh compatibility branch

This branch starts at upstream Iroh 1.1.0, revision
`fddf1a4ce29f92c6651eccff68fb366007b9be7d`. It retains published
`ed25519-dalek 2.2.0` and `curve25519-dalek 4.1.3` so applications using BIP32's
exact prerelease digest dependencies can resolve Iroh without changing their
cryptographic packages. The compatibility change consists of three dependency
requirements and the lockfile; production Rust source is unchanged. Additional
tests and preparation tooling validate the fork. The Curve25519 minimum retains
the timing fix released in 4.1.3.

## Consumption

Pin this branch's exact reviewed commit in the consuming workspace's root
`[patch.crates-io]` for `iroh`, `iroh-base`, `iroh-relay` and `iroh-dns` together.
Keep normal registry version requirements in dependency declarations.
A dependency's patch table is not inherited by downstream applications.
This is a source integration branch; no registry packages are published.
The proposed registry package names, reproducible staging command and consumer
wiring are documented in [PUBLICATION.md](PUBLICATION.md). Publication remains
blocked until the audit and compatibility gates pass and an operator explicitly
authorizes the prepared package set.

## Maintenance

Zakura maintainers own this compatibility branch. Review upstream Iroh and
Dalek security changes before each update, preserve strict signature
verification and existing feature flags, and rerun key/serialization tests,
authenticated connection tests, and consuming workspace checks. Do not infer
production equivalence from successful dependency resolution alone.

Remove the compatibility patch when upstream Iroh and the consuming dependency
graph resolve together and pass the same interoperability checks. Do not mix
BIP32 or Zcash cryptographic implementation changes into this branch.
