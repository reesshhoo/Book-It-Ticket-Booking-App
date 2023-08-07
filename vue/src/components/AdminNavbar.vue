<template>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/flatly/bootstrap.min.css" integrity="sha384-qF/QmIAj5ZaYFAeQcrQ6bfVMAh4zZlrGwTPY7T/M+iTTLJqJBJjwwnsE5Y0mV7QK" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary mt-2 sticky-top" style="border-radius: 30px;">
    <div class="container-fluid">
        <a class="navbar-brand" href="#"> <b style="font-size: 32px;"> BookIt </b></a>
        <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a @click="redirectHome" class="nav-link active lead" href="#">Home
                        <span class="visually-hidden">(current)</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a @click="redirectSummary" class="nav-link lead" href="#">Summary</a>
                </li>

            </ul>

        </div>
        <button id="logout" @click="logout" class="btn btn-danger nav-link text-primary font-weight-bold"> <i style="font-size:24px" class="fa">&#xf08b;</i> Logout</button>
    </div>
</nav>
</template>

<script>
import router from '@/router';

export default {
    name: 'AdminNavbar',
    methods: {
        logout: function () {
            localStorage.clear();
            this.$emit('logchange', false);

        },
        redirectHome() {
            router.push('/Admin_view')
        },
        redirectSummary() {
            router.push('/Admin_Summary_view')
        }
    }
}
</script>
