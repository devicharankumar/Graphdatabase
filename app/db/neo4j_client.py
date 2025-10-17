from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jConnection:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASS)
            )
            print("✅ Connected to Neo4j at", settings.NEO4J_URI)
        except Exception as e:
            print("❌ Neo4j connection failed:", e)

    def query(self, cypher_query, params=None):
        with self.driver.session() as session:
            result = session.run(cypher_query, params or {})
            return [r.data() for r in result]

    def close(self):
        self.driver.close()

# Create a shared connection object
db = Neo4jConnection()
