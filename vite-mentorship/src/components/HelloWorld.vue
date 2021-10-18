<template>
  <div>
    <h1>TMF Mentorship Program</h1>
    <h2>Login or Create Account:</h2>
    <button>I am a Mentee</button>
    <button>I am a Mentor</button>
    <br>
    <i>Testing out data returned from graphQL endpoint:</i>
    <h3>Meet the Mentees:</h3>
    <div v-for="item in mentees">
      <p>{{ item.mentee.mentee.firstName }}</p>
    </div>

    <h3>Meet the Mentors:</h3>
    <div v-for="item in allUsers">
      <p v-if="item.isMentor">{{ item.firstName }}</p>
    </div>
  </div>

</template>

<script>

import axios from "axios";

export default {
  name: "HelloWorld",

  data(){
    return {
      msg: 'Look here',
      mentees: {},
      allUsers: {}
    }
  },

  mounted(){
    axios({
      url: 'http://localhost:8000/graphql',
      method: 'post',
      data: {
        query:
        `
          {
            allMentees {
              mentee {
                mentee {
                    firstName
                }
              }
            }
            allUsers {
              mentee {
                mentee {
                  firstName
                }
              }
              isMentor
              isMentee
              firstName
              lastName
            }
          }

        `
      }
    })
    .then((response) => {
      console.log(response.data.data.allUsers)
        this.mentees = response.data.data.allMentees
        this.allUsers = response.data.data.allUsers

    })
    .catch(function(error){
      console.log(error.response)
    })
  }
}

</script>

<style scoped>
a {
  color: #42b983;
}
</style>
