#!/usr/bin/env python3
"""Stage renamed networking packages from a commit; never publish or modify the checkout."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tomllib

FAMILY = ("iroh-base", "iroh-dns", "iroh-relay", "iroh")


def prepare(repo, revision, output, version):
    revision = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--verify", revision + "^{commit}"], text=True
    ).strip()
    archive = subprocess.check_output(["git", "-C", str(repo), "archive", revision])
    output.mkdir(parents=True, exist_ok=False)
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(output, filter="data")
    before = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in output.rglob("*.rs")}
    dependency = re.compile(r"^(iroh(?:-base|-dns|-relay)?) = \{([^\n]*)\}", re.MULTILINE)
    for manifest in output.rglob("Cargo.toml"):
        content = manifest.read_text()
        data = tomllib.loads(content)
        name = data.get("package", {}).get("name")
        if name in FAMILY:
            content = content.replace(f'name = "{name}"', f'name = "zakura-{name}"', 1)
            content = content.replace('version = "1.1.0"', f'version = "{version}"', 1)
            content = content.replace('repository = "https://github.com/n0-computer/iroh"',
                                      'repository = "https://github.com/zakura-core/iroh"', 1)
            content = re.sub(r'^description = "([^"]*)"',
                             r'description = "Zakura compatibility fork: \1"', content,
                             count=1, flags=re.MULTILINE)
            readme = manifest.parent / data["package"].get("readme", "README.md")
            if readme.exists():
                readme.write_text(
                    "> This is the Zakura compatibility fork of Iroh 1.1.0. It retains "
                    "published Dalek 2.2 and Curve25519-Dalek 4.1.3. "
                    "See https://github.com/zakura-core/iroh/blob/zakura/v1.1.0/FORK.md.\n\n"
                    + readme.read_text())
            library = name.replace("-", "_")
            if "[lib]" in content:
                content = content.replace("[lib]", f'[lib]\nname = "{library}"', 1)
            else:
                content += f'\n[lib]\nname = "{library}"\n'
        elif name:
            # Servers and benchmarks are outside this publication set.
            if "publish" not in data["package"]:
                content = content.replace("[package]", "[package]\npublish = false", 1)

        def alias(match):
            key, fields = match.groups()
            fields = re.sub(r'\bversion\s*=\s*"[^"]*"\s*,?\s*', '', fields).strip().rstrip(',')
            return f'{key} = {{ package = "zakura-{key}", version = "={version}", {fields} }}'

        content = dependency.sub(alias, content)
        tomllib.loads(content)
        manifest.write_text(content)
    after = {str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in output.rglob("*.rs")}
    assert before == after, "package staging must not change Rust source"
    plan = {"source_revision": revision, "version": version,
            "publish_order": ["zakura-" + name for name in FAMILY],
            "rust_source_sha256": before}
    (output / "zakura-package-plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    (output / "zakura-consumer.toml").write_text(
        '# Merge this registry dependency into Zakura only after publication.\n'
        '[workspace.dependencies]\n'
        f'iroh = {{ package = "zakura-iroh", version = "={version}", '
        'default-features = false, features = ["tls-ring"] }\n'
        '# Remove the four existing root Iroh Git patches after switching.\n'
    )
    print(json.dumps({"output": str(output), "revision": revision,
                      "version": version, "publish_order": plan["publish_order"]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--version", default="1.1.0-rc.0")
    args = parser.parse_args()
    if not re.fullmatch(r"1\.1\.0-rc\.(0|[1-9][0-9]*)", args.version):
        parser.error("version must be an explicit 1.1.0 release candidate")
    prepare(Path(__file__).resolve().parents[1], args.revision, args.output.resolve(), args.version)


if __name__ == "__main__":
    main()
