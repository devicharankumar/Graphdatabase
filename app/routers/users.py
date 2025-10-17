from fastapi import APIRouter
from app.db.neo4j_client import db
from app.models.schemas import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("")
def create_user(user: User):
    q = """
    MERGE (p:Person {person_id:$person_id})
    SET p.name=$name, p.email=$email, p.role=$role, p.dept=$dept, p.batch=$batch
    RETURN p
    """
    res = db.query(q, user.dict())
    return {"status": "success", "user": res}

@router.get("/")
def get_all_users():
    q = "MATCH (p:Person) RETURN p LIMIT 25"
    res = db.query(q)
    return {"users": res}
