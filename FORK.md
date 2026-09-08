# Zakura Iroh compatibility branch

This branch starts at upstream Iroh 1.1.0, revision
`fddf1a4ce29f92c6651eccff68fb366007b9be7d`. It retains published
`ed25519-dalek 2.2.0` and `curve25519-dalek 4.1.3` so applications using BIP32's
exact prerelease digest dependencies can resolve Iroh without changing their
cryptographic packages. Only three dependency requirements and the lockfile
change; production Rust source is unchanged. The Curve25519 minimum retains
the timing fix released in 4.1.3.

## Consumption

Pin this branch's exact reviewed commit in the consuming workspace's root
`[patch.crates-io]` for `iroh`, `iroh-base`, `iroh-relay` and `iroh-dns` together.
Keep normal registry version requirements in dependency declarations.
A dependency's patch table is not inherited by downstream applications.
This is a source integration branch; no registry packages are published.
Registry publication remains blocked until an upstream-compatible release or
separately approved publication strategy exists.

## Maintenance

Zakura maintainers own this compatibility branch. Review upstream Iroh and
Dalek security changes before each update, preserve strict signature
verification and existing feature flags, and rerun key/serialization tests,
authenticated connection tests, and consuming workspace checks. Do not infer
production equivalence from successful dependency resolution alone.

Remove the compatibility patch when upstream Iroh and the consuming dependency
graph resolve together and pass the same interoperability checks. Do not mix
BIP32 or Zcash cryptographic implementation changes into this branch.
