import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import AdminView from '../views/AdminView.vue'
import UserView from '../views/UserView.vue'
import UserBookingView from '../views/UserBookingView.vue'
import RegisterComponent from '../components/RegisterComponent.vue'
import LoginComponent from '../components/LoginComponent.vue'
import AdminSummaryView from '../views/AdminSummaryView.vue'
// import UserDashboard from '../components/UserDashboard.vue'
import SearchComponent from '../components/SearchComponent.vue'

const routes = [
  {
    path: '/',
    name: 'LoginComponent',
    component: LoginComponent
  },
  {
    path: '/Register',
    name: 'RegisterComponent',
    component: RegisterComponent
  },
  {
    path: '/Admin_View',
    name: 'AdminView',
    component: AdminView
  },
  {
    path: '/User_View',
    name: 'User_view',
    component: UserView
  },
  {
    path: '/Admin_Summary_view',
    name: 'AdminSummaryView',
    component: AdminSummaryView
  },
  
  {
    path: '/User_Bookings',
    name: 'UserBookingView',
    component: UserBookingView
  },
  {
    path: '/search/:search',
    name: 'Search page',
    component: SearchComponent
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
