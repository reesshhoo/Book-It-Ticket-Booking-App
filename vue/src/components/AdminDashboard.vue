<template>
<div class="dashboard">
    <div class="container-fluid">
        <!------------------------------------------------------- Displaying venues -------------------------------------------------------------->
        <div class="row">
            <div class="row-3 card border-primary mb-3 mt-5" v-for="venue in venues" :key="venue.venue_id">
                <div class="d-flex justify-content-between  align-items-center" style=" border-bottom:3px solid rgba(13, 12, 12, 0.537); margin-bottom: 15px;">
                    <h2 class="text-primary text-dark" style="margin-top:15px;">{{ venue.name }} <br />
                        <h6 class="card-subtitle text-muted mt-0.7" style="font-size: 20px; margin-left: 2px;"> {{ venue.venue_location }}</h6>
                    </h2>
                    <!------------------------------------------------------- Venue Header ---------------------------------------------------------------->
                    <div>
                        <button @click="addShowOpenModal(venue.name)" class="btn btn-success btn-lg text-primary mr-2" style="position:relative; "> Add show </button>
                        <button @click="OpenEditvenueModal(venue.name)" class="btn btn-warning btn-lg text-primary mr-2"> &#128393; </button>
                        <button @click="deleteVenue(venue.name)" class="btn btn-danger btn-lg text-primary"> Del </button>

                    </div>
                </div>

                <!----------------------------------------------------- Displaying Shows ----------------------------------------------------------------->

                <div class="flex row mb-2">
                    <div v-for="show in venue.shows.shows" :key="show.show_id" class="card border-primary mb-2" style="max-width: 20rem; margin-top: 13px; margin-left:15px">

                        <div class="card-header" style="font-size: 32px;">{{show.name}}</div>
                        <div class="card-body">
                            <h4 class="card-title"></h4>
                            <h6 class="card-subtitle text-muted" style="font-size: 20px;">{{ show.show_datetime }}</h6>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="d-block user-select-none" width="100%" height="200" aria-label="Placeholder: Image cap" focusable="false" role="img" preserveAspectRatio="xMidYMid slice" viewBox="0 0 318 180" style="font-size:1.125rem;text-anchor:middle">
                            <rect width="100%" height="100%" fill="#868e96"></rect>
                            <text x="50%" y="50%" fill="#dee2e6" dy=".3em">Image cap</text>
                        </svg>
                        <div class="card-body">
                            <p class="card-text" style="font-size: 20px;">Screen Number : {{ show.show_screen }}</p>
                            <!-- <p class="card-text" style="font-size: 20px;">{{ show.show_datetime }}</p> -->
                            <p class="card-text" style="font-size: 20px;">Seats Available: {{ show.seats_booked }} / {{ show.seats_available }}</p>

                        </div>

                        <div class="d-grid gap-2">
                            <button @click="OpenEditShowModal(show.name)" class="btn btn-warning text-primary" type="button">Update</button>
                            <button class="btn btn-danger text-white mb-3" type="button">Delete</button>

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
                        <label class="label">
                            <h5> Venue Location </h5>

                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="venueLocation" placeholder="Enter venue location" />
                            <p v-if="venueLocationerror" style="color: red;">{{ venueLocationerror }}</p>
                        </div>

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
    <!----------------------------------------------------- Editing venues Modal ----------------------------------------------------------------->

    <div class="modal fade" :class="{ 'show': EditVenueModal }" id="EditVenueModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="VenueModalLabel" style="position: fixed;">Edit Venue</h5>
                    <button @click="closeEditVenueModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="field">
                        <label class="label">
                            <h5> Venue Name </h5>

                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="newVenueName" placeholder="Enter venue name" />

                        </div>
                        <label class="label">
                            <h5> Venue Location </h5>

                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="newVenueLocation" placeholder="Enter venue location" />

                        </div>

                    </div>
                </div>
                <!-- </section> -->
                <div class="modal-footer">
                    <button class="btn btn-success" @click="EditVenue">Edit Venue</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeEditVenueModal">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <!----------------------------------------------------- Adding Shows Modal ----------------------------------------------------------------->

    <div class="modal fade" :class="{ 'show': addShowModal }" id="AddShowModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
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
                            <input class="form-control" v-model="ShowSeats" label="seats" placeholder="Seats open for booking" />
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

    <!----------------------------------------------------- Editing Shows Modal ----------------------------------------------------------------->

    <div class="modal fade" :class="{ 'show': EditShowModal }" id="EditShowModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ShowModalLabel" style="position: fixed;">Edit Show</h5>
                    <button @click="closeEditShowModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="field">
                        <label class="label">
                            <h5> Show Name </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="newshowName" placeholder="Enter Show name" />
                        </div>

                        <label class="label">
                            <h5> Price </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="newprice" placeholder="Enter price of each ticket" />
                        </div>

                        <label class="label">
                            <h5> Screen Number </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="text" v-model="newShowScreen" placeholder="Enter the Screen no. of the show" />
                        </div>

                        <label class="label">
                            <h5> Seats Available</h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" v-model="newShowSeats" label="seats" placeholder="Seats open for booking" />
                        </div>

                        <label class="label">
                            <h5> Date and Time of the show </h5>
                        </label>
                        <div class="control mb-3">
                            <input class="form-control" type="datetime-local" v-model="newShowDateTime" placeholder="Enter date and time of show" />
                        </div>

                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-success" @click="EditShow">Edit Show</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeEditShowModal">Cancel</button>
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
            newVenueName: '',
            venueNameerror: '',
            venueLocation: '',
            newVenueLocation: '',
            venueLocationerror: '',
            newshowName: '',
            newprice: '',
            newShowScreen: '',
            newShowSeats: 0,
            newShowDateTime: '',
            showName: '',
            ShowScreen: '',
            ShowSeats: 0,
            ShowDateTime: '',
            ShowNameerror: '',
            ShowScreenerror: '',
            price: '',
            priceerror: '',
            showModal: false,
            EditVenueModal: false,
            addShowModal: false,
            EditShowModal: false,
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
            this.venueName = '';
            location.reload();
        },
        OpenEditvenueModal(venueName) {
            console.log(venueName);
            this.newVenueName = '';
            this.newVenueLocation = '';
            this.venueName = venueName;
            this.EditVenueModal = true;
        },
        closeEditVenueModal() {
            this.EditVenueModal = false;
            // location.reload();
        },
        OpenEditShowModal(showName) {
            // console.log(showName)
            this.showName = showName;
            this.EditShowModal = true;
        },
        closeEditShowModal() {
            this.EditShowModal = false;
            // location.reload();
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
                // console.log(response);
                return response.json();
            }).then((data) => {
                if (data) {
                    console.log(data.venues);
                    this.venues = data.venues;
                    console.log(this.venues)

                } else {
                    this.errormsg = data.msg;
                }
            }).catch((e) => {
                console.log(e);
            });
        },
        addVenue() {
            if (this.venueName && this.venueLocation) {
                fetch("http://127.0.0.1:5000/api/Venues", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        name: this.venueName,
                        venue_location: this.venueLocation,
                    }),

                }).then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                }).then((data) => {
                    // console.log(data)
                    if (data && data.status) {
                        // 
                        // alert("Venue added successfully");
                        // router.push('/Admin_View');
                        const {
                            venue_id,
                            admin_id,

                        } = data
                        const new_venue = {
                            venue_id,
                            name: this.venueName,
                            admin_id,
                        }
                        // console.log(new_venue)

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
                if (!this.venueLocation) {
                    this.venueLocationerror = "Please enter the Location of the venue";
                }
            }
        },
        deleteVenue(venueName) {
            const currentVenue = this.venues.find((venue) => venue.name === venueName);
            if (!currentVenue) {
                console.error("Venue not found");
                return;
            }

            fetch(`http://127.0.0.1:5000/api/Venues/${currentVenue.venue_id}`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    }
                })
                .then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data && data.status) {
                        // Remove the deleted venue from the `venues` array
                        const index = this.venues.indexOf(currentVenue);
                        if (index !== -1) {
                            this.venues.splice(index, 1);
                        }
                        console.log('Venue deleted successfully');
                    } else {
                        if (data && data.msg) {
                            this.errormsg = data.msg;
                            console.log(this.errormsg);
                        } else {
                            this.errormsg = "Unknown error occurred.";
                            console.log(this.errormsg);
                        }
                    }
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        EditVenue() {
            // console.log(venueName)
            const currentVenue = this.venues.find(venue => venue.name === this.venueName);
            // const currentVenue = this.venueName === venueName;
            if (!currentVenue) {
                console.error("Venue not found");
                return;
            }

            if (!this.newVenueName && !this.newVenueLocation) {
                console.error("No changes made");
                return;
            }
            const requestBody = {};
            if (this.newVenueName) {
                requestBody.name = this.newVenueName;
            }
            if (this.newVenueLocation) {
                requestBody.venue_location = this.newVenueLocation;
            }

            fetch(`http://127.0.0.1:5000/api/Venues/${currentVenue.venue_id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify(requestBody),
                })
                .then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data && data.status) {
                        // Update the venue details in the `venues` array
                        if (this.newVenueName) {
                            currentVenue.name = this.newVenueName;
                        }
                        if (this.newVenueLocation) {
                            currentVenue.venue_location = this.newVenueLocation;
                        }
                        console.log("Venue updated successfully");
                    } else {
                        if (data && data.msg) {
                            this.errormsg = data.msg;
                            console.log(this.errormsg);
                        } else {
                            this.errormsg = "Unknown error occurred.";
                            console.log(this.errormsg);
                        }
                    }
                })
                .catch((e) => {
                    console.log(e);
                })
                .finally(() => {
                    this.closeEditVenueModal(); // Assuming you have a function to close the modal after editing.
                });
        },

        addShow() {
            if (this.showName && this.price && this.ShowScreen && this.ShowDateTime && this.ShowSeats) {
                const currentVenue = this.venues.find(venue => venue.name === this.venueName);
                console.log(currentVenue.venue_id);
                if (!currentVenue) {
                    console.error('Venue not found.');
                    return;
                }

                fetch(`http://127.0.0.1:5000/api/Shows/${currentVenue.venue_id}`, {
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
                        // // console.log(this.venues);
                        // const idx = this.venues.filter((e, i) => {
                        //     return e.venue_id === currentVenue.venue_id ? i : -1;
                        // })
                        // // this.venues.filter(v => v.venue_id === currentVenue.venue_id).shows.shows.push(newShow);
                        // this.venues[idx].shows.show.push(newShow);
                        // // this.venues.shows.push(newShow);
                        currentVenue.shows.push(newShow);
                        console.log('New show added:', newShow);
                        // window.reload();
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
        EditShow() {
            
            const currentVenue = this.venues.find(venue => {
                return Array.isArray(venue.shows.shows) &&  venue.shows.shows.some(show => show.name === this.showName);
            });
            // const currentVenue = this.venueName === venueName;
            if (!currentVenue) {
                console.error("venue not found");
                return;
            }
            // console.log(currentVenue);
            const currentShow = currentVenue.shows.shows.find(show => show.name === this.showName);
            // console.log(currentShow);
            if (!this.newshowName && !this.newprice && !this.newShowDateTime && !this.newShowScreen && !this.newShowSeats) {
                console.error("No changes made");
                return;
            }
            const requestBody = {};
            if (this.newshowName) {
                requestBody.name = this.newshowName;
            }
            if (this.newprice) {
                requestBody.price = this.newprice;
            }
            if (this.newShowDateTime) {
                requestBody.date_time = this.newShowDateTime;
            }
            if (this.newShowScreen) {
                requestBody.show_screen = this.newShowScreen;
            }
            if (this.newShowSeats) {
                requestBody.price = this.newprice;
            }
            // console.log(currentShow)
            fetch(`http://127.0.0.1:5000/api/Shows/${currentShow.show_id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify(requestBody),
                })
                .then((response) => {
                    if (!response.ok) {
                        alert("Response not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data && data.status) {
                        // Update the venue details in the `venues` array
                        if (this.newVenueName) {
                            currentShow.name = this.newShowName;
                        }
                        if (this.newprice) {
                            currentShow.price = this.newprice;
                        }
                        if (this.newShowDateTime) {
                            currentShow.date_time = this.newShowDateTime;
                        }
                        if (this.newShowScreen) {
                            currentShow.show_screen = this.newShowScreen;
                        }
                        if (this.newShowSeats) {
                            currentShow.seats_available = this.newShowSeats;
                        }
                        console.log("Venue updated successfully");
                    } else {
                        if (data && data.msg) {
                            this.errormsg = data.msg;
                            console.log(this.errormsg);
                        } else {
                            this.errormsg = "Unknown error occurred.";
                            console.log(this.errormsg);
                        }
                    }
                })
                .catch((e) => {
                    console.log(e);
                })
                .finally(() => {
                    this.closeEditShowModal();
                    this.loadvenues(); // Assuming you have a function to close the modal after editing.
                });
        },

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
    right: 0%;

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
