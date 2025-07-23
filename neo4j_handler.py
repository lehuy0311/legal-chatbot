# neo4j_handler.py

from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, cypher_query, parameters=None):
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters)
            return [record.data() for record in result]

    def get_context_from_law(self, question):
        import re
        match = re.search(r"điều\s*(\d+)", question.lower())
        if match:
            so_dieu = f"Điều {match.group(1)}"
            query = """
            MATCH (d:Dieu_Luat)
            WHERE d.name = $name
            RETURN d.name AS name, d.content AS content
            LIMIT 1
            """
            result = self.query(query, {"name": so_dieu})
            if result:
                return f"{result[0]['name']}: {result[0]['content']}"
        return "Không tìm thấy thông tin phù hợp trong cơ sở dữ liệu luật."
