<template>
  <h1>Welcome Mentors! What would you like to do?</h1>
  <div class="flex justify-center">
      <button @click="mentorLoginForm" class="btn bg-red-500 text-white mr-3">Login</button>
      <button @click="mentorSignupForm" class="btn bg-green-700 text-white mr-3">Signup</button>
  </div>
  <form @submit="mentorLoginSubmit" method="post" v-if="displayMentorLoginForm">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" v-model="username">
     <label for="username">Password:</label>
    <input type="password" id="password" name="password" v-model="password">

    <button @click.prevent="mentorLoginSubmit($event)">Submit</button>
  </form>
  <h3 v-if="submissionSuccess" class="mt-6">{{ submissionMessage }}</h3>

</template>

<script>
  import axios from "axios";

  export default {
    name: 'Mentor',

    data(){
      return{
        displayMentorLoginForm: false,
        displayMentorSignupForm: false,
        username: '',
        password: '',
        submissionSuccess: false,
        submissionMessage: ''
      }
    },

    methods: {
      mentorLoginForm(){
        this.displayMentorLoginForm = !this.displayMentorLoginForm
      },

      mentorLoginSubmit(){
        const username = this.username
        const password = this.password
        alert(username)
        axios({
            url: 'http://localhost:8000/graphql',
            method: 'post',
            data: {
              query:
                  `mutation
                  {
                    tokenAuth(
                        username: "${username}"
                        password: "${password}"
                    ) {
                        success,
                        errors,
                        token,
                        refreshToken,
                        unarchiving,
                        user
                        {
                          id,
                          username
                        }
                      }
                  }
                `
            }
          })
          .then((response) => {
            console.log(response.data)
            if(response.data.data.tokenAuth.success) {
              this.submissionSuccess = true
              this.submissionMessage = `Thanks for logging in, ${response.data.data.tokenAuth.user.username}`
              this.displayMentorLoginForm = false
            }
          })
          .catch(function(error){
            console.log(error.response)
          })
      },

      mentorSignupForm(){
        this.displayMentorSignupForm = !this.displayMentorSignupForm
      },
    }
  }

</script>
