#!/usr/bin/env python3
"""
Reversa invocation axis verifier (single source tree `agents/`).

Every skill is either user-invoked or model-invoked, with no third state. The
verifier ensures that both axis marks are in lockstep WITHIN each skill:

  - Claude Code : disable-model-invocation: true        in SKILL.md
  - Codex       : policy.allow_implicit_invocation: false  in agents/openai.yaml

A skill is user-invoked in both harnesses or in neither. This is the SOURCE
repository (single tree); the installer replicates each skill via recursive copy,
so parity between `.claude/skills` and `.agents/skills` on the user's machine is
structural — what needs guarding here is the axis, not equality between trees.

Usage:  scripts/verify-invocation.py [<skills-dir>]   (default: agents)
Exits with code 1 if any violation is found (serves as a CI gate).
"""
import re, sys, pathlib

# MODEL trigger signatures — forbidden in user-invoked descriptions.
# These are enumerations of typed commands/phrases, not prose usage hints.
TRIGGER_SIGS = ('digitar "', 'Use com "', 'Ative com ', 'pedir "')


def frontmatter(p):
    t = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    return m.group(1) if m else None


def check(raiz):
    raiz = pathlib.Path(raiz)
    errors = []
    skills = sorted(raiz.glob("*/SKILL.md"))
    if not skills:
        return [f"{raiz}: no SKILL.md found"], 0, 0
    n_user = 0
    for sk in skills:
        nome = sk.parent.name
        fm = frontmatter(sk)
        if fm is None:
            errors.append(f"{nome}: SKILL.md missing frontmatter"); continue

        claude_user = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M))

        y = sk.parent / "agents" / "openai.yaml"
        if not y.exists():
            errors.append(f"{nome}: missing agents/openai.yaml (Codex mark absent)")
            continue
        yt = y.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        codex_user = bool(re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", yt, re.M))

        if not re.search(r"^\s*display_name:", yt, re.M):
            errors.append(f"{nome}: openai.yaml missing interface.display_name")
        if not re.search(r"^\s*short_description:", yt, re.M):
            errors.append(f"{nome}: openai.yaml missing interface.short_description")

        # LOCKSTEP: user-invoked in both marks, or in neither.
        if claude_user != codex_user:
            errors.append(
                f"{nome}: MISMATCH — Claude={'user' if claude_user else 'model'}-invoked, "
                f"Codex={'user' if codex_user else 'model'}-invoked")

        if claude_user:
            n_user += 1
            d = re.search(r"^description:\s*(.+?)(?=\n[a-zA-Z_-]+:|\Z)", fm, re.S | re.M)
            if d:
                desc = " ".join(d.group(1).split()).strip().strip("'\"")
                hit = next((s for s in TRIGGER_SIGS if s in desc), None)
                if hit:
                    errors.append(
                        f"{nome}: user-invoked description still has model trigger "
                        f"(signature {hit!r}) — should be a human summary without trigger lists")
    return errors, len(skills), n_user


def main(dirs):
    total_errors = 0
    for d in dirs:
        errors, n, n_user = check(d)
        print(f"\n=== {d}")
        print(f"    {n} skills · {n_user} user-invoked · {n - n_user} model-invoked")
        if errors:
            print(f"    {len(errors)} violation(s):")
            for e in errors[:60]:
                print(f"      ✗ {e}")
            if len(errors) > 60:
                print(f"      … and {len(errors) - 60} more")
        else:
            print("    ✓ invocation axis intact, 0 mismatches")
        total_errors += len(errors)

    print("\n" + "=" * 60)
    print("RESULT:", "✓ PASSED" if total_errors == 0 else f"✗ {total_errors} violation(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    argv = sys.argv[1:] or ["agents"]
    sys.exit(main(argv))
