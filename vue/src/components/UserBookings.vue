<template>
<div class="dashboard">
    <div class="container-fluid">
        <table class="table table-hover" style="margin-top: 50px; border-radius: 15px;">
            <thead>
                <tr class="table-primary">
                    <th scope="col">Show Name</th>
                    <th scope="col">Price</th>
                    <th scope="col">Tickets Booked</th>
                    <th scope="col">Date</th>
                    <th scope="col">Show Screen</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="book in bookings" :key="book.booking_id">
                    <th scope="row">{{ book.shows.name }}</th>
                    <td>{{ book.shows.price }}</td>
                    <td>{{ book.shows.tickets }}</td>
                    <td>{{ book.shows.show_datetime }}</td>
                    <td>{{ book.shows.show_screen }}</td>
                    <td>
                        <button v-if="book.shows.past_show" @click="OpenDeleteBookingModal(book.booking_id)" class="btn btn-block btn-danger">Cancel</button>
                        <!-- <button v-else @click="OpenRatingModal" class="btn btn-block btn-success"> &#11088; Rate</button> -->
                        <button v-else @click="OpenRatingModal" class="btn btn-block btn-danger disabled">Cancel </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="modal fade" :class="{ 'show': DeleteBookingModal }" id="DeleteBookingModal" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ShowModalLabel" style="position: fixed;">Delete Show</h5>
                    <button @click="closeDeleteBookingModal" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="field">

                        <h3>Are you sure you want to Cancel your booking? </h3>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-success" @click="DeleteBooking">Yes</button>
                    <button class="btn btn-danger" data-bs-dismiss="modal" @click="closeDeleteBookingModal">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- </div> -->
</template>

<script>
export default {
    name: 'UserBookings',
    data() {
        return {
            bookings: [],
            bookingid: null,
            errormsg: '',
            DeleteBookingModal: false,

        }
    },
    methods: {
        OpenDeleteBookingModal(bookingid) {
            this.bookingid = bookingid;
            this.DeleteBookingModal = true;
        },
        closeDeleteBookingModal() {
            this.bookingid = null;
            this.DeleteBookingModal = false;
        },
        loadBookings() {
            fetch("http://127.0.0.1:5000/api/UserBookings", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            }).then((response) => {
                if (!response.ok) {
                    console.error("Response not ok");
                }
                return response.json();
            }).then((data) => {
                if (data) {
                    console.log(data.bookings);
                    this.bookings = data.bookings;
                    console.log(this.bookings);

                } else {
                    this.errormsg = data.msg;
                }
            }).catch((e) => {
                console.log(e);
            });
        },
        DeleteBooking() {
            console.log(this.bookings);
            const currentBooking = this.bookings.find(booking => booking.booking_id === this.bookingid);
            if (!currentBooking) {
                console.error("Booking not found");
                return;
            }

            fetch(`http://127.0.0.1:5000/api/UserBookings/${currentBooking.booking_id}`, {
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
                    if (data) {
                        console.log(data)
                    } else {
                        this.errormsg = data.msg;
                    }
                }).catch((e) => {
                    console.log(e);
                })
            .finally(() => {
                this.closeDeleteBookingModal();
                this.loadBookings(); // Assuming you have a function to close the modal after editing.
            });
        }
    },
    mounted() {
        this.loadBookings();
    },
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

.col-md-4 {
    padding: 0.5rem;
}

.plus {
    position: fixed;
    bottom: 5%;
    right: 2%;
}
</style>
