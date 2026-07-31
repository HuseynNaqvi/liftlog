const registerForm = document.querySelector('#register-form');
const loginForm = document.querySelector('#login-form');
const usernameInput = document.querySelector('#username');
const emailInput = document.querySelector('#email');
const passwordInput = document.querySelector('#password');
const logoutBtn = document.querySelector('#logout-btn');
const splitForm = document.querySelector('#split-form');
const splitNameInput = document.querySelector('#split-name');
const splitsList = document.querySelector('#splits-list');
const entryForm = document.querySelector('#entry-form');
const exerciseInput = document.querySelector('#exercise');
const weightInput = document.querySelector('#weight');
const repsInput = document.querySelector('#reps');
const setsInput = document.querySelector('#sets');
const entriesList = document.querySelector('#entries-list');
const suggestionForm = document.querySelector('#suggestion-form');
const suggestionExerciseInput = document.querySelector('#suggestion-exercise');
const suggestionResult = document.querySelector('#suggestion-result');
const openSuggestionBtn = document.querySelector('#open-suggestion-btn');
const suggestionModalOverlay = document.querySelector('#suggestion-modal-overlay');
const closeSuggestionBtn = document.querySelector('#close-suggestion-btn');

if (window.location.pathname.includes('index.html')) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }
}

if (registerForm) {
    registerForm.addEventListener('submit', async(e)=>{
        e.preventDefault();  
        const username = usernameInput.value;
        const email = emailInput.value;
        const password = passwordInput.value;

        const response = await fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });

        if (response.ok) {
            window.location.href = 'login.html';
        } else {
            const errorData = await response.json();
            alert(errorData.detail);
        }
    })
}

if(loginForm){
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = usernameInput.value;
        const password = passwordInput.value;

        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert(errorData.detail);
        }
    });
}

if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = 'login.html';
    });
}

if (entryForm) {
    entryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        const exercise = exerciseInput.value;
        const weight = weightInput.value;
        const reps = repsInput.value;
        const sets = setsInput.value;

        const response = await fetch('http://127.0.0.1:8000/entries', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                exercise,
                weight: parseFloat(weightInput.value),
                reps: parseInt(repsInput.value),
                sets: parseInt(setsInput.value)
            })
        });

        if (response.ok) {
            entryForm.reset();
            loadEntries();
        } else {
            const errorData = await response.json();
            alert(errorData.detail);
        }
    });
}

async function loadEntries() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://127.0.0.1:8000/entries', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const entries = await response.json();

    entriesList.innerHTML = entries.map(entry => `
        <div class="entry-item">
            ${entry.exercise} — ${entry.weight}kg × ${entry.reps} reps × ${entry.sets} sets
            <button class="delete-btn" data-id="${entry.id}">Delete</button>
        </div>
    `).join('');

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            await fetch(`http://127.0.0.1:8000/entries/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            loadEntries();
        });
    });
}

if (entriesList) {
    loadEntries();
}

async function loadSplits() {
    const token = localStorage.getItem('token');
    const response = await fetch('http://127.0.0.1:8000/splits', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const splits = await response.json();

    splitsList.innerHTML = splits.map(split => `
        <div class="split-item">
            ${split.name}
            <button class="delete-split-btn" data-id="${split.id}">Delete</button>
        </div>
    `).join('');

    document.querySelectorAll('.delete-split-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const id = btn.dataset.id;
            await fetch(`http://127.0.0.1:8000/splits/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            loadSplits();
        });
    });
}

if (splitsList) {
    loadSplits();
}

if (splitForm) {
    splitForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        const name = splitNameInput.value;

        const response = await fetch('http://127.0.0.1:8000/splits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });

        if (response.ok) {
            splitForm.reset();
            loadSplits();
        } else {
            const errorData = await response.json();
            alert(errorData.detail);
        }
    });
}

if (suggestionForm) {
    suggestionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        const exercise = suggestionExerciseInput.value;

        const response = await fetch(`http://127.0.0.1:8000/entries/${exercise}/suggestion`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            suggestionResult.innerText = data.suggestion;
        } else {
            const errorData = await response.json();
            alert(errorData.detail);
        }
    });
}

if (openSuggestionBtn) {
    openSuggestionBtn.addEventListener('click', () => {
        suggestionModalOverlay.classList.remove('hidden');
    });
}

if (closeSuggestionBtn) {
    closeSuggestionBtn.addEventListener('click', () => {
        suggestionModalOverlay.classList.add('hidden');
    });
}

if (suggestionModalOverlay) {
    suggestionModalOverlay.addEventListener('click', (e) => {
        if (e.target === suggestionModalOverlay) {
            suggestionModalOverlay.classList.add('hidden');
        }
    });
}