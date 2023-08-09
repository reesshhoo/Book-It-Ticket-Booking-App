<template>
<div class="dashboard">
    <div>
        <div class="row mt-3">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Total Venues</h5>
                        <p class="card-text">{{ venues.length }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Total Shows</h5>
                        <p class="card-text">{{ getTotalShowsCount }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <br>
    <div class="row mt-4">
        <div class="col-md-12 text-center">
            <h3 class="">Completed Shows</h3>
            <table class="table table-hover">
                <thead>
                    <tr class="table-secondary">
                        <th>Show Name</th>
                        <th>Show Date</th>
                        <th>Price</th>
                        <th>Tickets Sold</th>
                        <th></th>

                    </tr>
                </thead>
                <tbody>
                    <tr v-for="show in pastShows" :key="show.show_id">
                        <td>{{ show.name }}</td>
                        <td>{{ show.show_datetime }}</td>
                        <td>{{ show.price }}</td>
                        <td>{{ show.seats_booked }}</td>
                        <td style="width:30%">
                            <div class="progress">
                                <div class="progress-bar progress-bar-striped" role="progressbar" :style="getProgressBarStyle(show)" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: 'AdminSummary',
    data() {
        return {
            venues: [],
        }
    },
    methods: {
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
        getProgressBarStyle(show) {
            const progressWidth = (show.seats_booked * 100) / show.seats_available;
            return `width: ${progressWidth}%;`;
        }

    },
    computed: {
        getTotalShowsCount() {
            let totalShows = 0;
            this.venues.forEach((venue) => {
                totalShows += venue.shows.shows.length;
            });
            return totalShows;
        },
        pastShows() {
            const pastShows = [];
            this.venues.forEach((venue) => {
                venue.shows.shows.forEach((show) => {
                    if (show.past_show) {
                        pastShows.push(show);
                    }
                });
            });
            console.log(pastShows)
            return pastShows;
        }
    },
    mounted() {
        this.loadvenues();
    }
}
</script>

<style scoped>
.dashboard {
    position: relative;
}
</style>
