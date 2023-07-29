<template>
<div class="dashboard">
    <div class="container-fluid">
        <!------------------------------------------------------- Displaying venues -------------------------------------------------------------->
        <div class="row">
            <div class="row-3" v-for="venue in venues" :key="venue.venue_id">
                <div class="d-flex justify-content-between  align-items-center" style=" border-bottom:3px solid rgba(13, 12, 12, 0.537); margin-bottom: 15px;">
                    <h2 class="text-primary text-dark" style="margin-top:10px;">{{ venue.name }}</h2>
                    <!------------------------------------------------------- Venue Header ---------------------------------------------------------------->
                    <div>
                        <button @click="addShowOpenModal(venue.name)" class="btn btn-success btn-lg text-primary mr-2" style="position:relative; "> Add show </button>
                        <button class="btn btn-warning btn-lg text-primary mr-2"> + </button>
                        <button class="btn btn-danger btn-lg text-primary"> Del </button>
                    </div>
                </div>

                <!----------------------------------------------------- Displaying Shows ----------------------------------------------------------------->
                <!-- <div v-if="venue.shows.length > 0" class="shows-container"> -->
                <div class="flex row">
                    <div v-for="show in venue.shows" :key="show.show_id" class="card border-primary mb-2" style="max-width: 20rem; margin-top: 13px; margin-left:15px">
                        <div class="card-header">{{show.name}}</div>
                        <div class="card-body">
                            <h4 class="card-title"></h4>
                            <p class="card-text">Some quick example text to build on the card title and make up the bulk of
                                the card's content.</p>
                            <div class="d-grid gap-2">
                                <button class="btn btn-warning text-primary" type="button">Update</button>
                                <button class="btn btn-danger text-white" type="button">Delete</button>
                            </div>
                            <!-- </div> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!----------------------------------------------------- Adding venues Modal ----------------------------------------------------------------->

    <div class=" add-venue-container">
        <button @click="OpenModal" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#VenueModal" type="button" style="margin-top: 450px;">Add New Venue</button>
    </div>
    <div class="modal fade" :class="{ 'show': showModal }" id="VenueModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="VenueModalLabel" style="position: fixed;">Add Venue</h5>
                    <button @click="closeModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="field">
                        <label class="label">
                            <h5> Venue Name </h5>

                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="venueName" placeholder="Enter venue name" />
                            <p v-if="venueNameerror" style="color: red;">{{ venueNameerror }}</p>
                        </div>
                        <!-- <label class="label">
                                <h5> No. of screens in venue </h5>
                            </label>
                            <div class="control mb-3">
                                <input class="form-control" type="number" v-model="venueScreens"
                                    placeholder="Enter seating capacity of venue" />
                                <p v-if="venueScreenerror" style="color: red;">{{ venueScreenerror }}</p>
                            </div> -->
                    </div>
                </div>
                <!-- </section> -->
                <div class="modal-footer">
                    <button class="btn btn-success" @click="addVenue">Add Venue</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeModal">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <!----------------------------------------------------- Adding Shows Modal ----------------------------------------------------------------->

    <div class="modal fade" :class="{ 'show': addShowModal }" id="VenueModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ShowModalLabel" style="position: fixed;">Add Show</h5>
                    <button @click="closeShowModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="field">
                        <label class="label">
                            <h5> Show Name </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="showName" placeholder="Enter Show name" />
                            <p v-if="ShowNameerror" style="color: red;">{{ ShowNameerror }}</p>
                        </div>

                        <label class="label">
                            <h5> Price </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="price" placeholder="Enter price of each ticket" />
                            <p v-if="priceerror" style="color: red;">{{ priceerror }}</p>
                        </div>

                        <label class="label">
                            <h5> Screen Number </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="ShowScreen" placeholder="Enter the Screen no. of the show" />
                            <p v-if="ShowScreenerror" style="color: red;">{{ ShowScreenerror }}</p>
                        </div>

                        <label class="label">
                            <h5> Seats Available</h5>
                        </label>
                        <div class="control mb-3">
                            <input v-model="ShowSeats" label="seats" placeholder="Seats open for booking" />
                            <p v-if="ShowSeatserror" style="color: red;">{{ ShowSeatserror }}</p>
                        </div>

                        <label class="label">
                            <h5> Date and Time of the show </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="datetime-local" v-model="ShowDateTime" placeholder="Enter date and time of show" />
                            <p v-if="ShowDatetimeerror" style="color: red;">{{ ShowDatetimeerror }}</p>
                        </div>

                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-success" @click="addShow">Add Show</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeShowModal">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
// import router from '@/router';

export default {
    name: "AdminDashboard",
    data() {
        return {
            errormsg: '',
            venues: [],
            venueName: '',
            venueNameerror: '',
            shows: {},
            showName: '',
            ShowScreen: '',
            ShowSeats: 0,
            ShowDateTime: '',
            screenOptions: [],
            ShowNameerror: '',
            ShowScreenerror: '',
            price: '',
            priceerror: '',
            showModal: false,
            addShowModal: false,
            ShowSeatserror: '',
            ShowDatetimeerror: '',

        }
    },
    methods: {
        OpenModal() {
            this.showModal = true;

        },
        addShowOpenModal(venueName) {
            this.venueName = venueName;
            this.addShowModal = true;

        },
        closeModal() {
            this.showModal = false;
            location.reload()
        },
        closeShowModal() {
            this.addShowModal = false;
            location.reload()
        },
        addVenue() {
            if (this.venueName) {
                fetch("http://127.0.0.1:5000/api/Venues", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        name: this.venueName,
                    }),

                }).then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                }).then((data) => {
                    console.log(data)
                    if (data && data.status) {
                        // 
                        // alert("Venue added successfully");
                        // router.push('/Admin_View');
                        const {
                            venue_id,
                            admin_id
                        } = data
                        const new_venue = {
                            venue_id,
                            name: this.venueName,
                            admin_id,
                        }

                        this.venues.push(new_venue);
                        // this.screenOptions.push(screen_options);
                        console.log(this.venues);

                    } else {
                        if (data && data.msg) {
                            this.errormsg = data.msg;
                            console.log(this.errormsg);
                        } else {
                            this.errormsg = "Unknown error occurred.";
                            console.log(this.errormsg);
                        }
                    }
                }).catch((e) => {
                    console.log(e);
                }).finally(() => {
                    this.closeModal();
                })
            } else {
                if (!this.venueName) {
                    this.venueNameerror = "Please enter the name of the venue";
                }
            }
        },
        addShow() {
            if (this.showName && this.price && this.ShowScreen && this.ShowDateTime && this.ShowSeats) {
                const currentVenue = this.venues.find(venue => venue.name === this.venueName);
                if (!currentVenue) {
                    console.error('Venue not found.');
                    return;
                }

                fetch(`http://127.0.0.1:5000/api/shows/${currentVenue.venue_id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        name: this.showName,
                        price: this.price,
                        show_screen: this.ShowScreen,
                        show_seats: this.ShowSeats,
                        show_datetime: this.ShowDateTime
                    }),
                }).then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                }).then((data) => {
                    if (data && data.status) {
                        const {
                            show_id,
                            name,
                            show_datetime,
                            seats_available,
                            show_screen,
                            price
                        } = data;
                        const newShow = {
                            show_id,
                            name,
                            price,
                            show_screen,
                            seats_available,
                            show_datetime

                        };
                        currentVenue.shows.push(newShow);
                        console.log('New show added:', newShow);
                    } else {
                        if (data && data.msg) {
                            this.errormsg = data.msg;
                            console.log(this.errormsg);
                        } else {
                            this.errormsg = "Unknown error occurred.";
                            console.log(this.errormsg);
                        }
                    }
                }).catch((e) => {
                    console.log(e);
                }).finally(() => {
                    this.closeShowModal();
                });
            } else {
                if (!this.showName) {
                    this.ShowNameerror = "Please enter the name of the show";
                }
                if (!this.price) {
                    this.priceerror = "Please enter the price of the show";
                }
                if (!this.ShowScreen) {
                    this.ShowScreenerror = "Please choose the screen number for the show";
                }
            }
        },

        loadvenues() {
            fetch("http://127.0.0.1:5000/api/Venues", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            }).then((response) => {
                if (!response.ok) {
                    alert("Response not ok");
                }
                console.log(response);
                return response.json();
            }).then((data) => {
                if (data) {
                    console.log("here's the data");
                    this.venues = data.venues;
                    console.log(this.venues)

                } else {
                    this.errormsg = data.msg;
                }
            }).catch((e) => {
                console.log(e);
            });
        },
        loadShows() {
            const currentVenue = this.venues.find((venue) => venue.name === this.venueName);
            if (!currentVenue) {
                console.error('Venue not found.');
                return;
            }
            fetch(`http://127.0.0.1:5000/api/Shows/${currentVenue.venue_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            }).then((response) => {
                if (!response.ok) {
                    alert("Response not ok");
                }
                console.log(response);
                return response.json();
            }).then((data) => {
                if (data) {
                    console.log("Here's the data");
                    this.shows = data.shows;
                } else {
                    this.errormsg = data.msg;
                }
            }).catch((e) => {
                console.log(e);
            });
        }
    },

    async mounted() {
        this.loadvenues();
        // this.loadShows();

    }
}
</script>

<style scoped>
.dashboard {
    position: relative;
}

.modal {
    display: none;
    background: rgba(0, 0, 0, 0.5);
}

.show {
    display: block;

}

.add-venue-container {
    position: fixed;
    bottom: 20px;
    z-index: 999;
    width: 200px;
    font-size: 1.1rem;
    padding: 10px;

}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -0.5rem;
}

.col-md-4 {
    padding: 0.5rem;
}
</style>
