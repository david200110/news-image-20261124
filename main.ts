import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

function sha256(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function findEntry(): string {
  const botDir = process.env.MAKEFUN_BOT_DIR;
  if (botDir) {
    const p = join(botDir, "entry.png");
    if (existsSync(p)) return p;
  }
  const local = join(here, "entry.png");
  if (existsSync(local)) return local;
  const cwd = join(process.cwd(), "entry.png");
  if (existsSync(cwd)) return cwd;
  throw new Error("entry.png not found in MAKEFUN_BOT_DIR, script dir, or cwd");
}

const src = findEntry();
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
const want = sha256(src);
const got = sha256(dest);
if (want !== got) {
  throw new Error(`entry.png copy mismatch: source ${want} vs output ${got}`);
}
console.log("entry.png written to", dest, "sha256", got);
