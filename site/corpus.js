// The page data in the two pieces it is published as.
//
// graph.json is the skeleton: every term with its names, kind, classes and a
// note of which prose it has, and every edge. It is what the views, the matrix
// and the search over names need, and it grows by about forty bytes a term
// compressed. The prose (definitions, notes, sources, statements) lies in
// details/<n>.json, a fixed number of terms per file in skeleton order, and is
// read when a term is opened or the full text is asked for. Pure; no DOM, no
// network.

export const PROSE = ["definition", "note", "comment", "sources", "statements"];

/** The skeleton as the { meta, nodes, edges } shape every module reads. */
export function expand(skeleton) {
  const nodes = skeleton.nodes.map((node, position) => ({
    definition: {},
    note: {},
    comment: {},
    sources: [],
    statements: [],
    has: [],
    ...node,
    label: node.label ?? node.labels.en ?? node.labels[""],
    chunk: Math.floor(position / skeleton.meta.chunk),
  }));
  const edges = skeleton.edges.map(([source, rel, target]) => ({
    source: nodes[source].id,
    rel: skeleton.rels[rel],
    target: nodes[target].id,
  }));
  return { meta: skeleton.meta, nodes, edges };
}

/** Put one file of prose onto the nodes it belongs to. */
export function absorb(nodesById, chunk) {
  for (const [id, prose] of Object.entries(chunk)) Object.assign(nodesById.get(id), prose);
}
