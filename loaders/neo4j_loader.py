"""Neo4j AuraDB loader for Cypher ingest."""

from __future__ import annotations

import argparse

from loaders.base_loader import BoltLoaderMixin, GraphLoader


class Neo4jLoader(BoltLoaderMixin, GraphLoader):
    """Load benchmark data into Neo4j AuraDB using the official Neo4j driver."""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(
            {
                "platform": "aura",
                "env": {
                    "uri": "AURA_URI",
                    "password": "AURA_PASSWORD",
                    "database": "AURA_DATABASE",
                },
                **(config or {}),
            }
        )
        self.connection["user"] = "neo4j"


def main() -> None:
    """Run Neo4j AuraDB loading from the command line."""
    parser = argparse.ArgumentParser(description="Load CSV benchmark data into AuraDB.")
    parser.add_argument("nodes_csv_path")
    parser.add_argument("edges_csv_path")
    args = parser.parse_args()

    loader = Neo4jLoader()
    try:
        loader.connect()
        loader.create_indexes()
        print(loader.load_nodes(args.nodes_csv_path))
        print(loader.load_edges(args.edges_csv_path))
    finally:
        loader.close()


if __name__ == "__main__":
    main()
