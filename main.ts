// The Wednesday Record — news-image-20261125 entry (Node 22, standard library only).
// The entry image is the entry.png beside this file (rendered deterministically by draw.py);
// this program copies it to the output directory.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
