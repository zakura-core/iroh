# Networking package publication

The maintained workspace contains `zakura-iroh`, `zakura-iroh-base`,
`zakura-iroh-dns`, and `zakura-iroh-relay` directly. Git consumers and registry
releases use the same manifests. There is no generated package workspace or
separate staging branch.

The public library names and dependency aliases remain `iroh`, `iroh_base`,
`iroh_dns`, and `iroh_relay`. Existing Rust imports do not change. The DNS
server and benchmark packages are not published.

## Verify the source

All four packages use `1.1.0-rc.2` and exact sibling requirements. Previously
published versions must not be overwritten. From the reviewed checkout, run:

```sh
cargo metadata --locked --format-version 1 > /tmp/zakura-iroh-metadata.json
cargo check --locked -p zakura-iroh --lib --no-default-features --features tls-ring
cargo tree --locked -i zakura-iroh-base
cargo tree --locked -i noq
```

The root transport patches are temporary. Cargo does not inherit a dependency's
patch table, so every consuming workspace must provide the same transport
patches until compatible registry releases exist. Successful Git qualification
does not establish that the packages can be published or built from crates.io.

## Package and publish

Before publication, resolve the transport dependency's release route, replace
its Git patches with compatible registry versions, and refresh `Cargo.lock`.
Recheck version availability and package ownership. Then package and verify the
complete family from a clean, committed checkout:

```sh
cargo package --locked -p zakura-iroh-base -p zakura-iroh-dns \
  -p zakura-iroh-relay -p zakura-iroh
```

This packages and rebuilds the archives locally. It does not upload them.
Publication requires explicit approval. Publish the dependency family in order:

1. `zakura-iroh-base`
2. `zakura-iroh-dns`
3. `zakura-iroh-relay`
4. `zakura-iroh`

The checked-in manifests retain published Dalek dependencies and pin relay LRU
to `0.18.3`. Preserve those constraints when publishing. Review authentication
compatibility and run consuming workspace checks before removing Git patches.

## Consumer wiring

Consumers keep registry dependency declarations. For example:

```toml
[workspace.dependencies.iroh]
package = "zakura-iroh"
version = "=1.1.0-rc.2"
default-features = false
features = ["tls-ring"]
```

Before publication, use root `[patch.crates-io]` entries for all four packages,
pinned to one reviewed commit of this maintained branch. Patch the complete
transport family in the consumer's root as well. No package renaming is needed.

Only after all required registry releases are available, remove the Git
patches, refresh the lockfile, and verify metadata and inverse dependency trees.
Rerun packaging, semver, and application checks. Keep draft integration work
open until these gates pass. Publication introduces no blanket cargo-vet trust
or audit exemption.
