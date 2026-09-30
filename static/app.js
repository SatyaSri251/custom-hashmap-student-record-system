let allStudents = [];

document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => showSection(btn.dataset.section));
});

function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.toggle("active", b.dataset.section === id));
    const titles = {
        dashboard: "Student Record Dashboard",
        students: "Student Records",
        hashmap: "Hash Table Visualization",
        about: "How It Works"
    };
    document.getElementById("pageTitle").textContent = titles[id];
    if (id === "hashmap") loadBuckets();
}

async function loadStudents() {
    const res = await fetch("/api/students");
    const data = await res.json();
    allStudents = data.students;
    document.getElementById("statStudents").textContent = data.size;
    document.getElementById("statCapacity").textContent = data.capacity;
    document.getElementById("statLoad").textContent = Math.round(data.load_factor * 100) + "%";
    renderStudents(allStudents);
    renderBuckets(data.buckets);
}

function renderStudents(records) {
    const body = document.getElementById("studentTable");
    const empty = document.getElementById("emptyState");
    body.innerHTML = "";
    empty.style.display = records.length ? "none" : "block";

    records.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${esc(s.student_id)}</td>
            <td>${esc(s.name)}</td>
            <td>${s.age}</td>
            <td>${esc(s.course)}</td>
            <td>${Number(s.marks).toFixed(1)}</td>
            <td><button class="delete-btn" onclick="deleteStudent('${escAttr(s.student_id)}')">Delete</button></td>
        `;
        body.appendChild(tr);
    });
}

function searchStudent() {
    const q = document.getElementById("searchId").value.trim().toLowerCase();
    renderStudents(allStudents.filter(s => s.student_id.toLowerCase().includes(q)));
}

function renderBuckets(buckets) {
    const container = document.getElementById("buckets");
    container.innerHTML = "";
    buckets.forEach(bucket => {
        const div = document.createElement("div");
        div.className = "bucket";
        let content = `<div class="bucket-title">BUCKET ${bucket.index}</div>`;
        if (!bucket.entries.length) {
            content += `<span style="font-size:10px;color:#a6adbb">Empty</span>`;
        } else {
            bucket.entries.forEach((entry, i) => {
                if (i > 0) content += `<span class="arrow">→</span>`;
                content += `<span class="node">${esc(entry.key)} · ${esc(entry.name)}</span>`;
            });
        }
        div.innerHTML = content;
        container.appendChild(div);
    });
}

async function loadBuckets() {
    const res = await fetch("/api/students");
    const data = await res.json();
    renderBuckets(data.buckets);
}

async function deleteStudent(id) {
    if (!confirm(`Delete ${id}?`)) return;
    const res = await fetch(`/api/students/${encodeURIComponent(id)}`, {method:"DELETE"});
    const data = await res.json();
    if (!res.ok) return toast(data.error);
    toast(data.message);
    loadStudents();
}

function openModal() {
    document.getElementById("modal").classList.add("show");
    document.getElementById("studentForm").reset();
    document.getElementById("formMessage").innerHTML = "";
}
function closeModal(){ document.getElementById("modal").classList.remove("show"); }

document.getElementById("studentForm").addEventListener("submit", async e => {
    e.preventDefault();
    const form = new FormData(e.target);
    const payload = Object.fromEntries(form.entries());
    const res = await fetch("/api/students", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
        document.getElementById("formMessage").innerHTML = `<div class="error">${esc(data.error)}</div>`;
        return;
    }
    closeModal();
    toast(data.message);
    await loadStudents();
    showSection("students");
});

async function runHashDemo() {
    const key = document.getElementById("hashKey").value.trim();
    if (!key) return toast("Enter a student ID first.");
    const res = await fetch("/api/hash-demo", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({student_id:key})
    });
    const data = await res.json();
    if (!res.ok) return toast(data.error);

    const steps = data.steps.map((s, i) =>
        `<span class="step">${i+1}. '${esc(s.character)}' (${s.ascii}) → ${s.result}</span>`
    ).join("");
    document.getElementById("hashResult").innerHTML = `
        <div style="margin-bottom:8px;font-size:12px"><b>${esc(data.key)}</b> maps to <b>Bucket ${data.bucket}</b> of ${data.capacity}</div>
        <div class="step-row">${steps}</div>
        <p style="font-size:10px;color:#8992a7">${esc(data.collision_handling)}</p>
    `;
}

function toast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.style.display = "block";
    setTimeout(()=>t.style.display="none", 2400);
}
function esc(v) {
    return String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function escAttr(v){return String(v).replace(/'/g,"\\'")}

loadStudents();
