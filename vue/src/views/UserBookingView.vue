<template>
<div class="container">
    <div v-if="log">
        <UserNavbar @logchange="log = $event" />
        <UserBookings />

    </div>
    <div v-if="!log">
    </div>
</div>
</template>

   
   
<script>
import UserNavbar from "@/components/UserNavbar.vue";
// import UserDashboard from "@/components/UserDashboard.vue";
import router from '@/router';
import UserBookings from "@/components/UserBookings.vue";
export default {
    name: 'UserBookingView',
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
        UserNavbar,
        UserBookings
    },
    mounted() {
        if (localStorage.getItem("access_token")) {
            this.log = true;
            this.name = localStorage.getItem('name')
        } else {
            this.log = false;
        }
    }

}
</script>
