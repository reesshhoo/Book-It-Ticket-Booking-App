<template>
  <div class="container">
    <div v-if="log">
      <AdminNavbar @logchange="log = $event" />
      <AdminDashboard />

    </div>
    <div v-if="!log">
    </div>
  </div>
</template>


<script>
import AdminNavbar from "@/components/AdminNavbar.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import router from '@/router';
export default {
  name: 'AdminView',
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
    AdminDashboard
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