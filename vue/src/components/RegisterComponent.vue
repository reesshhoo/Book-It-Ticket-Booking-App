<template>
    <body class="bg-nav">
        <!-- // Bootswatch CDN -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/flatly/bootstrap.min.css"
            integrity="sha384-qF/QmIAj5ZaYFAeQcrQ6bfVMAh4zZlrGwTPY7T/M+iTTLJqJBJjwwnsE5Y0mV7QK" crossorigin="anonymous">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#"> <img src="../assets/BookIt.png" height="35px" style="margin-top: -8px;"
                        alt=""> <b style="font-size: 25px;"> BookIt </b></a>

                <!-- <form class="d-flex">
                    <input class="form-control me-sm-2" type="search" placeholder="Search">
                    <button class="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
                </form> -->
            </div>

        </nav>


        <div class="container">


            <div class="row">
                <div class="col md-8 mt-5">
                    <h1 class="display-4 mt-100" style="font-size: 65px;">
                        <b>Stress Less. </b> <br>
                        <b>Sell more. </b> <br>
                        <b>BookIt. </b>
                    </h1>
                </div>
                <div class="col md-4 ">
                    <div class="card" style="margin-top: 12px;">
                        <div class="card-body">
                            <h1><b>Sign Up!</b></h1><br>
                            <form class="form">
                                <label>Email</label><br>
                                <input v-model="email" type="text" class="form-control">
                                <p v-if="emailerror" style="color: red;">{{ emailerror }}</p>

                                <label class="mt-2">Name</label><br>
                                <input v-model="name" type="text" class="form-control">
                                <p v-if="nameerror" style="color: red;">{{ nameerror }}</p>

                                <label class="mt-2">Password</label><br>
                                <input v-model="password" type="password" class="form-control">
                                <p v-if="passworderror" style="color: red;">{{ passworderror }}</p>

                                <label class="mt-2">Confirm Password</label><br>
                                <input v-model="confirmpassword" type="password" class="form-control">
                                <p v-if="passworderror" style="color: red;">{{ passworderror }}</p><br>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" v-model="role" name="userradio" id="user"
                                        value="user" checked="">
                                    <label class="form-check-label" for="user">
                                        I want to register as a user.
                                    </label>
                                    <span style="margin-left: 50px;">
                                    <input class="form-check-input" type="radio" name="adminradio" v-model="role" id="admin"
                                        value="admin">
                                    <label class="form-check-label" for="admin">
                                        I want to register as an Admin.
                                    </label>
                                </span>
                                </div>
                                <br>

                                <div class="d-grid gap-2">
                                    <button @click.prevent="submitForm" class="btn btn-lg btn-primary"
                                        type="submit">Register</button>
                                </div>
                            </form>
                            <p class="mt-2">Already Registered? <router-link to="/"> Sign In </router-link> </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </body>
</template>

<script>
// import { required, minLength, email, sameAs } from 'vuelidate/lib/validators';
import router from "@/router";

export default {
    data() {
        return {
            name: '',
            email: '',
            password: '',
            confirmpassword: '',
            emailerror: '',
            passworderror: '',
            nameerror: '',
            role: 'user',
            errorMessage: '',
        }
    },
    // validations: {
    //     name: { required },
    //     email: { required, email },
    //     password: { required, minLength: minLength(6) },
    //     confirmpassword: { sameAsPassword: sameAs('password') }
    // },
    methods: {
        submitForm: function () {
            if (this.email && this.password && this.confirmpassword) {
                if (!this.isValidEmail(this.email)) {
                    this.emailerror = "Please enter a valid email address";
                    return;
                }
                if (this.password !== this.confirmpassword) {
                    this.passworderror = 'Passwords do not match';
                    return;
                }
                fetch("http://127.0.0.1:5000/api/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body: JSON.stringify({
                        name: this.name,
                        email: this.email,
                        password: this.password,
                        role: this.role
                    }),
                }).then((response) => {
                    if (!response.ok) {
                        alert("Email already exists");
                    }
                    return response.json();
                }).then((data) => {
                    if (data.status) {
                        localStorage.setItem("access_token", data.access_token);
                        localStorage.setItem("name", this.name);
                        if (this.role == 'admin'){
                            router.push('/Admin_View')
                        }
                        else {
                            router.push('/User_View')
                        }
                    }
                    else {
                        this.name = null;
                        this.email = null;
                        this.password = null;
                        this.errorMessage = data.msg;

                    }
                }).catch((e) => {
                    console.log(e);
                });

            }
            else {
                if (!this.email) {
                    this.emailerror = "Please enter email";
                }
                if (!this.password) {
                    this.passworderror = "Please enter password";
                }
                if (!this.name) {
                    this.nameerror = "Please enter name";
                }
                return;
            }
        },
        isValidEmail(email) {
            // Regular expression to validate email format
            const emailRegex = /\S+@\S+\.\S+/;
            return emailRegex.test(email);
        }
    }
}

</script>


<style>
.card {

    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);


}
</style>


<!-- <div class="container">
    <header>

        <h1>Notes </h1>
        <button @click="showModal = true">+</button>
    </header>
    <div class="card-container">

        <div v-for="note in notes" :key="note.id" class="card" :style="{backgroundColor : note.backgroundColor}">
            <p class="main-text">{{ note.text }}</p>
            <p class="date">{{ note.date.toString() }}</p>
        </div>

    </div>
</div> -->