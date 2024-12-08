let currentPasswords = [];
let selectedPasswordId = null;

// Load passwords from API
async function loadPasswords() {
    try {
        const response = await fetch('/homepass/get_passwords', {
        });
        
        if (!response.ok) throw new Error('Failed to load passwords');
        
        currentPasswords = await response.json();
        renderPasswordList();
    } catch (error) {
        console.error('Error loading passwords:', error);
    }
}

// Render password list
function renderPasswordList() {
    const listElement = document.getElementById('passwordList');
    listElement.innerHTML = currentPasswords.map(pass => `
        <div class="password-item ${pass.id === selectedPasswordId ? 'active' : ''}"
             onclick="selectPassword(${pass.id})">
            ${pass.name}
        </div>
    `).join('');
}

// Select password
function selectPassword(id) {
    selectedPasswordId = id;
    const password = currentPasswords.find(p => p.id === id);
    if (password) {
        document.getElementById('nameInput').value = password.name;
        document.getElementById('loginInput').value = password.login;
        document.getElementById('urlInput').value = password.url;
        document.getElementById('passwordInput').value = password.password;
        document.getElementById('passwordInput').type = 'password';
    }
    renderPasswordList();
}

// Отображение видимости пароля
function togglePassword() {
    const passwordInput = document.getElementById('passwordInput');
    const showBtn = document.querySelector('.show-btn');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showBtn.textContent = 'Скрыть';
    } else {
        passwordInput.type = 'password';
        showBtn.textContent = 'Показать';
    }
}

// Скопировать пароль в буфер обмена
function copyToClipboard() {
    const passwordInput = document.getElementById('passwordInput');
    passwordInput.type = 'text';
    navigator.clipboard.writeText(passwordInput.value);
    passwordInput.type = 'password';
}

function toggleNewPassword() {
    const passwordInput = document.getElementById('newPassword');
    const showBtn = passwordInput.nextElementSibling;
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showBtn.textContent = 'Hide';
    } else {
        passwordInput.type = 'password';
        showBtn.textContent = 'Show';
    }
}

// Функции модального окна
function showAddModal() {
    document.getElementById('addModal').classList.add('active');
}

function hideAddModal() {
    document.getElementById('addModal').classList.remove('active');
    document.getElementById('addPasswordForm').reset();
}


// Обработчик добавления пароля
async function handleAddPassword(event) {
    event.preventDefault();

    const newPassword = {
        name: document.getElementById('newName').value,
        login: document.getElementById('newLogin').value,
        url: document.getElementById('newUrl').value,
        password: document.getElementById('newPassword').value
    };

    try {
        const response = await fetch('/homepass/add_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newPassword)
        });

        if (!response.ok) throw new Error('Failed to add password');

        await loadPasswords();
        hideAddModal();
    } catch (error) {
        console.error('Error adding password:', error);
    }
}

// Edit password
async function editPassword() {
    if (!selectedPasswordId) return;
    
    const updatePassword = {
        id: selectedPasswordId,
        name: document.getElementById('nameInput').value,
        login: document.getElementById('loginInput').value,
        url: document.getElementById('urlInput').value,
        password: document.getElementById('passwordInput').value
    };

    try {
        const response = await fetch('/homepass/update_password_data', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatePassword)
        });

        if (!response.ok) throw new Error('Failed to update password');

        await loadPasswords();
    } catch (error) {
        console.error('Error updating password:', error);
    }
}
// Delete password
async function deletePassword() {
    if (!selectedPasswordId) return;
    const deletePassword = {
        id: selectedPasswordId
    };
    if (confirm('Вы уверены что желаете удалить пароль?')) {
        try {
            const response = await fetch(`/homepass/delete_password`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(deletePassword)
            });

            if (!response.ok) throw new Error('Failed to delete password');

            await loadPasswords();
            selectedPasswordId = null;
            document.getElementById('nameInput').value = '';
            document.getElementById('loginInput').value = '';
            document.getElementById('urlInput').value = '';
            document.getElementById('passwordInput').value = '';
            document.getElementById('passwordInput').type = 'password';
        } catch (error) {
            console.error('Error deleting password:', error);
        }
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', loadPasswords);