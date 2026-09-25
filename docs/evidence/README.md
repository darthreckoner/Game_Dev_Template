# Evidence records

One record per evidence run of a frozen candidate:
`docs/evidence/<milestone>/<run_id>.md`, with small captures beside it in
`<run_id>/captures/`. Large recordings stay in ignored `work/`; record their
SHA-256 in the evidence record instead.

`$evidence-run` writes these records. The gate definitions, anchored scale, and
record template are in `.agents/skills/evidence-run/references/gates.md`.

Records are immutable once reviewed. A rerun gets a new `run_id` and links the
record it follows. Only the user fills the `human` block's `accepted` field.
