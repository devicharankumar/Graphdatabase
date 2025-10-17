from fastapi import APIRouter
from app.db.neo4j_client import db
from app.models.schemas import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("")
def create_job(job: Job):
    q = """
    MERGE (j:Job {job_id:$job_id})
    SET j.title=$title, j.description=$description, j.type=$type, j.compensation=$compensation
    WITH j
    MATCH (p:Person {person_id:$posted_by})
    MERGE (p)-[:OFFERS]->(j)
    RETURN j
    """
    res = db.query(q, job.dict())
    return {"status": "success", "job": res}

@router.get("/")
def get_all_jobs():
    q = "MATCH (j:Job) RETURN j LIMIT 25"
    res = db.query(q)
    return {"jobs": res}
