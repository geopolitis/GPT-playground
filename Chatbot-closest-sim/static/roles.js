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

const getRoleForm = document.querySelector('#get-role-form');
const getRoleNameInput = document.querySelector('#get-role-name');
const getRoleMessage = document.querySelector('#get-role-message');

getRoleForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const roleName = getRoleNameInput.value;
    fetch(`${API_URL}/Get_Roles?name=${roleName}`)
        .then(response => response.json())
        .then(role => {
            getRoleMessage.innerHTML = '';
            for (const [roleName, roleContent] of Object.entries(role)) {
                getRoleMessage.textContent = `${roleName}: ${roleContent}`;
            }
        })
        .catch(error => getRoleMessage.textContent = error);
});