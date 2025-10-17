from app.db.neo4j_client import db  # make sure your Neo4j client is properly imported

def seed_users():
    users = [
        {"person_id": "U001", "name": "Dr. Ramesh Kumar", "email": "ramesh@nitt.edu", "role": "Faculty", "batch": None},
        {"person_id": "S101", "name": "Ananya Sharma", "email": "ananya@student.nitt.edu", "role": "Student", "batch": 2024},
        {"person_id": "A201", "name": "Alumni Rahul", "email": "rahul@alumni.nitt.edu", "role": "Alumni", "batch": 2018},
    ]
    for u in users:
        q = """
        MERGE (p:Person {person_id:$person_id})
        SET p.name=$name, p.email=$email, p.role=$role, p.batch=$batch
        """
        db.query(q, u)
    print("✅ Users seeded")

def seed_jobs():
    jobs = [
        {"job_id": "J001", "title": "Part-time Research Assistant", "description": "Work on thermal systems project.", "posted_by": "U001", "type": "Part-time", "compensation": 8000},
        {"job_id": "J002", "title": "Club Designer", "description": "Create posters for EEE club.", "posted_by": "S101", "type": "Freelance", "compensation": 1000},
    ]
    for j in jobs:
        q = """
        MERGE (j:Job {job_id:$job_id})
        SET j.title=$title, j.description=$description, j.posted_by=$posted_by, j.type=$type, j.compensation=$compensation
        WITH j
        MATCH (p:Person {person_id:$posted_by})
        MERGE (p)-[:OFFERS]->(j)
        """
        db.query(q, j)
    print("✅ Jobs seeded")

def seed_mentorship():
    mentorships = [
        {"request_id": "R001", "student_id": "S101", "mentor_id": "U001", "topic": "Renewable Energy Research", "status": "Pending"},
        {"request_id": "R002", "student_id": "S101", "mentor_id": "A201", "topic": "Career Guidance", "status": "Pending"},
    ]
    for m in mentorships:
        q = """
        MERGE (r:MentorshipRequest {request_id:$request_id})
        SET r.topic=$topic, r.status=$status
        WITH r
        MATCH (s:Person {person_id:$student_id})
        MATCH (m:Person {person_id:$mentor_id})
        MERGE (s)-[:REQUESTS_MENTORSHIP]->(r)
        MERGE (m)-[:RECEIVES_REQUEST]->(r)
        """
        db.query(q, m)
    print("✅ Mentorship requests seeded")

if __name__ == "__main__":
    seed_users()
    seed_jobs()
    seed_mentorship()
    print("🎉 Database seeding complete!")
