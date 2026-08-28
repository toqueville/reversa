#!/usr/bin/env python3
"""
Invocation axis verifier.

Ensures each skill declares its invocation in BOTH marks, in lockstep:
  - Claude Code : disable-model-invocation: true   in SKILL.md
  - Codex       : policy.allow_implicit_invocation: false  in agents/openai.yaml

Usage:  verify_invocation.py <skills-dir> [<skills-dir> ...]
Exits with code 1 if there is any violation.
"""
import re, sys, pathlib

def frontmatter(p):
    t = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    return m.group(1) if m else None

def check(raiz):
    raiz = pathlib.Path(raiz)
    erros, skills = [], sorted(raiz.glob("*/SKILL.md"))
    if not skills:
        return [f"{raiz}: no SKILL.md found"], 0, 0
    n_user = 0
    for sk in skills:
        nome = sk.parent.name
        fm = frontmatter(sk)
        if fm is None:
            erros.append(f"{nome}: SKILL.md without frontmatter"); continue

        claude_user = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M))

        y = sk.parent / "agents" / "openai.yaml"
        if not y.exists():
            erros.append(f"{nome}: missing agents/openai.yaml (Codex mark absent)")
            continue
        yt = y.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        codex_user = bool(re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", yt, re.M))

        # Codex UI metadata
        if not re.search(r"^\s*display_name:", yt, re.M):
            erros.append(f"{nome}: openai.yaml missing interface.display_name")
        if not re.search(r"^\s*short_description:", yt, re.M):
            erros.append(f"{nome}: openai.yaml missing interface.short_description")

        # LOCKSTEP: user-invoked in both marks, or in neither
        if claude_user != codex_user:
            erros.append(
                f"{nome}: MISMATCH — Claude={'user' if claude_user else 'model'}-invoked, "
                f"Codex={'user' if codex_user else 'model'}-invoked")
        if claude_user:
            n_user += 1

            # user-invoked description is human-facing: no trigger lists
            d = re.search(r"^description:\s*(.+?)(?=\n[a-zA-Z_-]+:|\Z)", fm, re.S | re.M)
            if d:
                desc = " ".join(d.group(1).split())
                if re.search(r"Use quando|Use when|digitar\s+[\"'`]?/", desc, re.I):
                    erros.append(
                        f"{nome}: user-invoked description still has model trigger "
                        f"({len(desc)} chars) — should be a human one-line summary")
    return erros, len(skills), n_user


def main(dirs):
    total_erros = 0
    for d in dirs:
        erros, n, n_user = check(d)
        print(f"\n=== {d}")
        print(f"    {n} skills - {n_user} user-invoked - {n - n_user} model-invoked")
        if erros:
            print(f"    {len(erros)} violation(s):")
            for e in erros[:40]:
                print(f"      ✗ {e}")
            if len(erros) > 40:
                print(f"      ... and {len(erros) - 40} more")
        else:
            print("    ✓ invocation axis intact, 0 mismatches")
        total_erros += len(erros)

    # the trees must be identical to each other
    if len(dirs) > 1:
        import filecmp
        base = dirs[0]
        for outra in dirs[1:]:
            cmp = filecmp.dircmp(base, outra)
            def difs(c, pref=""):
                out = [pref + x for x in c.left_only + c.right_only + c.diff_files]
                for sub, cc in c.subdirs.items():
                    out += difs(cc, pref + sub + "/")
                return out
            d = difs(cmp)
            print(f"\n=== trees {base} x {outra}")
            if d:
                print(f"    ✗ {len(d)} divergence(s): {d[:5]}")
                total_erros += len(d)
            else:
                print("    ✓ identical")

    print(f"\n{'='*60}")
    print("RESULT:", "✓ APPROVED" if total_erros == 0 else f"✗ {total_erros} violation(s)")
    return 1 if total_erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["."]))
