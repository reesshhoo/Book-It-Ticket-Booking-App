import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import AdminView from '../views/AdminView.vue'
import UserView from '../views/UserView.vue'
import RegisterComponent from '../components/RegisterComponent.vue'
import LoginComponent from '../components/LoginComponent.vue'
import AdminSummary from '../components/AdminSummary.vue'

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
    path: '/AdminSummary',
    name: 'AdminSummary',
    component: AdminSummary
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
