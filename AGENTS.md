# Repository guidance

- This repository currently contains project documentation only; there is no application source, package manifest, build system, test suite, or lint/typecheck configuration to run.
- The documentation lives under `Docs/`; `Docs/README.md` records the business requirements and quality scenarios, while `Docs/AnteProyecto.md` records the solution architecture, objectives, roadmap, and references.
- Keep diagrams and their Markdown references together under `Docs/img/`; use paths relative to the document (for example, `./img/dCtx.png`). The editable diagram source is `Docs/img/diagrams.excalidraw`.
- The project domain is the SICEE system for digitizing wood-stove water-boiling tests (WBT), thermal efficiency, and emissions data for the CII/USAC; preserve the existing Spanish terminology and requirement IDs when editing documentation.
- No repository-local development or verification command is defined. For documentation-only changes, verify Markdown links and referenced assets manually, and inspect `git diff` before committing.
