<template>
    <div>
      <div class="tabs flex justify-center border-b">
        <div
          v-for="tab in tabs"
          :key="tab.id"
          @click="selectTab(tab)"
          :class="['tab p-4', { 'border-b-2 border-blue-500': tab.isActive }]"
        >
          {{ tab.name }}
        </div>
      </div>
      <div class="tab-content">
        <slot :selected-tab="selectedTab"></slot>
      </div>
    </div>
</template>

<script>
  export default {
    props: {
      tabs: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        selectedTab: this.tabs[0].id,
      };
    },
    methods: {
      selectTab(tab) {
        this.selectedTab = tab.id;
        tab.isActive = true;
        this.tabs.forEach((t) => {
          if (t.id !== tab.id) {
            t.isActive = false;
          }
        });
      },
    },
  };
</script>
  
  <style scoped>
  .tab {
    cursor: pointer;
  }
  </style>
  