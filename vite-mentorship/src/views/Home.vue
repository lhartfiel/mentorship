<template>
  <div>
    <h1 class="text-5xl xl:text-7xl mb-4">TMF Mentorship Program</h1>
    <div class="flex justify-center">
      <router-link to="/mentee" class="btn bg-red-500 text-white mr-3">I am a Mentee</router-link>
      <router-link to="/mentor"  class="btn bg-indigo-500 text-white">I am a Mentor</router-link>
    </div>

    <br>
    <i>Testing out data returned from graphQL endpoint:</i>
    <h3>Meet the Mentees:</h3>
    <div v-for="item in allMentees">
      <p>{{ item.mentee.mentee.firstName }}</p>
    </div>

    <h3>Meet the Mentors:</h3>
    <div v-for="item in allUsers">
      <p v-if="item.isMentor">{{ item.firstName }}</p>
    </div>
  </div>

</template>

<script>

// import axios from "axios";
import gql from "graphql-tag";


export default {
  name: "Home",

  data(){
    return {
      msg: 'Look here',
      mentees: {},
      allMentees: {},
      allUsers: {}
    }
  },

  apollo: {
    allUsers: gql`query {
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
      }`,
    allMentees: gql`query{
      allMentees {
        mentee {
          mentee {
             firstName
          }
        }
      }
    }`
  },

  mounted(){
    // axios({
    //   url: 'http://localhost:8000/graphql',
    //   method: 'post',
    //   data: {
    //     query:
    //     `
    //       {
    //         allMentees {
    //           mentee {
    //             mentee {
    //                 firstName
    //             }
    //           }
    //         }
    //         allUsers {
    //           mentee {
    //             mentee {
    //               firstName
    //             }
    //           }
    //           isMentor
    //           isMentee
    //           firstName
    //           lastName
    //         }
    //       }
    //
    //     `
    //   }
    // })
    // .then((response) => {
    //   console.log(response.data.data.allUsers)
    //     this.mentees = response.data.data.allMentees
    //     this.allUsers = response.data.data.allUsers
    //
    // })
    // .catch(function(error){
    //   console.log(error.response)
    // })
  },

  // methods(){
  //
  // }
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

.btn {
  /*background: purple;*/
  border-radius: 4px;
  padding: 10px;
  text-decoration: none;
}
</style>
