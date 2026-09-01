// The one view that is not a drawing of the graph.
//
// A node-link picture can only show what is there. Lay the traditions against
// the claim forms instead and the empty cells become the finding: this
// tradition has been read for what it says a practice yields, that one has not
// been read for anything but its concepts, and the column that carries the
// point of the whole corpus is nearly bare. That is a fact about the state of
// the work, and no arrangement of dots and lines states it.

const local = (curie) => curie.split(":").pop();

// The row for claims that belong to no single tradition.
export const ACROSS = "across";

// The row and column for a tradition neither scale was applied to.
export const UNSTATED = "unstated";

/**
 * Cross-tabulate traditions against claim forms.
 *
 * Columns are the classes instantiated by the material itself, never the
 * controlled vocabularies: pm:textualAttestation is an instance of pm:Attesting
 * but it is a term of the ontology, not a claim anyone made from a tradition,
 * and counting it would put a column of scaffolding beside the columns of work.
 *
 * The last row holds claims made across traditions rather than within one —
 * convergences and disputes belong to no single sector, and dropping them
 * would understate exactly the work the corpus exists for.
 */
export function crosstab(data, ctx) {
  const isVocabulary = (id) => id.startsWith("pm:");
  const claims = data.nodes.filter(
    (node) => !isVocabulary(node.id) && ctx.classOf.has(node.id) && node.kind !== "tradition",
  );

  const columnTotals = new Map();
  const rowTotals = new Map();
  const cells = new Map();
  const key = (row, column) => `${row} ${column}`;

  for (const node of claims) {
    const column = ctx.classOf.get(node.id);
    const row = ctx.traditionOf.get(node.id) ?? ACROSS;
    columnTotals.set(column, (columnTotals.get(column) ?? 0) + 1);
    rowTotals.set(row, (rowTotals.get(row) ?? 0) + 1);
    cells.set(key(row, column), (cells.get(key(row, column)) ?? 0) + 1);
  }

  const label = (id) => (id === ACROSS ? "Across traditions" : ctx.byId.get(id)?.label ?? local(id));
  const order = (ids) =>
    ids.sort((a, b) => (rowTotals.get(b) ?? 0) - (rowTotals.get(a) ?? 0) || label(a).localeCompare(label(b)));

  const columns = [...columnTotals.keys()].sort(
    (a, b) => columnTotals.get(b) - columnTotals.get(a) || label(a).localeCompare(label(b)),
  );

  // Rows are the traditions that witness. A registered transmission whose
  // corpus has only been named carries nothing by definition — pm:corpusNamed
  // says so outright — so an empty row for it would not be the finding the
  // empty cells of this table are. It would be the same statement repeated a
  // hundred and more times, and it would bury the cells that do mean
  // something: a tradition that has been read and still has nothing under a
  // claim form. Where the register stands is the register table's question,
  // and the count is carried in `registered` so the caption can say it.
  const traditions = data.nodes.filter((node) => node.kind === "tradition").map((node) => node.id);
  const rows = order(traditions.filter((id) => (rowTotals.get(id) ?? 0) > 0));
  if (rowTotals.has(ACROSS)) rows.push(ACROSS);

  return {
    rows: rows.map((id) => ({ id, label: label(id), total: rowTotals.get(id) ?? 0 })),
    columns: columns.map((id) => ({ id, label: label(id), total: columnTotals.get(id) })),
    count: (row, column) => cells.get(key(row, column)) ?? 0,
    filled: cells.size,
    total: claims.length,
    peak: Math.max(1, ...cells.values()),
    registered: traditions.length - rows.filter((id) => id !== ACROSS).length,
  };
}

/**
 * The register, cross-tabulated: coverage state against contact route.
 *
 * The claim-form table above says what the opened traditions carry. This one
 * says where the opening itself stands, and it is the table the coverage
 * vocabulary was introduced to make possible: a corpus named and unread and a
 * corpus read and genuinely thin no longer read alike, so the register becomes
 * a denominator instead of a silence.
 *
 * Contact route is the second axis rather than a footnote because it decides
 * how an agreement with these traditions may be counted. It does not decide
 * what the agreement is worth: a documented route says how a claim travelled
 * and bars counting the same statement twice, and a transmission carried that
 * way is still a finding about what was carried. A corpus with no route for
 * the period it was fixed is a candidate for independent attestation.
 */
export function registerTab(data, ctx, { coverageScale, contactScale }) {
  const traditions = data.nodes.filter((node) => node.kind === "tradition").map((node) => node.id);
  const label = (id) =>
    id === UNSTATED ? "Not stated" : ctx.byId.get(id)?.label ?? local(id);

  // The terms are read off the graph; only their order comes from the scales,
  // and a scale keeps a term nobody is in — an absent row would read as an
  // absent stage rather than as a stage nothing has reached.
  const axis = (type, scale) => {
    const present = data.nodes.filter((node) => node.types.includes(type)).map((node) => node.id);
    return [
      ...scale.filter((id) => present.includes(id)),
      ...present.filter((id) => !scale.includes(id)).sort(),
    ];
  };
  const rows = axis("pm:CoverageState", coverageScale);
  const columns = axis("pm:ContactRoute", contactScale);

  const cells = new Map();
  const rowTotals = new Map();
  const columnTotals = new Map();
  const key = (row, column) => `${row} ${column}`;
  for (const id of traditions) {
    const row = ctx.coverageOf.get(id) ?? UNSTATED;
    const column = ctx.contactOf.get(id) ?? UNSTATED;
    cells.set(key(row, column), (cells.get(key(row, column)) ?? 0) + 1);
    rowTotals.set(row, (rowTotals.get(row) ?? 0) + 1);
    columnTotals.set(column, (columnTotals.get(column) ?? 0) + 1);
  }
  // A tradition the scales were never applied to is neither a stage nor a
  // route; it is an omission, and it gets its own row and column so that it is
  // counted rather than rounded away.
  if (rowTotals.has(UNSTATED)) rows.push(UNSTATED);
  if (columnTotals.has(UNSTATED)) columns.push(UNSTATED);

  return {
    rows: rows.map((id) => ({ id, label: label(id), total: rowTotals.get(id) ?? 0 })),
    columns: columns.map((id) => ({ id, label: label(id), total: columnTotals.get(id) ?? 0 })),
    count: (row, column) => cells.get(key(row, column)) ?? 0,
    filled: cells.size,
    total: traditions.length,
    peak: Math.max(1, ...cells.values()),
  };
}


/** The query that would list exactly the terms counted in one claim-form cell. */
export function queryFor(rowId, columnId) {
  const type = columnId ? `type:${local(columnId)}` : "";
  if (rowId === ACROSS) return `${type} -has:tradition`.trim();
  const tradition = rowId ? `tradition:${local(rowId)}` : "";
  return `${tradition} ${type}`.trim();
}

/** The query that would list the traditions counted in one register cell. */
export function registerQueryFor(rowId, columnId) {
  const coverage = rowId === UNSTATED ? "-has:coverage" : rowId ? `coverage:${local(rowId)}` : "";
  const contact = columnId === UNSTATED ? "-has:contact" : columnId ? `contact:${local(columnId)}` : "";
  return `kind:tradition ${coverage} ${contact}`.replace(/\s+/g, " ").trim();
}

/**
 * Draw both cross-tabulations into a container: what the opened traditions
 * carry, and where the opening itself stands. Real tables, so a screen reader
 * reads them as the tables they are and they inherit the page's own colours
 * rather than being painted on a canvas.
 */
export function renderMatrix(container, tables, { onSelect } = {}) {
  const parts = [];
  for (const { matrix, caption, queryFor: query } of tables) {
    if (!matrix.rows.length || !matrix.columns.length) continue;
    parts.push(renderTable(matrix, caption, query, onSelect));
  }
  container.replaceChildren(...parts);
  return parts;
}

function renderTable(matrix, captionText, queryFor, onSelect) {
  const table = document.createElement("table");
  table.className = "matrix";

  const caption = document.createElement("caption");
  caption.textContent = captionText;
  table.append(caption);

  const head = document.createElement("thead");
  const headRow = document.createElement("tr");
  headRow.append(cell("td", "", { className: "matrix-corner" }));
  for (const column of matrix.columns) {
    const th = cell("th", column.label, { scope: "col" });
    th.append(countBadge(column.total));
    th.append(button(`All of ${column.label}`, () => onSelect?.(queryFor(null, column.id))));
    headRow.append(th);
  }
  headRow.append(cell("th", "all", { scope: "col", className: "matrix-total" }));
  head.append(headRow);
  table.append(head);

  const body = document.createElement("tbody");
  for (const row of matrix.rows) {
    const tr = document.createElement("tr");
    const th = cell("th", row.label, { scope: "row" });
    th.append(button(`All of ${row.label}`, () => onSelect?.(queryFor(row.id, null))));
    tr.append(th);
    for (const column of matrix.columns) {
      const count = matrix.count(row.id, column.id);
      const td = document.createElement("td");
      td.className = count ? "matrix-cell" : "matrix-cell matrix-empty";
      // Shading runs on the square root of the count: a cell with thirty-two
      // terms is not thirty-two times more worth looking at than one with one,
      // and a linear ramp would sink every small cell into the background.
      if (count) {
        const weight = 12 + 76 * Math.sqrt(count / matrix.peak);
        td.style.background = `color-mix(in oklab, var(--text) ${weight.toFixed(1)}%, var(--surface))`;
        td.style.color = weight > 52 ? "var(--bg)" : "var(--text)";
        td.textContent = String(count);
      } else {
        td.textContent = "";
      }
      td.append(
        button(
          count
            ? `${count}: ${row.label} · ${column.label}`
            : `Nothing: ${row.label} · ${column.label}`,
          () => onSelect?.(queryFor(row.id, column.id)),
        ),
      );
      tr.append(td);
    }
    tr.append(cell("td", String(row.total), { className: "matrix-total" }));
    body.append(tr);
  }
  table.append(body);
  return table;
}

function cell(tag, text, { scope, className } = {}) {
  const node = document.createElement(tag);
  if (scope) node.scope = scope;
  if (className) node.className = className;
  if (text) node.append(document.createTextNode(text));
  return node;
}

function countBadge(count) {
  const span = document.createElement("span");
  span.className = "matrix-count";
  span.textContent = String(count);
  return span;
}

/**
 * The whole cell is the control. A stretched button keeps the table a table
 * while giving every count a name a keyboard or a screen reader can reach —
 * including the empty ones, which are the cells most worth opening.
 */
function button(label, handler) {
  const control = document.createElement("button");
  control.type = "button";
  control.className = "matrix-hit";
  control.title = label;
  control.append(cell("span", label, { className: "visually-hidden" }));
  control.addEventListener("click", handler);
  return control;
}
