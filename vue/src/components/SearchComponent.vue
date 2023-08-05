<template>
<div class="container">
    <div class="dashboard">
        <UserNavbar />
        <div class="container-fluid">
            <!------------------------------------------------------- Displaying venues -------------------------------------------------------------->
            <div class="">
                <div class=" row">
                    <div class="row-3 card border-primary mb-3 mt-5" v-for="result in results" :key="result.venue_id">
                        <div class="d-flex justify-content-between  align-items-center" style=" border-bottom:3px solid rgba(13, 12, 12, 0.537); margin-bottom: 15px;">
                            <h2 class="text-primary text-dark" style="margin-top:15px;">{{ result.name }} <br />
                                <h6 class="card-subtitle text-muted mt-0.7" style="font-size: 20px; margin-left: 2px;"> {{ result.venue_location }}</h6>
                            </h2>
                        </div>

                        <!----------------------------------------------------- Displaying Shows ----------------------------------------------------------------->

                        <div class="flex row mb-2">
                            <div v-for="show in result.shows" :key="show.show_id" class="card border-primary mb-2 pb-4" style="max-width: 20rem; margin-top: 13px; margin-left:15px">

                                <div class="card-header" style="font-size: 32px;">
                                    {{show.name}}
                                    <h6 class="card-subtitle text-muted" style="font-size: 20px;">{{ show.show_datetime }}</h6>
                                </div>
                                <img v-if="show.imagefile" :src="show.imagefile">
                                <svg v-else class="d-block user-select-none" width="100%" height="200" aria-label="Placeholder: Image cap" focusable="false" role="img" preserveAspectRatio="xMidYMid slice" viewBox="0 0 318 180" style="font-size:1.125rem;text-anchor:middle">
                                    <rect width="100%" height="100%" fill="#868e96"></rect>
                                    <text x="50%" y="50%" fill="#dee2e6" dy=".3em">Image cap</text>
                                </svg>
                                <div class="card-body">
                                    <p class="card-text" style="font-size: 20px;">Screen Number : {{ show.show_screen }}</p>
                                    <p class="card-text" style="font-size: 20px; margin-top: -10px;">Price: &#x20B9; {{ show.price }} /-</p>
                                    <p class="card-text" style="font-size: 20px; margin-top: -10px;">Seats Left: {{ show.seats_available - show.seats_booked }} / {{ show.seats_available }}</p>
                                    <p class="card-text" style="font-size: 20px; margin-top: -10px;">Genre : <span v-for="tag in show.tags" :key="tag" class="badge bg-secondary mr-1">{{ tag }}</span></p>

                                </div>

                                <div class="d-grid gap-2">
                                    <button @click="OpenBookShowModal(show.show_id,show.name,show.show_datetime,show.price,show.seats_available,show.seats_booked, show.imagefile)" class="btn btn-success text-primary" type="button">Book Now!</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!----------------------------------------------------- Book Shows modal----------------------------------------------------------------->

        <div class="modal fade" :class="{ 'show': BookModal }" id="VenueModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="BookModalLabel" style=" font-size:32px">{{ showName }}</h5>
                        <button @click="closeBookModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="field">
                            <div class="card mb-5" width=100% height="80%">
                                <img :src=this.imagefile>
                            </div>
                            <div class="label">

                                <h5> Show Price : <span class="ml-3">&#x20B9; {{ showPrice  }} </span></h5>
                            </div>
                            <div class="label">
                                <h5> Seats Left : <span class="ml-3">{{ seatsAvailable - seatsBooked}} / {{ seatsAvailable }} </span> </h5>
                            </div>
                            <div class="label">
                                <h5> Show Date: <span class="ml-3"> {{ showDateTime }} </span> </h5>
                            </div>
                            <br>
                            <label class="label">
                                <h5> No. of People </h5>
                            </label>
                            <div class="control mb-3">
                                <input class="form-control" type="number" v-model="NumberOfPeople" placeholder="How many tickets do you need?" />
                                <p v-if="NumberOfPeopleerror" style="color: red;">{{ NumberOfPeopleerror }}</p>
                            </div>

                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="OpenPaymentModal">Confirm</button>
                        <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeModal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        <!----------------------------------------------------- Payment Modal ----------------------------------------------------------------->
        <div class="modal fade" :class="{ 'show': PaymentModal }" id="PaymentModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <!-- <h5 class="modal-title" id="ShowModalLabel" style="position: fixed;">Delete Show</h5> -->
                        <button @click="ClosePaymentModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">

                        <h4> Your Total Amount Payable is : <span class="ml-3">&#x20B9; {{ showPrice  * NumberOfPeople}} </span></h4>

                        <div class="field">

                            <h4>Confirm Payment? </h4>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="BookShow">Pay</button>
                        <button class="btn btn-danger" data-bs-dismiss="modal" @click="ClosePaymentModal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue';
import router from '@/router';
// import router from '@/router';

export default {
    name: 'SearchComponent',
    components: {
        UserNavbar
    },
    data() {
        return {
            results: [],
            venues: [],
            errormsg: '',
            BookModal: false,
            PaymentModal: false,
            search: this.$route.params.search,
            NumberOfPeople: null,
            NumberOfPeopleerror: '',
            showid: null,
            showName: '',
            showDateTime: '',
            showPrice: '',
            seatsAvailable: 0,
            seatsBooked: 0,
            imagefile: '',
        }
    },
    methods: {
        OpenBookShowModal(showid, showname, show_datetime, showprice, seats_available, seats_booked, imagefile) {
            this.showid = showid
            this.showName = showname;
            this.showDateTime = show_datetime;
            this.showPrice = showprice;
            this.seatsAvailable = seats_available;
            this.seatsBooked = seats_booked;
            this.imagefile = imagefile;
            this.BookModal = true;

        },
        closeBookModal() {
            this.showid = null;
            this.showName = null;
            this.showDateTime = null;
            this.showPrice = null;
            this.seatsAvailable = null;
            this.seatsBooked = null;
            this.NumberOfPeople = null;
            this.NumberOfPeopleerror = null;
            this.BookModal = false;
        },
        OpenPaymentModal() {
            this.PaymentModal = true;
        },
        ClosePaymentModal() {
            this.PaymentModal = false;
            this.closeBookModal();
            router.push('/User_Bookings');
        },

        loadresults() {
            this.search = this.$route.params.search.toLowerCase();
            fetch(`http://127.0.0.1:5000/api/search/${this.search}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            }).then((response) => {
                if (!response.ok) {
                    console.error("Response not ok");
                    throw new Error("Response not ok");
                }
                return response.json();
            }).then((data) => {
                if (data && data.venues && data.venues.length > 0) {
                    console.log(data.venues);
                    this.results = data.venues;
                    console.log(this.results);
                } else {
                    this.errormsg = data.msg || 'No results found';
                    console.log(this.errormsg);
                    router.push('/User_view');
                    alert('No results found');
                }
            }).catch((e) => {
                console.log(e);
                router.push('/User_view');
                alert('No results found');
            });
        },
        BookShow() {
            if (this.NumberOfPeople) {
                if (this.NumberOfPeople > 0) {
                    const currentVenue = this.results.find(venue => {
                        return Array.isArray(venue.shows) && venue.shows.some(show => show.show_id === this.showid);
                    });

                    if (!currentVenue) {
                        console.error("venue not found");
                        return;
                    }
                    // console.log(currentVenue);
                    const currentShow = currentVenue.shows.find(show => show.show_id === this.showid);
                    console.log(currentShow);

                    fetch(`http://127.0.0.1:5000/api/User/${currentShow.show_id}`, {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*",
                                Authorization: "Bearer " + localStorage.getItem("access_token"),
                            },
                            body: JSON.stringify({
                                tickets: this.NumberOfPeople,
                            }),
                        }).then((response) => {
                            if (!response.ok) {
                                alert("Insuffiecient Seats");

                            }
                            return response.json();
                        }).then((data) => {
                            if (data) {
                                console.log(data);

                            } else {
                                this.errormsg = data.msg;
                            }
                        }).catch((e) => {
                            console.log(e);
                        })
                        .finally(() => {
                            this.ClosePaymentModal();
                            this.NumberOfPeople = null;
                        });
                } else {
                    this.NumberOfPeopleerror = 'Please enter valid no. of seats';
                    alert(this.NumberOfPeopleerror);
                }
            }
        }

    },
    mounted() {
        // this.loadvenues();
        this.loadresults();
    },
    // beforeMount() {
    //     this.loadresults();
    // },

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

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -0.5rem;
}
</style>
