<template>
    <div class="container">
      <div v-if="log">
        <AdminNavbar @logchange="log = $event" />
        <AdminSummary/>
  
      </div>
      <div v-if="!log">
      </div>
    </div>
  </template>
  
  
  <script>
  import AdminNavbar from "@/components/AdminNavbar.vue";
  import AdminSummary from "@/components/AdminSummary.vue";
  import router from '@/router';
  export default {
    name: 'AdminSummaryView',
    data() {
      return {
        log: false,
        name: '',
      }
    },
    watch: {
      log(newValue) {
        if (!newValue) {
          this.renderLogin()
        }
      },
    },
    methods: {
      renderLogin() {
        router.push('/');
      }
    },
    components: {
      AdminNavbar,
      AdminSummary
    },
    mounted() {
      if (localStorage.getItem("access_token")) {
        this.log = true;
        this.name = localStorage.getItem('name')
      }
      else {
        this.log = false;
      }
    }
  
  }
  </script>