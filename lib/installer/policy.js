// Single source of Reversa's non-destructiveness rule: the only folders the
// framework may create/write to. Renders the rule text injected into each
// engine entry file at install time.
//
// `_reversa_sdd` and `_reversa_forward` are user-configurable
// (state.json: output_folder / forward_folder). `_reversa_docs` is fixed for
// now; if it ever becomes configurable (docs_folder), just pass it here.

// Also exported for future use by updateGitignore/uninstall, which currently
// only know about `.reversa/` + output_folder and diverge from the global rule.
export function getWritableFolders({
  outputFolder = '_reversa_sdd',
  forwardFolder = '_reversa_forward',
} = {}) {
  return ['.reversa/', `${outputFolder}/`, '_reversa_docs/', `${forwardFolder}/`];
}

export function renderPolicyBlock(opts = {}) {
  const folders = getWritableFolders(opts).map((f) => `\`${f}\``);
  const list = `${folders.slice(0, -1).join(', ')} and ${folders[folders.length - 1]}`;
  return [
    'Never delete, modify, or overwrite pre-existing files from the legacy project.',
    `Reversa only writes to ${list}.`,
  ].join('\n');
}
