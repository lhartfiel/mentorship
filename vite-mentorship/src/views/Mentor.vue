<template>
  <h1>Welcome Mentors! What would you like to do?</h1>
  <div class="flex justify-center">
      <button @click="mentorLoginForm" class="btn bg-red-500 text-white mr-3">Login</button>
      <button @click="mentorSignupForm" class="btn bg-green-700 text-white mr-3">Signup</button>
  </div>
  <form @submit="mentorLoginSubmit" method="post" v-if="displayMentorLoginForm" v-model="mentorLogin">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username">

     <label for="username">Password:</label>
    <input type="password" id="password" name="password">

    <input type="submit" value="Login">
  </form>

</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Mentor',

    data(){
      return{
        displayMentorLoginForm: false,
        displayMentorSignupForm: false
      }
    },

    methods: {
      mentorLoginForm(){
        this.displayMentorLoginForm = !this.displayMentorLoginForm
      },

      mentorLoginSubmit(){
        axios.post()
      },

      mentorSignupForm(){
        this.displayMentorSignupForm = !this.displayMentorSignupForm
      }
    }
  }

</script>
