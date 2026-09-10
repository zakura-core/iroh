# Networking package preparation

The checked-in Iroh package identities remain unchanged for source integration.
The preparation script emits a separate, reproducible workspace from a committed
revision. It changes package metadata and dependency aliases without changing
Rust source or modifying the checkout. It cannot publish anything.

## Proposed packages

All four packages use `1.1.0-rc.1`, derived from upstream Iroh 1.1.0. Publish in
this dependency order only after explicit approval:

1. `zakura-iroh-base`
2. `zakura-iroh-dns`
3. `zakura-iroh-relay`
4. `zakura-iroh`

The DNS server and benchmark packages are outside this set and are marked
`publish = false` in the prepared workspace. Existing license files and upstream
authorship are retained. Public library names and dependency aliases remain
`iroh`, `iroh_base`, `iroh_dns`, and `iroh_relay`; package names identify the fork.
The manifests keep upstream noq 1.2 and published Dalek dependencies.
The relay package pins LRU to 0.18.3 so consumers without this workspace
lockfile cannot select 0.18.4's faulty `retain` implementation.

## Prepare and verify

Run with Python 3.12 or newer, using a destination that does not already exist:

```sh
python3 scripts/prepare-zakura-packages.py --revision HEAD --output /tmp/zakura-iroh-rc1
cd /tmp/zakura-iroh-rc1
cargo metadata --format-version 1 > metadata.json
cargo package -p zakura-iroh-base -p zakura-iroh-dns -p zakura-iroh-relay -p zakura-iroh
```

The last command packages and rebuilds the archives locally; it does not upload
them. Cargo stages the sibling packages together, so this validation does not
require reserving registry names. `zakura-package-plan.json` records the source
commit and hashes every Rust file. Keep this evidence with the built archives.

`zakura-consumer.toml` is the post-publication dependency template for Zakura.
Only after all four packages are available, replace its `iroh` workspace
dependency with the template and remove the four old Iroh root Git patches.
Refresh the lockfile, verify the complete family and features with Cargo
metadata and inverse trees, then rerun packaging, semver and application tests.
Check that BIP32 and the Zcash cryptographic dependency versions remain unchanged.

## Before publication

The four package names are already owned and `1.1.0-rc.0` is published.
Recheck version availability and owners before an authorized publication.
Preparation does not authorize a registry upload or a release tag.

Archive validation does not replace cargo-vet coverage of the new dependency
graph, review of authentication compatibility, or full-node interoperability
checks. Keep the integration draft until those gates are satisfied. No blanket
trust or audit exemption is introduced by this preparation.
