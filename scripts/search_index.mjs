// Build the page's search index once, at publish time, and write it as files.
//
//   node scripts/search_index.mjs <full page data.json> <output directory>
//
// The page data is publish.build_data with the prose, not the skeleton. The
// index is site/search.js's own buildIndex, so the files say exactly what the
// browser would compute, and packIndex cuts them the way shippedIndex reads
// them. Called by scripts/publish.py; no network.
//
// shortcut: the association count keeps up to 946 term pairs per document in
// one Map, about 1.3 GB at 16275 terms; past roughly five times that, cap
// ASSOC_TERMS_PER_DOC in site/search.js or count the pairs prefix by prefix.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { buildIndex, packIndex } from "../site/search.js";

const [source, output] = process.argv.slice(2);
if (!source || !output) {
  console.error("usage: node scripts/search_index.mjs <data.json> <output directory>");
  process.exit(2);
}
const { meta, shards } = packIndex(buildIndex(JSON.parse(readFileSync(source, "utf8"))));
mkdirSync(output, { recursive: true });
writeFileSync(join(output, "meta.json"), JSON.stringify(meta));
for (const [key, shard] of Object.entries(shards)) writeFileSync(join(output, `${key}.json`), JSON.stringify(shard));
console.log(`search index: ${meta.vocabulary.length} terms in ${meta.keys.length} files`);
