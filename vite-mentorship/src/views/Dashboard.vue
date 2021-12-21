<template>
  <div class="container max-w-screen-md m-auto">
    <h1 class="text-6xl mb-6">Welcome, {{username}}!</h1>

    <h2 class="text-3xl">Sessions:</h2>
    <div class="sessions" v-for="session in sessions">
      <div class="b-shadow p-3 my-3">
        <router-link :to="{ name: 'progress', params: { username: username, id: parseInt(session.id), session_name: session.name }}">
            <h3 class="text-xl">{{ session.name }}</h3>
            <p class="mb-4" v-if="session.dateSessionStart">{{ dateFilter(session.dateSessionStart) }} - {{ dateFilter(session.dateSessionEnd) }}</p>
        </router-link>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: "Dashboard",

  props: ['username', 'test'],

  data(){
    return {
      currentUser: this.username,
      loggedInUser: '',
      sessions: [],
    }
  },

  created(){
    axios({
      url: 'http://localhost:8000/graphql',
      method: 'post',
      data: {
        query:
          `
          {
            allSessions{
              dateSessionStart
              dateSessionEnd
              id
              name
            },
          }
        `
      }
    })
    .then((response) => {
      console.log(response.data)
        this.sessions = response.data.data.allSessions
        // this.progress = response.data.data.allProgress
        // this.loggedInUser = response.data.data.userAccess
    })
    .catch(function(error){
      console.log(error.response)
    })
  },

  methods: {
    dateFilter(value) {
      let date = value
      return moment(date).format('MMM Do, YYYY')
    },
  }

}

</script>

<style>
h1 {
  font-size: 3.6rem;
}

h2 {
  font-size: 2.4rem;
}

h3 {
  font-size: 2rem;
}

h4 {
  font-size: 1.8rem;
}

.b-shadow {
  box-shadow: -1px 2px 15px -4px #BABABA;
}

.inputBtn {
  font-size: 2rem;
  padding: 12px;
}
</style>