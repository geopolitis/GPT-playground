const API_URL = 'http://localhost:5000';

const createRoleForm = document.querySelector('#create-role-form');
const roleNameInput = document.querySelector('#role-name');
const roleContentInput = document.querySelector('#role-content');
const createRoleMessage = document.querySelector('#create-role-message');

createRoleForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const roleName = roleNameInput.value;
    const roleContent = roleContentInput.value;
    fetch(`${API_URL}/Create_New_Role`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `Role_name=${roleName}&Role_content=${roleContent}`
    })
        .then(response => response.text())
        .then(data => createRoleMessage.textContent = data)
        .catch(error => createRoleMessage.textContent = error);
});

const getRolesButton = document.querySelector('#get-roles-button');
const rolesList = document.querySelector('#roles-list');

getRolesButton.addEventListener('click', () => {
    fetch(`${API_URL}/Get_Roles`)
        .then(response => response.json())
        .then(roles => {
            rolesList.innerHTML = '';
            for (const [roleName, roleContent] of Object.entries(roles)) {
                const listItem = document.createElement('li');
                listItem.textContent = `${roleName}: ${roleContent}`;
                rolesList.appendChild(listItem);
            }
        })
        .catch(error => alert(error));
});

const deleteRoleForm = document.querySelector('#delete-role-form');
const deleteRoleNameInput = document.querySelector('#delete-role-name');
const deleteRoleMessage = document.querySelector('#delete-role-message');

deleteRoleForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const roleName = deleteRoleNameInput.value;
    fetch(`${API_URL}/Delete_Role`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `Role_name=${roleName}`
    })
        .then(response => response.text())
        .then(data => deleteRoleMessage.textContent = data)
        .catch(error => deleteRoleMessage.textContent = error);
});

