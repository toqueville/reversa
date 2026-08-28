#!/usr/bin/env node
// Smoke test for the installer's mark transport.
//
// The installer (lib/installer/writer.js) installs each skill with
// cpSync(src, dest, { recursive: true }). This test exercises that same
// mechanism in a temporary folder and confirms that BOTH invocation axis
// marks survive the copy — the disable-model-invocation flag in SKILL.md
// and policy.allow_implicit_invocation in agents/openai.yaml. This ensures
// that the context savings also apply on the user's machine, not just at the source.
import { cpSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const SKILL = 'reversa-scout'; // representative user-invoked skill
const src = join(ROOT, 'agents', SKILL);

const tmp = mkdtempSync(join(tmpdir(), 'reversa-transport-'));
let failures = 0;
const check = (cond, msg) => { if (!cond) { console.error(`  ✗ ${msg}`); failures++; } else { console.log(`  ✓ ${msg}`); } };

try {
  const dest = join(tmp, SKILL);
  cpSync(src, dest, { recursive: true });

  const skill = readFileSync(join(dest, 'SKILL.md'), 'utf8');
  check(/^disable-model-invocation:\s*true\s*$/m.test(skill),
    'disable-model-invocation flag carried over to the installed SKILL.md');

  const yaml = readFileSync(join(dest, 'agents', 'openai.yaml'), 'utf8');
  check(/^\s*allow_implicit_invocation:\s*false\s*$/m.test(yaml),
    'policy.allow_implicit_invocation carried over in the installed agents/openai.yaml');
  check(/display_name:/.test(yaml),
    'interface.display_name present in the installed openai.yaml');
} finally {
  rmSync(tmp, { recursive: true, force: true });
}

console.log(failures ? `\nRESULT: ✗ ${failures} failure(s)` : '\nRESULT: ✓ transport intact');
process.exit(failures ? 1 : 0);
