<template>
  <div class="bg-gray-800 text-white">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <div class="flex space-x-4">
          <button @click="$emit('navigate', 'Chatbot')" class="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75">Chatbot</button>
          <button @click="$emit('navigate', 'Roles')" class="py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75">Roles</button>
        </div>  
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AppHeader',
  methods: {
    navigate(view) {
      this.$emit('navigate', view);
    },
  },
};
</script>
