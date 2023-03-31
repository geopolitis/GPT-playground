<template>
  <div class="container mx-auto px-4">
    <h1 class="text-4xl font-bold mb-8">Roles</h1>

    <h2 class="text-2xl font-bold mb-4">Create a new role</h2>
    <form @submit.prevent="createRole" class="space-y-4">
      <div>
        <label for="role-name" class="block mb-1">Role name:</label>
        <input type="text" id="role-name" v-model="roleName" class="border border-gray-300 p-2 w-full" />
      </div>
      <div>
        <label for="role-content" class="block mb-1">Role content:</label>
        <input type="text" id="role-content" v-model="roleContent" class="border border-gray-300 p-2 w-full" />
      </div>
      <input type="submit" value="Submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" />
    </form>
    <p>{{ createRoleMessage }}</p>

    <h2 class="text-2xl font-bold mb-4">Get roles that match a name</h2>
    <form @submit.prevent="getMatchingRoles" class="space-y-4">
      <div>
        <label for="search-role-name" class="block mb-1">Role name:</label>
        <input type="text" id="search-role-name" v-model="searchRoleName" class="border border-gray-300 p-2 w-full" />
      </div>
      <input type="submit" value="Search" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" />
    </form>
    <ul class="list-none space-y-2">
      <li v-for="(content, name) in matchingRoles" :key="name" class="p-2 bg-gray-100 rounded shadow font-mono">{{ name }}: {{ content }}</li>
    </ul>

    <h2 class="text-2xl font-bold mb-4">Delete a role</h2>
    <form @submit.prevent="deleteRole" class="space-y-4">
      <div>
        <label for="delete-role-name" class="block mb-1">Role name:</label>
        <input type="text" id="delete-role-name" v-model="deleteRoleName" class="border border-gray-300 p-2 w-full" />
      </div>
      <input type="submit" value="Submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" />
    </form>
    <p>{{ deleteRoleMessage }}</p>

    <!-- "Get roles" button here -->
    <div class="mt-8 mb-4">
      <h2 class="text-2xl font-bold mb-4">Get all roles</h2>
      <button @click="getRoles" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Get roles</button>
    </div>
  </div>
</template>

<script>
const API_URL = "http://localhost:5000";

export default {
  data() {
    return {
      roleName: "",
      roleContent: "",
      createRoleMessage: "",
      roles: {},
      deleteRoleName: "",
      deleteRoleMessage: "",
      searchRoleName: "",
      matchingRoles: {}, 
    };
  },
  methods: {
    createRole() {
      fetch(`${API_URL}/Create_New_Role`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `Role_name=${this.roleName}&Role_content=${this.roleContent}`,
      })
        .then((response) => response.text())
        .then((data) => (this.createRoleMessage = data))
        .catch((error) => (this.createRoleMessage = error));
    },
    getRoles() {
      fetch(`${API_URL}/Get_Roles`)
        .then((response) => response.json())
        .then((roles) => {
          this.roles = roles;
        })
        .catch((error) => alert(error));
    },
    getMatchingRoles() {
      fetch(`${API_URL}/Get_Roles?name=${encodeURIComponent(this.searchRoleName)}`)
        .then((response) => response.json())
        .then((matchingRoles) => {
            this.matchingRoles = matchingRoles;
        })
          .catch((error) => alert(error));
    },
    deleteRole() {
      fetch(`${API_URL}/Delete_Role`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `Role_name=${this.deleteRoleName}`,
      })
        .then((response) => response.text())
        .then((data) => (this.deleteRoleMessage = data))
        .catch((error) => (this.deleteRoleMessage = error));
    },
  },
};
</script>