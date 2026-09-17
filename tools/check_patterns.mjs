// Both Python and the desktop's Unicode JavaScript RegExp consume these patterns.
// A Python-valid escape is not necessarily valid in JavaScript.
import { readFileSync } from 'node:fs'

for (const file of ['infrastructureProducts', 'fixedEquipmentProducts']) {
  const rows = JSON.parse(readFileSync(new URL(`../catalogues/${file}.json`, import.meta.url), 'utf8'))
  for (const row of rows) {
    const pattern = new RegExp(row.pattern, 'iu')
    for (const example of row.examples ?? []) {
      if (!pattern.test(example)) throw new Error(`JavaScript fixture failed: ${row.name}`)
    }
  }
}
console.log('Catalogue patterns compile and match their examples in Unicode JavaScript.')
