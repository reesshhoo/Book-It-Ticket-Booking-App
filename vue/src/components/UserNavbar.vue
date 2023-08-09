<template>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/flatly/bootstrap.min.css" integrity="sha384-qF/QmIAj5ZaYFAeQcrQ6bfVMAh4zZlrGwTPY7T/M+iTTLJqJBJjwwnsE5Y0mV7QK" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary mt-2 sticky-top" style="border-radius: 30px;">
    <div class="container-fluid">
        <img class="navbar-brand" style="height:2%; width: 4%;" src="../assets/BookIt.png" alt=""> <b style="font-size: 32px; color: azure; margin-right: 10px;"> BookIt </b>
        <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a @click="redirectHome" class="nav-link active lead" href="#">Home
                        <span class="visually-hidden">(current)</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a @click="redirectBookings" class="nav-link lead" href="#">Bookings</a>
                </li>

            </ul>

        </div>
        <form class="d-flex">
            <input v-model="searchValue" class="form-control me-sm-2" type="search" placeholder="Search">
            <button @click="searchFunction" class="btn btn-secondary my-2 my-sm-0 mr-2 text-primary font-weight-bold" type="submit">Search</button>
        </form>
        <button id="logout" @click="logout" class="btn btn-secondary nav-link text-primary font-weight-bold" style="font-size: 20px;">Logout <i class="fa mt-1">&#xf08b;</i> </button>
    </div>
</nav>
</template>

    
    
<script>
import router from '@/router';

export default {
    name: 'UserNavbar',
    data() {
        return{
        searchValue: null,
        }
    },
    methods: {
        logout: function () {
            localStorage.clear();
            this.$emit('logchange', false);

        },
        redirectHome() {
            router.push('/User_view')
        },
        redirectBookings() {
            router.push('/User_Bookings')
        },
        searchFunction(){
            if (!this.searchValue) {
                alert('Enter a value to search');
            }
            else{
            router.push(`/search/${this.searchValue}`)
        }
    }
    }
}
</script>
