<template>
  <div>
    <AppHeader @navigate="navigate" />
    <div class="container mx-auto px-4 mt-8">
      <component :is="currentView" />
    </div>
  </div>
</template>


<script>
import AppHeader from "./components/Header.vue";
import Chatbot from "./components/Chatbot.vue";
import Roles from "./components/Roles.vue";

export default {
  components: {
    AppHeader,
    Chatbot,
    Roles,
  },
  data() {
    return {
      currentView: 'Chatbot',
    };
  },
  methods: {
    navigate(view) {
      this.currentView = view;
    },
  },
};
</script>
