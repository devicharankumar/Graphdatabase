const API_BASE = window.location.origin; // same host as backend
// Simple router by hash
const app = document.getElementById('app');

document.getElementById('link-home').addEventListener('click', e => { e.preventDefault(); navigate('/'); });
document.getElementById('link-jobs').addEventListener('click', e => { e.preventDefault(); navigate('/jobs'); });
document.getElementById('link-mentorship').addEventListener('click', e => { e.preventDefault(); navigate('/mentorship'); });

function navigate(path){
  window.history.pushState({}, '', path);
  renderRoute(path);
}

window.onpopstate = () => renderRoute(window.location.pathname);

function renderRoute(path){
  if(path === '/jobs'){
    renderJobs();
  } else if (path === '/mentorship'){
    renderMentorship();
  } else {
    renderHome();
  }
}

// ---------- Home
function renderHome(){
  app.innerHTML = `
    <div class="grid">
      <div>
        <div class="card">
          <h2>Welcome to LinkNITT</h2>
          <p class="small">A lightweight static frontend for demoing your FastAPI + Neo4j backend (no Node required).</p>
        </div>

        <div class="card">
          <h3>Create demo user</h3>
          <div class="form-row"><input id="u_person_id" class="input" placeholder="person_id (e.g. U100)"></div>
          <div class="form-row"><input id="u_name" class="input" placeholder="Full name"></div>
          <div class="form-row"><input id="u_email" class="input" placeholder="email"></div>
          <div class="form-row"><input id="u_dept" class="input" placeholder="dept"></div>
          <div class="form-row"><input id="u_role" class="input" placeholder="role (Student/Faculty/Alumni)"></div>
          <div><button id="create-user" class="btn">Create User</button></div>
          <div id="create-user-msg" class="small" style="margin-top:8px"></div>
        </div>
      </div>

      <aside>
        <div class="card">
          <h4>Quick actions</h4>
          <button id="seed-btn" class="btn">Seed DB (server-side)</button>
          <p class="small" style="margin-top:8px">If seed script is present, use backend endpoint to trigger it (or run seed_db.py manually).</p>
        </div>
      </aside>
    </div>
  `;

  document.getElementById('create-user').onclick = async () => {
    const payload = {
      person_id: document.getElementById('u_person_id').value || `U${Date.now()}`,
      name: document.getElementById('u_name').value || 'Demo User',
      email: document.getElementById('u_email').value || `demo${Date.now()}@nitt.edu`,
      role: document.getElementById('u_role').value || 'Student',
      dept: document.getElementById('u_dept').value || 'CA',
    };
    try {
      const res = await fetch(API_BASE + '/users', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      document.getElementById('create-user-msg').textContent = data.status ? 'User created' : JSON.stringify(data);
    } catch(e){
      document.getElementById('create-user-msg').textContent = 'Error: ' + e.message;
    }
  };

  document.getElementById('seed-btn').onclick = async () => {
    try {
      const res = await fetch(API_BASE + '/seed', { method: 'POST' });
      const txt = await res.text();
      alert('Seed: ' + txt);
    } catch(e) { alert('Seed failed: ' + e.message); }
  };
}

// ---------- Jobs page
async function renderJobs(){
  app.innerHTML = `
    <div>
      <div class="card">
        <h2>Jobs</h2>
        <div style="margin-top:8px">
          <button id="new-job-btn" class="btn">New Job</button>
        </div>
        <div id="jobs-area" style="margin-top: 12px"></div>
      </div>
    </div>
  `;

  document.getElementById('new-job-btn').onclick = async () => {
    const title = prompt('Job title'); if(!title) return;
    const description = prompt('Description') || '';
    const fac_id = prompt('Faculty Id');
    const job = {
      job_id: 'J' + Date.now(),
      title, description,
      posted_by: fac_id , type: 'Part-time', compensation: 0
    };
    await fetch(API_BASE + '/jobs', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(job)
    });
    await loadJobs();
  };

  await loadJobs();
}

async function loadJobs(){
  const jobsArea = document.getElementById('jobs-area');
  jobsArea.innerHTML = 'Loading ...';
  try {
    const res = await fetch(API_BASE + '/jobs/'); // ✅ trailing slash
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`HTTP ${res.status}: ${text.slice(0, 100)}`);
    }

    const data = await res.json();
    const jobs = data.jobs || [];
    if(jobs.length === 0) jobsArea.innerHTML = '<div class="small">No jobs yet</div>';
    else {
      jobsArea.innerHTML = jobs.map(j => {
        const job = j.j || j;
        return `<div class="job card"><strong>${job.title}</strong><div class="small">${job.description}</div></div>`;
      }).join('');
    }
  } catch(e) { 
    jobsArea.innerHTML = 'Error: ' + e.message; 
    console.error("Load jobs failed:", e);
  }
}

// ---------- Mentorship page
function renderMentorship(){
  app.innerHTML = `
    <div>
      <div class="card">
        <h2>Mentorship Requests</h2>
        <form id="ment-form">
          <div class="form-row"><input id="m_student" class="input" placeholder="student_id (e.g. S101)"></div>
          <div class="form-row"><input id="m_mentor" class="input" placeholder="mentor_id (e.g. U001)"></div>
          <div class="form-row"><input id="m_topic" class="input" placeholder="topic"></div>
          <div><button class="btn" type="submit">Request Mentor</button></div>
        </form>
        <div id="ment-msg" class="small" style="margin-top:10px"></div>
      </div>
    </div>
  `;

  document.getElementById('ment-form').onsubmit = async (e) => {
    e.preventDefault();
    const payload = {
      request_id: 'R' + Date.now(),
      student_id: document.getElementById('m_student').value || 'S101',
      mentor_id: document.getElementById('m_mentor').value || 'U001',
      topic: document.getElementById('m_topic').value || 'General',
      status: 'Pending'
    };
    try {
      const res = await fetch(API_BASE + '/mentorship', {
        method:'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
      });
      const data = await res.json();
      document.getElementById('ment-msg').textContent = data.status ? 'Request created' : JSON.stringify(data);
    } catch(err) { document.getElementById('ment-msg').textContent = 'Error: '+err.message; }
  };
}

// start
renderRoute(window.location.pathname);
