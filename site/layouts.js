// The arrangements the graph can be drawn in.
//
// One picture answers one question. The rings say what the vocabulary is made
// of and say nothing about which tradition carries what; the tradition sectors
// say that and flatten the vocabulary. Neither is the true shape of the graph,
// because a graph has no true shape — which is the reason for offering more
// than one rather than tuning a single layout until it is merely adequate at
// everything.
//
// Every view here is a pure function from the published data to model-space
// coordinates. Cytoscape fits them to the canvas, so the numbers only have to
// be right relative to each other, and nothing in this file touches the DOM.

// Model-space spacing. A node is 21 units across and its label wraps at 68, so
// anything under about forty units of separation puts two labels on top of
// each other at fitted zoom.
const ITEM_GAP = 46;
const RING_GAP = 56;

const TAU = Math.PI * 2;
const local = (curie) => curie.split(":").pop();

/**
 * The derived facts every view wants: who is next to whom, how connected each
 * term is, which tradition carries it, and which class it instantiates.
 * Computed once per data load and handed to each view.
 */
export function context(data) {
  const byId = new Map(data.nodes.map((node) => [node.id, node]));
  const neighbours = new Map(data.nodes.map((node) => [node.id, []]));
  const traditionOf = new Map();
  for (const edge of data.edges) {
    neighbours.get(edge.source)?.push(edge.target);
    neighbours.get(edge.target)?.push(edge.source);
    if (edge.rel === "withinTradition" && !traditionOf.has(edge.source)) {
      traditionOf.set(edge.source, edge.target);
    }
  }
  // The class an instance instantiates. A node may declare several types; the
  // first pm: one is the claim form it was written as, which is the one every
  // view here groups by.
  const classOf = new Map();
  for (const node of data.nodes) {
    if (node.kind !== "instance" && node.kind !== "tradition") continue;
    const type = node.types.find((candidate) => candidate.startsWith("pm:"));
    if (type && byId.has(type)) classOf.set(node.id, type);
  }
  return {
    byId,
    neighbours,
    traditionOf,
    classOf,
    degree: new Map(data.nodes.map((node) => [node.id, neighbours.get(node.id).length])),
  };
}

// ---------------------------------------------------------------------------
// Shared geometry
// ---------------------------------------------------------------------------

/** The mean direction of a set of angles, or null when they cancel out. */
function meanAngle(angles) {
  if (!angles.length) return null;
  const x = angles.reduce((sum, angle) => sum + Math.cos(angle), 0);
  const y = angles.reduce((sum, angle) => sum + Math.sin(angle), 0);
  return x === 0 && y === 0 ? null : Math.atan2(y, x);
}

/** Midpoint of the widest gap in a sorted list of angles. */
function widestGapMid(sorted) {
  if (sorted.length === 0) return -Math.PI / 2;
  let index = 0;
  let widest = -1;
  for (let i = 0; i < sorted.length; i++) {
    let gap = sorted[(i + 1) % sorted.length] - sorted[i];
    if (gap <= 0) gap += TAU;
    if (gap > widest) {
      widest = gap;
      index = i;
    }
  }
  const from = sorted[index];
  let to = sorted[(index + 1) % sorted.length];
  if (to <= from) to += TAU;
  return (from + to) / 2;
}

/**
 * Place a ring of nodes: order them by where their already-placed neighbours
 * sit, space them evenly so labels never collide, then rotate the whole ring
 * to the offset that lines it up best with those neighbours. Nodes with no
 * placed neighbour drop into the widest gap, so they land somewhere sensible
 * instead of at zero.
 */
function placeRing(ids, radius, anchorOf, place) {
  const count = ids.length;
  if (count === 0) return;
  const items = ids.map((id) => ({ id, angle: anchorOf(id) }));
  const taken = items.filter((item) => item.angle != null).map((item) => item.angle).sort((a, b) => a - b);
  for (const item of items) {
    if (item.angle != null) continue;
    item.angle = widestGapMid(taken);
    taken.push(((item.angle % TAU) + TAU) % TAU);
    taken.sort((a, b) => a - b);
  }
  items.sort((a, b) => a.angle - b.angle);
  let sumX = 0;
  let sumY = 0;
  items.forEach((item, position) => {
    const anchor = anchorOf(item.id);
    if (anchor == null) return;
    const even = (position * TAU) / count;
    sumX += Math.cos(anchor - even);
    sumY += Math.sin(anchor - even);
  });
  const offset = sumX === 0 && sumY === 0 ? -Math.PI / 2 : Math.atan2(sumY, sumX);
  items.forEach((item, position) => place(item.id, radius, (position * TAU) / count + offset));
}

/**
 * Fill an angular sector with nodes, arc by arc from the inside out, keeping
 * roughly the same spacing between neighbours whatever the radius. Returns the
 * radius the sector reached, so a caller can tell how far its widest group ran.
 */
function fillSector(ids, { from, to, inner, place, gap = ITEM_GAP, ring = RING_GAP }) {
  const width = to - from;
  let radius = inner;
  let index = 0;
  while (index < ids.length) {
    const capacity = Math.max(1, Math.floor((width * radius) / gap));
    const arc = ids.slice(index, index + capacity);
    const step = arc.length > 1 ? Math.min(width / arc.length, gap / radius) : 0;
    const start = (from + to) / 2 - (step * (arc.length - 1)) / 2;
    arc.forEach((id, position) => place(id, radius, start + position * step));
    index += arc.length;
    if (index < ids.length) radius += ring;
  }
  return radius;
}

// The kinds whose labels the drawing keeps legible at fitted zoom. Wherever
// they are packed together they need the room that label takes, not the room a
// dot takes, or their names overlap at every zoom — position and type scale
// together, so no amount of zooming pulls them apart.
const LANDMARKS = new Set(["root", "class", "tradition"]);
const LANDMARK_GAP = 118;
const LANDMARK_RING = 76;

/**
 * Split a circle into one sector per group, sized by how much each group
 * carries. The floor keeps a thin group readable; the proportion keeps a fat
 * one honest. `traditions/daoist.ttl` is deliberately thin, and a view that
 * hid that would be hiding the thing the file was written to show.
 */
function sectors(groups, { floor = 4, gap = 0.03 } = {}) {
  const total = groups.reduce((sum, group) => sum + group.ids.length + floor, 0);
  let angle = -Math.PI / 2;
  return groups.map((group) => {
    const width = (TAU * (group.ids.length + floor)) / total;
    const sector = { ...group, from: angle + gap / 2, to: angle + width - gap / 2 };
    angle += width;
    return sector;
  });
}

/** Group ids by a key function, dropping empties, ordered by the given order. */
function groupBy(ids, keyOf) {
  const groups = new Map();
  for (const id of ids) {
    const key = keyOf(id);
    if (key == null) continue;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(id);
  }
  return groups;
}

/** A placer that writes polar coordinates into a positions object. */
function polarPlacer(positions, cx = 0, cy = 0) {
  return (id, radius, angle) => {
    positions[id] = { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
  };
}

// ---------------------------------------------------------------------------
// Rings — the vocabulary's own strata
// ---------------------------------------------------------------------------

// Rings from the centre outward: the root process, the classes that divide it,
// the properties that relate them, and the instances asserted under them.
const RING = { root: 0, class: 1, property: 2, instance: 3, tradition: 3 };
// The gap between rings stays wider than a wrapped label, and the outermost
// ring sits close enough in that the fitted graph still resolves its labels.
const RADIUS = [0, 140, 260, 380];

function ringPositions(data, ctx) {
  const positions = {};
  const angle = new Map(); // only ring nodes get an angle; the centre has none
  const place = (id, radius, value) => {
    angle.set(id, value);
    positions[id] = { x: radius * Math.cos(value), y: radius * Math.sin(value) };
  };
  const anchorOf = (id) =>
    meanAngle(ctx.neighbours.get(id).map((other) => angle.get(other)).filter((value) => value != null));

  // Centre: position only, no angle, so it never biases an outer node's anchor.
  const centre = data.nodes.find((node) => node.kind === "root");
  if (centre) positions[centre.id] = { x: 0, y: 0 };

  // Inner ring: classes, evenly spaced, with the subclasses of the root process
  // grouped ahead of the classes that stand on their own.
  const subclassOfRoot = new Set(
    data.edges.filter((e) => e.rel === "subClassOf" && e.target === centre?.id).map((e) => e.source),
  );
  const classes = data.nodes
    .filter((node) => RING[node.kind] === 1)
    .sort(
      (a, b) =>
        Number(subclassOfRoot.has(b.id)) - Number(subclassOfRoot.has(a.id)) ||
        a.id.localeCompare(b.id),
    );
  classes.forEach((node, position) =>
    place(node.id, RADIUS[1], -Math.PI / 2 + (position * TAU) / classes.length),
  );

  const ids = (ring) => data.nodes.filter((node) => RING[node.kind] === ring).map((node) => node.id);
  placeRing(ids(2), RADIUS[2], anchorOf, place);
  // The outer stratum holds every instance in the corpus. One circle would
  // have to be four times the radius of the rest of the drawing to give each
  // of them a label's width, leaving the vocabulary a dot in the middle of an
  // empty disc; a band of concentric circles keeps the same angular ordering
  // and stays compact enough that the whole graph fits legibly.
  placeBand(ids(3), RADIUS[3], anchorOf, place);
  return positions;
}

/**
 * Spread one stratum over as many concentric circles as it needs. Nodes are
 * dealt out in angular order, so consecutive circles interleave rather than
 * splitting the stratum into an inner and an outer half: two nodes that belong
 * side by side stay side by side, one ring apart.
 */
function placeBand(ids, inner, anchorOf, place) {
  if (!ids.length) return;
  const circles = Math.max(1, Math.ceil((ids.length * ITEM_GAP) / (TAU * inner)));
  const ordered = ids
    .map((id) => ({ id, angle: anchorOf(id) ?? Infinity }))
    .sort((a, b) => a.angle - b.angle || a.id.localeCompare(b.id));
  for (let circle = 0; circle < circles; circle++) {
    const slice = ordered.filter((_, position) => position % circles === circle).map((item) => item.id);
    placeRing(slice, inner + circle * RING_GAP, anchorOf, place);
  }
}

// ---------------------------------------------------------------------------
// Taxonomy — what is asserted under what
// ---------------------------------------------------------------------------

function taxonomyPositions(data, ctx) {
  const positions = {};
  const place = polarPlacer(positions);
  const root = data.nodes.find((node) => node.kind === "root");
  if (root) positions[root.id] = { x: 0, y: 0 };

  // Properties sit inside the classes they relate: vocabulary in the middle,
  // what has been asserted in it further out.
  const properties = data.nodes.filter((node) => node.kind === "property").map((node) => node.id);
  fillSector(properties, { from: -Math.PI / 2, to: -Math.PI / 2 + TAU, inner: 96, place });

  const classes = data.nodes.filter((node) => node.kind === "class");
  const members = groupBy(
    data.nodes.filter((node) => node.kind === "instance" || node.kind === "tradition").map((n) => n.id),
    (id) => ctx.classOf.get(id) ?? null,
  );

  // Each class gets an angular share of the circle proportional to what has
  // actually been written under it, so the picture reports the distribution of
  // the corpus rather than the length of the class list.
  const groups = sectors(
    classes
      .map((node) => ({ id: node.id, ids: (members.get(node.id) ?? []).slice().sort() }))
      .sort((a, b) => b.ids.length - a.ids.length || a.id.localeCompare(b.id)),
  );
  groups.forEach((group, position) => {
    // A class with almost nothing under it gets a sliver of a sector, and two
    // slivers side by side would put their headings on top of each other.
    // Alternating the heading radius separates them without widening the
    // sliver, which would misreport how much stands under the class.
    place(group.id, position % 2 ? 250 : 330, (group.from + group.to) / 2);
    fillSector(group.ids, { from: group.from, to: group.to, inner: 430, place });
  });

  // Instances of a class the graph does not draw still have to land somewhere.
  const placed = new Set(Object.keys(positions));
  const orphans = data.nodes.filter((node) => !placed.has(node.id)).map((node) => node.id);
  fillSector(orphans, { from: -Math.PI / 2, to: -Math.PI / 2 + TAU, inner: 170, place });
  return positions;
}

// ---------------------------------------------------------------------------
// Traditions — who carries what, and where two of them meet
// ---------------------------------------------------------------------------

function traditionPositions(data, ctx) {
  const positions = {};
  const place = polarPlacer(positions);

  const traditions = data.nodes.filter((node) => node.kind === "tradition");
  const members = groupBy(
    data.nodes.map((node) => node.id),
    (id) => ctx.traditionOf.get(id) ?? null,
  );
  const groups = sectors(
    traditions
      .map((node) => ({ id: node.id, ids: (members.get(node.id) ?? []).slice().sort() }))
      .sort((a, b) => b.ids.length - a.ids.length || a.id.localeCompare(b.id)),
    { floor: 3 },
  );

  // The vocabulary belongs to no tradition and goes in the middle, which is
  // also the truth of it: every sector is described in these terms. An edge
  // that leaves one sector for another without passing through the centre is a
  // claim of convergence, and this is the view that makes those visible.
  const claimed = new Set([...members.values()].flat().concat(traditions.map((node) => node.id)));
  const vocabulary = data.nodes
    .filter((node) => !claimed.has(node.id))
    .sort((a, b) => (ctx.degree.get(b.id) ?? 0) - (ctx.degree.get(a.id) ?? 0))
    .map((node) => node.id);
  const root = vocabulary.find((id) => ctx.byId.get(id)?.kind === "root");
  if (root) {
    positions[root] = { x: 0, y: 0 };
    vocabulary.splice(vocabulary.indexOf(root), 1);
  }
  // The centre is sized by what is in it, so the traditions always begin
  // outside the vocabulary rather than through it.
  const centre = fillSector(vocabulary, {
    from: -Math.PI / 2,
    to: -Math.PI / 2 + TAU,
    inner: 110,
    place,
    gap: LANDMARK_GAP,
    ring: LANDMARK_RING,
  });

  groups.forEach((group, position) => {
    // Staggered for the same reason as in the taxonomy: a tradition
    // contributing three terms earns a sliver, and two slivers side by side
    // would collide at the same radius.
    place(group.id, centre + RING_GAP + (position % 2 ? 0 : 46), (group.from + group.to) / 2);
    fillSector(group.ids, { from: group.from, to: group.to, inner: centre + RING_GAP * 3, place });
  });
  return positions;
}

// ---------------------------------------------------------------------------
// Hubs — what the graph actually hangs on
// ---------------------------------------------------------------------------

function hubPositions(data, ctx) {
  const positions = {};
  const angle = new Map();
  const place = (id, radius, value) => {
    angle.set(id, value);
    positions[id] = { x: radius * Math.cos(value), y: radius * Math.sin(value) };
  };
  const anchorOf = (id) =>
    meanAngle(ctx.neighbours.get(id).map((other) => angle.get(other)).filter((value) => value != null));

  const ranked = data.nodes
    .slice()
    .sort((a, b) => (ctx.degree.get(b.id) ?? 0) - (ctx.degree.get(a.id) ?? 0) || a.id.localeCompare(b.id));

  // The best connected term takes the centre and the rest fall outward in
  // rings, each ring holding as many as its circumference allows. Distance
  // from the middle is then readable as one thing only: how much of the corpus
  // hangs off this term. The thin edge of the graph ends up literally at the
  // edge.
  if (ranked.length) positions[ranked[0].id] = { x: 0, y: 0 };
  let index = 1;
  let radius = 140;
  while (index < ranked.length) {
    // The classes and traditions are the best connected terms and land on the
    // inner rings, where the circumference is smallest. Those rings are given
    // the room their labels need; the anonymous rings further out are not,
    // because nothing out there is being read at fitted zoom anyway.
    const look = Math.max(3, Math.floor((TAU * radius) / ITEM_GAP));
    const sample = ranked.slice(index, index + look);
    const crowded = sample.filter((node) => LANDMARKS.has(node.kind)).length > sample.length / 2;
    const capacity = Math.max(3, Math.floor((TAU * radius) / (crowded ? LANDMARK_GAP : ITEM_GAP)));
    const ring = ranked.slice(index, index + capacity).map((node) => node.id);
    placeRing(ring, radius, anchorOf, place);
    index += ring.length;
    radius += crowded ? LANDMARK_RING : RING_GAP;
  }
  return positions;
}

// ---------------------------------------------------------------------------
// Claim forms — how much of the corpus has reached which kind of statement
// ---------------------------------------------------------------------------

const BLOCK_WIDTH = 5;

function claimPositions(data, ctx) {
  const positions = {};
  // Instances group by the claim form they were written as; everything else by
  // what it is, so the vocabulary keeps its own columns instead of vanishing.
  const groups = [...groupBy(
    data.nodes.map((node) => node.id),
    (id) => ctx.classOf.get(id) ?? `kind:${ctx.byId.get(id).kind}`,
  )].map(([key, ids]) => ({ key, ids: ids.slice().sort() }))
    .sort((a, b) => b.ids.length - a.ids.length || a.key.localeCompare(b.key));

  // Blocks of a fixed width, so a block's height is its count and the
  // difference between a thickly worked claim form and a barely started one is
  // the first thing the eye gets. pm:Converging, pm:Disputing and pm:Testing
  // carry the point of the whole corpus; this is the view that says how far
  // they have got.
  // A class that heads a block is drawn once, above its own block. Without
  // this it would also be dealt into the block of classes further along and
  // the second placement would silently win, moving every heading off its
  // block.
  const headers = new Set(groups.map((group) => group.key).filter((key) => ctx.byId.has(key)));
  const blocks = groups.map((group) => {
    const header = headers.has(group.key) ? group.key : null;
    const body = group.ids.filter((id) => !headers.has(id));
    // Classes and traditions carry a label large enough to read at fitted
    // zoom, which is wider than the pitch the anonymous terms are packed at.
    // A block of them therefore gets fewer, wider columns; packed at the same
    // pitch as the rest their names would overlap at every zoom, since both
    // the type and the spacing scale together.
    const landmark = body.length > 0 && body.every((id) => LANDMARKS.has(ctx.byId.get(id).kind));
    const width = landmark ? 3 : BLOCK_WIDTH;
    return {
      header,
      body,
      width,
      spread: landmark ? 3 : 1,
      lift: landmark ? 1.7 : 1,
      columns: Math.max(1, Math.min(width, body.length)),
      rows: Math.ceil(body.length / width),
    };
  });

  // Shelved left to right and wrapped, rather than laid out in one long strip:
  // twenty blocks in a row would fit the canvas at a zoom that leaves every
  // label unreadable, which loses the comparison the view exists to make.
  const rowHeight = ITEM_GAP * 0.62;
  const spanOf = (block) => block.columns * block.spread + 1.4;
  const heightOf = (block) => block.rows * block.lift;
  const area = blocks.reduce((sum, block) => sum + spanOf(block) * (heightOf(block) + 3.4), 0);
  const shelfWidth = Math.max(BLOCK_WIDTH + 2, Math.sqrt(area * 1.6));

  let x = 0;
  let y = 0;
  let shelf = 0;
  for (const block of blocks) {
    if (x > 0 && x + spanOf(block) > shelfWidth) {
      x = 0;
      y += (shelf + 4.2) * rowHeight;
      shelf = 0;
    }
    const left = x * ITEM_GAP;
    const pitchX = ITEM_GAP * block.spread;
    const pitchY = rowHeight * block.lift;
    // Far enough above the block that the heading's own label, which hangs
    // below its node, clears the first row rather than landing in it.
    if (block.header) {
      positions[block.header] = { x: left + ((block.columns - 1) * pitchX) / 2, y: y - rowHeight * 2.7 };
    }
    block.body.forEach((id, position) => {
      positions[id] = {
        x: left + (position % block.width) * pitchX,
        y: y + Math.floor(position / block.width) * pitchY,
      };
    });
    x += spanOf(block);
    shelf = Math.max(shelf, heightOf(block));
  }
  return positions;
}

// ---------------------------------------------------------------------------
// The registry
// ---------------------------------------------------------------------------

export const VIEWS = [
  {
    id: "rings",
    name: "Rings",
    question: "What is the vocabulary made of? The root process at the centre, the classes that divide it, the properties that relate them, and everything asserted under them on the rim.",
    positions: ringPositions,
  },
  {
    id: "taxonomy",
    name: "Taxonomy",
    question: "What has been asserted under which class? Each class holds an arc of the rim in proportion to what stands under it, so the shape of the corpus is the shape of the picture.",
    positions: taxonomyPositions,
  },
  {
    id: "traditions",
    name: "Traditions",
    question: "Who carries what? One sector per tradition, sized by what it contributes, with the shared vocabulary in the middle. An edge crossing from one sector to another is a claim that two traditions meet.",
    positions: traditionPositions,
  },
  {
    id: "claims",
    name: "Claim forms",
    question: "How far has each kind of claim got? One block per claim form, a fixed five terms wide, so the height of a block is how much of the corpus has reached it.",
    positions: claimPositions,
  },
  {
    id: "hubs",
    name: "Hubs",
    question: "What does the graph hang on? The best connected term takes the centre and the rest fall outward, so distance from the middle reads as nothing but how much depends on a term.",
    positions: hubPositions,
  },
  {
    id: "force",
    name: "Force",
    question: "What clusters without being told to? The links are treated as springs and the nodes as charges; whatever settles together does so because the assertions hold it together.",
    positions: ringPositions,
    // Started from the rings rather than at random, so the same data settles
    // the same way twice and a reader can point at a cluster and find it again.
    layout: {
      name: "cose",
      randomize: false,
      animate: false,
      nodeDimensionsIncludeLabels: true,
      idealEdgeLength: 150,
      nodeOverlap: 20,
      nodeRepulsion: 45000,
      gravity: 28,
      numIter: 1600,
      componentSpacing: 160,
      nestingFactor: 0.9,
      coolingFactor: 0.95,
    },
  },
  {
    id: "matrix",
    name: "Matrix",
    question: "Where is the corpus thin? Traditions down the side, claim forms across the top, one cell per pairing. The empty cells are the finding: a node-link drawing can only show what is there.",
    matrix: true,
  },
];

export const DEFAULT_VIEW = VIEWS[0].id;

export function viewById(id) {
  return VIEWS.find((view) => view.id === id) ?? VIEWS[0];
}

/** Model-space coordinates for one view, keyed by node id. */
export function positionsFor(id, data, ctx = context(data)) {
  const view = viewById(id);
  return view.positions ? view.positions(data, ctx) : {};
}
