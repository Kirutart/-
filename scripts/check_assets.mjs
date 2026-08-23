import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sources = ['index.html', 'service-worker.js'];
const refs = new Set();

for (const source of sources) {
  const content = readFileSync(resolve(root, source), 'utf8');
  for (const match of content.matchAll(/(?:\.\/)?assets\/[A-Za-z0-9_./-]+\.(?:webp|png|ttf)/g)) {
    refs.add(match[0].replace(/^\.\//, ''));
  }
}

const missing = [...refs].filter(path => !existsSync(resolve(root, path)));
if (missing.length) {
  console.error('Missing local assets:', missing.join(', '));
  process.exit(1);
}
console.log(`Checked ${refs.size} local asset references.`);
