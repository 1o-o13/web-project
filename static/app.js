const API_BASE = "http://127.0.0.1:8000";

// ===== 페이지 로드 =====
window.addEventListener("load", async () => {
    await checkLogin();
});

// ===== 인증 =====
async function checkLogin() {
    try {
        const res = await fetch(`${API_BASE}/auth/me`, { credentials: "include" });
        if (res.ok) {
            const user = await res.json();
            showAdminPanel(user.username);
        } else {
            showLoginPanel();
        }
    } catch (e) {
        console.error("로그인 확인 오류:", e);
        showLoginPanel();
    }
}

function showLoginPanel() {
    document.getElementById("header").classList.add("hidden");
    document.getElementById("adminSection").classList.add("hidden");
    document.getElementById("loginSection").classList.remove("hidden");
}

async function showAdminPanel(username) {
    document.getElementById("header").classList.remove("hidden");
    document.getElementById("loginSection").classList.add("hidden");
    document.getElementById("adminSection").classList.remove("hidden");
    document.getElementById("username").textContent = username;

    await loadCategories();
    await loadContacts();
}

function switchTab(tab) {
    const isLogin = tab === "login";
    document.getElementById("loginTab").classList.toggle("active", isLogin);
    document.getElementById("signupTab").classList.toggle("active", !isLogin);
    document.getElementById("loginTabBtn").classList.toggle("active", isLogin);
    document.getElementById("signupTabBtn").classList.toggle("active", !isLogin);
    clearAlerts();
}

async function signup() {
    const username = document.getElementById("signupUsername").value;
    const password = document.getElementById("signupPassword").value;
    const alert = document.getElementById("signupAlert");

    if (!username || !password) {
        showAlert(alert, "모든 항목을 입력하세요", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
            credentials: "include"
        });

        if (res.ok) {
            showAlert(alert, "가입 완료! 로그인해주세요", "success");
            document.getElementById("signupUsername").value = "";
            document.getElementById("signupPassword").value = "";
            setTimeout(() => switchTab("login"), 1500);
        } else {
            const err = await res.json();
            showAlert(alert, err.detail || "가입 실패", "error");
        }
    } catch (e) {
        showAlert(alert, "네트워크 오류: " + e.message, "error");
    }
}

async function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    const alert = document.getElementById("loginAlert");

    if (!username || !password) {
        showAlert(alert, "아이디와 비밀번호를 입력하세요", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
            credentials: "include"
        });

        if (res.ok) {
            document.getElementById("loginUsername").value = "";
            document.getElementById("loginPassword").value = "";
            await checkLogin();
        } else {
            const err = await res.json();
            showAlert(alert, err.detail || "로그인 실패", "error");
        }
    } catch (e) {
        showAlert(alert, "네트워크 오류: " + e.message, "error");
    }
}

async function logout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: "POST",
            credentials: "include"
        });
    } catch (e) {
        console.error("로그아웃 오류:", e);
    }
    await checkLogin();
}

async function showMyInfo() {
    try {
        const res = await fetch(`${API_BASE}/auth/me`, { credentials: "include" });
        if (res.ok) {
            const user = await res.json();
            const createdDate = new Date(user.created_at).toLocaleString('ko-KR');
            alert(`📋 내 정보\n\n아이디: ${user.username}\n가입일: ${createdDate}`);
        } else {
            showAlert(document.getElementById("globalAlert"), "내정보를 불러올 수 없습니다", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

// ===== 카테고리 관리 =====
async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE}/categories`, { credentials: "include" });
        if (res.ok) {
            const categories = await res.json();
            updateCategoryTable(categories);
            updateCategorySelects(categories);
        }
    } catch (e) {
        console.error("카테고리 로드 오류:", e);
    }
}

function updateCategoryTable(categories) {
    const tbody = document.querySelector("#categoryTable tbody");
    tbody.innerHTML = categories.map(cat => `
        <tr>
            <td>${escapeHtml(cat.name)}</td>
            <td>
                <button onclick="editCategory(${cat.id}, '${escapeHtml(cat.name)}')">수정</button>
                <button class="danger" onclick="deleteCategory(${cat.id})">삭제</button>
            </td>
        </tr>
    `).join("");
}

function updateCategorySelects(categories) {
    const contactSelect = document.getElementById("contactCategory");
    const filterSelect = document.getElementById("filterCategory");

    const html = categories.map(cat => `<option value="${cat.id}">${escapeHtml(cat.name)}</option>`).join("");
    contactSelect.innerHTML = html;
    filterSelect.innerHTML = `<option value="">종류 전체</option>${html}`;
}

async function addCategory() {
    const name = document.getElementById("newCategoryName").value;
    if (!name) {
        showAlert(document.getElementById("globalAlert"), "카테고리 이름을 입력하세요", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/categories`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
            credentials: "include"
        });

        if (res.ok) {
            document.getElementById("newCategoryName").value = "";
            showAlert(document.getElementById("globalAlert"), "카테고리가 추가되었습니다", "success");
            await loadCategories();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "추가 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

async function editCategory(id, oldName) {
    const newName = prompt(`카테고리 이름 수정 (현재: ${oldName}):`);
    if (!newName || newName === oldName) return;

    try {
        const res = await fetch(`${API_BASE}/categories/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName }),
            credentials: "include"
        });

        if (res.ok) {
            showAlert(document.getElementById("globalAlert"), "카테고리가 수정되었습니다", "success");
            await loadCategories();
            await loadContacts();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "수정 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

async function deleteCategory(id) {
    if (!confirm("정말 삭제하시겠습니까?")) return;

    try {
        const res = await fetch(`${API_BASE}/categories/${id}`, {
            method: "DELETE",
            credentials: "include"
        });

        if (res.ok || res.status === 204) {
            showAlert(document.getElementById("globalAlert"), "카테고리가 삭제되었습니다", "success");
            await loadCategories();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "삭제 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

// ===== 연락처 관리 =====
async function loadContacts(name = null, categoryId = null) {
    try {
        let url = `${API_BASE}/contacts`;
        const params = new URLSearchParams();
        if (name) params.append("name", name);
        if (categoryId) params.append("category_id", categoryId);
        if (params.toString()) url += "?" + params;

        const res = await fetch(url, { credentials: "include" });
        if (res.ok) {
            const data = await res.json();
            updateContactTable(data.items);
            document.getElementById("totalCount").textContent = data.total;
        }
    } catch (e) {
        console.error("연락처 로드 오류:", e);
    }
}

function updateContactTable(contacts) {
    const tbody = document.querySelector("#contactTable tbody");
    tbody.innerHTML = contacts.map(c => `
        <tr>
            <td>${escapeHtml(c.name)}</td>
            <td>${escapeHtml(c.phone)}</td>
            <td>${escapeHtml(c.addr)}</td>
            <td>${escapeHtml(c.category_name)}</td>
            <td>
                <button onclick="editContact(${c.id})">수정</button>
                <button class="danger" onclick="deleteContact(${c.id})">삭제</button>
            </td>
        </tr>
    `).join("");
}

async function addContact() {
    const name = document.getElementById("contactName").value;
    const phone = document.getElementById("contactPhone").value;
    const addr = document.getElementById("contactAddr").value;
    const categoryId = parseInt(document.getElementById("contactCategory").value);

    if (!name || !phone || !categoryId) {
        showAlert(document.getElementById("globalAlert"), "필수 항목을 입력하세요", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/contacts`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, phone, addr, category_id: categoryId }),
            credentials: "include"
        });

        if (res.ok || res.status === 201) {
            document.getElementById("contactName").value = "";
            document.getElementById("contactPhone").value = "";
            document.getElementById("contactAddr").value = "";
            showAlert(document.getElementById("globalAlert"), "연락처가 추가되었습니다", "success");
            await loadContacts();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "추가 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

async function editContact(id) {
    const contact = (await fetch(`${API_BASE}/contacts`, { credentials: "include" }).then(r => r.json())).items.find(c => c.id === id);
    if (!contact) {
        showAlert(document.getElementById("globalAlert"), "연락처를 찾을 수 없습니다", "error");
        return;
    }

    const newName = prompt(`이름 (현재: ${contact.name}):`, contact.name);
    if (newName === null || newName === contact.name) return;

    const newPhone = prompt(`전화번호 (현재: ${contact.phone}):`, contact.phone);
    if (newPhone === null || newPhone === contact.phone) {
        if (newName === contact.name) return;
    }

    const newAddr = prompt(`주소 (현재: ${contact.addr}):`, contact.addr);
    if (newAddr === null) return;

    try {
        const updateData = {};
        if (newName && newName !== contact.name) updateData.name = newName;
        if (newPhone && newPhone !== contact.phone) updateData.phone = newPhone;
        if (newAddr !== undefined) updateData.addr = newAddr;

        const res = await fetch(`${API_BASE}/contacts/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updateData),
            credentials: "include"
        });

        if (res.ok) {
            showAlert(document.getElementById("globalAlert"), "연락처가 수정되었습니다", "success");
            await loadContacts();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "수정 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

async function deleteContact(id) {
    if (!confirm("정말 삭제하시겠습니까?")) return;

    try {
        const res = await fetch(`${API_BASE}/contacts/${id}`, {
            method: "DELETE",
            credentials: "include"
        });

        if (res.ok || res.status === 204) {
            showAlert(document.getElementById("globalAlert"), "연락처가 삭제되었습니다", "success");
            await loadContacts();
        } else {
            const err = await res.json();
            showAlert(document.getElementById("globalAlert"), err.detail || "삭제 실패", "error");
        }
    } catch (e) {
        showAlert(document.getElementById("globalAlert"), "네트워크 오류: " + e.message, "error");
    }
}

function searchContacts() {
    const name = document.getElementById("searchName").value || null;
    loadContacts(name);
}

function filterByCategory() {
    const categoryId = document.getElementById("filterCategory").value || null;
    loadContacts(null, categoryId ? parseInt(categoryId) : null);
}

// ===== 유틸리티 =====
function showAlert(element, message, type) {
    element.textContent = message;
    element.className = `alert ${type}`;
    element.style.display = "block";
}

function clearAlerts() {
    document.querySelectorAll(".alert").forEach(el => {
        el.style.display = "none";
    });
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
