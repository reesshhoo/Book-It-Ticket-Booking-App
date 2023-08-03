<template>
<body class="bg-nav">
    <!-- // Bootswatch CDN -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/flatly/bootstrap.min.css" integrity="sha384-qF/QmIAj5ZaYFAeQcrQ6bfVMAh4zZlrGwTPY7T/M+iTTLJqJBJjwwnsE5Y0mV7QK" crossorigin="anonymous">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#"> <img src="../assets/BookIt.png" height="35px" style="margin-top: -8px;" alt=""> <b style="font-size: 25px;"> BookIt </b></a>

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
                <div class="card" style="margin-top: 30px;">
                    <div class="card-body">
                        <h1><b>Sign In</b></h1><br>
                        <form class="form">
                            <label>Email</label><br>
                            <input v-model="email" type="text" class="form-control">
                            <p v-if="emailerror" style="color: red;">{{ emailerror }}</p>

                            <label class="mt-2">Password</label><br>
                            <input v-model="password" type="password" class="form-control">
                            <p v-if="passworderror" style="color: red;">{{ passworderror }}</p>

                            <div class="form-check">
                                <input class="form-check-input" type="radio" v-model="role" name="userradio" id="user" value="user">
                                <label class="form-check-label" for="user">
                                    I am a user
                                </label>
                                <span style="margin-left: 50px;">
                                    <input class="form-check-input" type="radio" name="adminradio" v-model="role" id="admin" value="admin">
                                    <label class="form-check-label" for="admin">
                                        I am an Admin
                                    </label>
                                </span>
                            </div>
                            <p v-if="roleerror" style="color: red;">{{ roleerror }}</p><br>
                            <br>

                            <div class="d-grid gap-2">
                                <button @click.prevent="submitForm" class="btn btn-lg btn-primary" type="button" value="Login-admin">Log In</button>
                            </div>
                        </form>
                        <p class="mt-2">Not Registered?<router-link to="/Register"> Sign Up </router-link>
                        </p>
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
            email: '',
            password: '',
            emailerror: '',
            passworderror: '',
            role: '',
            roleerror: '',
            errorMessage: '',
        }
    },
    methods: {
        submitForm: function () {
            if (this.email && this.password && this.role) {
                if (!this.isValidEmail(this.email)) {
                    this.emailerror = "Please enter a valid email address";
                    return;
                }

                fetch("http://127.0.0.1:5000/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        role: this.role
                    }),
                }).then((response) => {
                    if (!response.ok) {
                        alert("Invalid Credentials");
                    }
                    return response.json();
                }).then((data) => {
                    if (data.status) {
                        localStorage.setItem("access_token", data.access_token);
                        localStorage.setItem("name", data.name);
                        localStorage.setItem("role", this.role);

                        if (this.role == 'admin') {
                            router.push('/Admin_View')
                        } else {
                            router.push('/User_view')
                        }
                    } else {
                        this.email = null;
                        this.password = null;
                        this.errorMessage = data.msg;

                    }
                }).catch((e) => {
                    console.log(e);
                });

            } else {
                if (!this.email) {
                    this.emailerror = "Please enter email";
                }
                if (!this.password) {
                    this.passworderror = "Please enter password";
                }
                if (!this.role) {
                    this.roleerror = "Please select your role";
                }
                return;
            }
        },
        isValidEmail(email) {
            // Regular expression to validate email format
            const emailRegex = /\S+@\S+\.\S+/;
            return emailRegex.test(email);
        }
    },
    async mounted() {
        if (localStorage.getItem("access_token")) {
            switch (localStorage.getItem("role")) {
                case "admin":
                    router.push('/Admin_View');
                    break;
                case "user":
                default:
                    router.push('/User_view');
                    break;
            }
        }

    }
}
</script>

<style>
.card {

    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);

}
</style>
