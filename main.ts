// news-image-20261123 entry: the front page is drawn by render.py (Python
// + PIL) and shipped in this repository as entry.png. This program copies
// that image to the output directory the grader provides:
// MAKEFUN_OUTPUT_DIR when set, otherwise /output. It needs no network and
// writes the same bytes every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
