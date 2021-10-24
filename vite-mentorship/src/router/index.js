import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/components/Home.vue'
import Mentee from '/src/components/Mentee.vue'
import MenteeLogin from '/src/components/MenteeLogin.vue'
import MenteeSignup from '/src/components/MenteeSignup.vue'
import Mentor from '/src/components/Mentor.vue'
import MentorLogin from '/src/components/MentorLogin.vue'
import MentorSignup from '/src/components/MentorSignup.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
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