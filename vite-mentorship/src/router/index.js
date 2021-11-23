import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/views//Home.vue'
import Mentee from '/src/views/Mentee.vue'
import MenteeLogin from '/src/views/MenteeLogin.vue'
import MenteeSignup from '/src/views/MenteeSignup.vue'
import Mentor from '/src/views/Mentor.vue'
import MentorLogin from '/src/views/MentorLogin.vue'
import MentorSignup from '/src/views/MentorSignup.vue'
import Dashboard from '/src/views/Dashboard.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },

     {
        path: '/dashboard/user/:username',
        name: 'dashboard',
        component: Dashboard,
        props: true,
        params: true
    },
    {
        path: '/mentee',
        name: 'mentee',
        component: Mentee,
    },
    {
        path: '/mentee/login',
        name: 'menteeLogin',
        component: MenteeLogin,
    },
    {
        path: '/mentee/signup',
        name: 'menteeSignup',
        component: MenteeSignup,
    },
    {
        path: '/mentor',
        name: 'mentor',
        component: Mentor,
    },
    {
        path: '/mentor/login',
        name: 'mentorLogin',
        component: MentorLogin,
    },
    {
        path: '/mentor/signup',
        name: 'mentorSignup',
        component: MentorSignup,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router