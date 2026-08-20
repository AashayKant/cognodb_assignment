# Graph DB Benchmark

Python benchmark harness for comparing managed graph database platforms on the same sampled social graph dataset.

The project prepares a directed edge-list dataset, loads it into configured graph databases, runs read/write workloads, writes JSON results, generates charts, and serves a small static dashboard.

## Supported Platforms

Implemented loaders:

- CognoDB Cloud: `cognodb`
- Neo4j AuraDB: `aura`
- Memgraph Cloud: `memgraph`
- FalkorDB: `falkordb`
- ArangoDB Oasis: `arango`
- TigerGraph Cloud: `tigergraph`

PuppyGraph env placeholders are included, but a PuppyGraph loader is not implemented yet.

## Setup

Clone the repo, then from the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and fill in only the platforms you want to run. Never commit `.env`.

## Environment Variables

CognoDB:

```env
COGNODB_URI=
COGNODB_PASSWORD=
COGNODB_DATABASE=
```

Neo4j AuraDB:

```env
AURA_URI=
AURA_PASSWORD=
AURA_DATABASE=
```

Memgraph:

```env
MEMGRAPH_URI=
MEMGRAPH_USER=
MEMGRAPH_PASSWORD=
MEMGRAPH_DATABASE=
```

FalkorDB:

```env
FALKORDB_DATABASE=
FALKORDB_HOST=
FALKORDB_INSTANCE_ID=
FALKORDB_PORT=
FALKORDB_USERNAME=
FALKORDB_PASSWORD=
```

ArangoDB:

```env
ARANGO_URL=
ARANGO_USER=
ARANGO_PASSWORD=
ARANGO_DB=
ARANGO_GRAPH=
ARANGO_VERTEX_COLLECTION=
ARANGO_EDGE_COLLECTION=
```

TigerGraph:

```env
TG_HOST=
TG_USERNAME=
TG_PASSWORD=
TG_GRAPHNAME=
```

## Prepare Dataset

Final benchmark dataset:

```bash
python data/prepare_dataset.py --target-edges 200000 --seed 42
```

Quick smoke-test dataset:

```bash
python data/prepare_dataset.py --target-edges 1000 --seed 42 --seed-node 0 --relationships-url https://snap.stanford.edu/data/facebook_combined.txt.gz --relationships-path facebook_combined.txt.gz
```

Generated CSV files are written to:

```text
data/nodes.csv
data/edges.csv
```

These generated files are ignored by git.

## Run Benchmarks

Run all implemented platforms:

```bash
python -m harness.runner
```

Run selected platforms:

```bash
python -m harness.runner --platforms cognodb,aura,memgraph
```

Run selected platforms without loading data again:

```bash
python -m harness.runner --platforms cognodb,aura --skip-load
```

The default workload performs 100 measured read iterations after warm-up and mixed concurrent workloads at concurrency levels 1, 10, and 40.

## Generate Charts And README

```bash
python -m harness.make_charts
python -m harness.generate_readme
```

Chart output:

```text
results/charts/traversal_latency.png
results/charts/ingest_throughput.png
results/charts/mixed_workload_qps.png
```

JSON output:

```text
results/latest.json
results/results_<UTC-timestamp>.json
results/start_nodes.json
```

Result JSON files and charts are ignored by git.

## One-Command Run

On systems with Bash:

```bash
bash scripts/run_all.sh --platforms cognodb,aura,memgraph
```

The script activates `.venv` or `venv` if present, prepares the dataset if `data/edges.csv` is missing, runs the benchmark, and generates charts.

## Results Dashboard

Serve the repo root:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8765/frontend/index.html
```

The dashboard reads `results/latest.json` and displays platform status, KPI cards, tables, and charts.

## Methodology Notes

- Dataset: SNAP soc-Pokec relationship edge list, sampled to the configured target edge count.
- Sampling: connected subgraph grown by BFS from a reproducible seed.
- Node properties: dense benchmark `id`, original SNAP user id, and synthetic `region`.
- Edge type: directed `FOLLOWS` relationship.
- Lookup index: `User.user_id_original`.
- Resource tiers: [FILL IN: instance size, region, and limits per platform].
- Footprint: [FILL IN: storage or memory footprint source per platform].

## Caveats

- Do not compare smoke-test results against final benchmark results.
- Re-running without `--skip-load` may duplicate rows or fail on duplicate keys, depending on the platform.
- TigerGraph is schema-first, so setup differs from ad hoc Cypher/AQL inserts.
- FalkorDB needs a real host endpoint; an instance id alone may not be resolvable.
- PuppyGraph is listed in `.env.example` but does not have a loader yet.
