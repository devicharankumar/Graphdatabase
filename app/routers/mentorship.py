from fastapi import APIRouter
from app.db.neo4j_client import db
from pydantic import BaseModel

router = APIRouter(prefix="/mentorship", tags=["Mentorship"])

class MentorshipRequest(BaseModel):
    request_id: str
    student_id: str
    mentor_id: str
    topic: str
    status: str = "Pending"

@router.post("")
def create_request(req: MentorshipRequest):
    q = """
    MERGE (s:Person {person_id:$student_id})
    MERGE (m:Person {person_id:$mentor_id})
    MERGE (r:MentorshipRequest {request_id:$request_id, topic:$topic, status:$status})
    MERGE (s)-[:REQUESTS_MENTORSHIP]->(r)
    MERGE (m)-[:RECEIVES_REQUEST]->(r)
    RETURN r
    """
    res = db.query(q, req.dict())
    return {"status": "created", "request": res}

@router.get("/")
def get_all_requests():
    q = "MATCH (r:MentorshipRequest) RETURN r"
    res = db.query(q)
    return {"requests": res}
