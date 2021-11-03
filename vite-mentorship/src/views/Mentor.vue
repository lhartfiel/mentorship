<template>
  <h1>Welcome Mentors! What would you like to do?</h1>
  <div class="flex justify-center">
      <button @click="mentorLoginForm" class="btn bg-red-500 text-white mr-3">Login</button>
      <button @click="mentorSignupForm" class="btn bg-green-700 text-white mr-3">Signup</button>
  </div>
  <form @submit="mentorLoginSubmit" method="post" v-if="displayMentorLoginForm" class="flex flex-wrap justify-content-center">
    <div class="mb-5 w-full flex flex-wrap">
      <label class="w-full block" for="username">Username:</label>
      <input class="w-full block" type="text" id="username" name="username" v-model="username">
    </div>

    <div class="mb-5 w-full flex flex-wrap">
      <label class="w-full block" for="username">Password:</label>
      <input class="w-full block" type="password" id="password" name="password" v-model="password">
    </div>

    <button class="btn bg-indigo-500 text-white flex m-auto" @click.prevent="mentorLoginSubmit($event)">Submit</button>
  </form>

  <form @submit="mentorLoginSubmit" method="post" v-if="displayMentorSignupForm" class="flex flex-wrap justify-content-center">
     <div class="mb-5 w-full flex flex-wrap">
      <label for="signup-first-name" class="w-full block">First Name:</label>
      <input class="w-full block" type="text" id="signup-first-name" name="first-name" v-model="firstName" required>
    </div>

    <div class="mb-5 w-full flex flex-wrap">
      <label for="username" class="w-full block">Username:</label>
      <input class="w-full block" type="text" id="signup-username" name="username" v-model="username" required>
    </div>

     <div class="mb-5 w-full flex flex-wrap">
      <label class="w-full block" for="username">Email:</label>
      <input class="w-full block" type="email" id="email" size="30" v-model="email" required>
     </div>

    <div class="mb-5 w-full flex flex-wrap">
      <label class="w-full block" for="username">Password:</label>
      <input class="w-full block" type="password" id="signup-password" name="password" v-model="password" required>
    </div>

    <div class="mb-5 w-full flex flex-wrap">
      <label class="w-full block" for="username">Confirm Password:</label>
      <input class="w-full block" type="password" id="signup-password-confirm" name="password-confirm" v-model="passwordConfirm" required>
    </div>

    <button class="btn bg-indigo-500 text-white flex m-auto" @click.prevent="mentorSignupSubmit($event)">Submit</button>
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
        email: '',
        firstName: '',
        password: '',
        passwordConfirm: '',
        submissionSuccess: false,
        submissionMessage: '',
        username: '',
      }
    },

    methods: {
      mentorLoginForm(){
        this.displayMentorLoginForm = !this.displayMentorLoginForm
        this.displayMentorSignupForm = false
      },

      mentorLoginSubmit(){
        const username = this.username
        const password = this.password
        let self = this;
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
              self.$router.push({path: `/dashboard/user/${response.data.data.tokenAuth.user.id}`, props: {username: response.data.data.tokenAuth.user.username}})
            }
          })
          .catch(function(error){
            console.log(error.response)
          })
      },

      mentorSignupForm(){
        this.displayMentorSignupForm = !this.displayMentorSignupForm
        this.displayMentorLoginForm = false
      },

      mentorSignupSubmit(){
        const username = this.username
        const password = this.password
        const passwordConfirm = this.passwordConfirm
        const email = this.email
        const firstName = this.firstName
        axios({
            url: 'http://localhost:8000/graphql',
            method: 'post',
            data: {
              query:
                  `mutation
                  {
                    register(
                      firstName: "${firstName}",
                      isMentor: "True",
                      email: "${email}",
                      username: "${username}",
                      password1: "${password}",
                      password2: "${passwordConfirm}",
                    ) {
                        success,
                        errors,
                        token,
                        refreshToken,
                      }
                  }
                `
            }
          })
          .then((response) => {
            console.log(response.data)
            if(response.data.data.register.success === true) {
              this.submissionSuccess = true
              this.submissionMessage = `Thanks for signing up, ${this.username}`
              this.displayMentorSignupForm = false
            }
          })
          .catch(function(error){
            console.log(error.response)
          })
      },
    }
  }

</script>


<style>

  form {
    margin: 0 auto;
    max-width: 768px;
  }

</style>
