<template>
  <div class="container max-w-screen-md m-auto">
    <h2 class="text-4xl">Current Progress for {{ session_name }}:</h2>

    <div class="progress" v-for="item in allProgress">
      <div class="b-shadow p-3 my-3">
        <p class="mb-4" v-if="item.dateStart">{{ dateFilter(item.dateStart) }} - {{ dateFilter(item.dateEnd) }}</p>
        <p class="text-lg font-bold" v-if="item.accomplishment">Accomplishments:</p>
        <ul class="accomplishments" v-for="accomplishment in item.accomplishment">
          <li>{{ accomplishment.accomplishment }}</li>
        </ul>
        <p class="text-lg font-bold mt-4" v-if="item.comments">Comments:</p>
        <div class="comments" v-if="item.comments">
          <p>{{ item.comments }}</p>
        </div>

        <div class="summary mt-4 mb-4" v-if="item.summary">
          <p class="text-lg font-bold">Summary:</p>
          <p v-html="item.summary"></p>
        </div>
      </div>
    </div>

    <a href="#" class="block mb-8" @click.prevent="addProgress">Add Progress +</a>
    <form @submit="submitProgress" method="post" v-if="displayProgress" class="flex flex-wrap content-center">
    <div class="mb-5 w-full flex flex-wrap">
      <label class="block w-full" for="comment">Comments</label>
      <input class="block w-full" type="textarea" id="comment" name="comment" v-model="comment">
    </div>
    <div class="mb-5 w-full flex flex-wrap">
      <label class="block w-full" for="summary">Summary</label>
      <input class="block w-full" type="textarea" id="summary" v-model="summary">
    </div>
    <div class="mb-5 w-full flex flex-wrap">
      <label class="block w-full" for="startDate">Start Date</label>
      <input class="block w-full" type="date" id="startDate" v-model="startDate">
    </div>
    <div class="mb-5 w-full flex flex-wrap">
      <label class="block w-full" for="endDate">End Date</label>
      <input class="block w-full" type="date" id="endDate" v-model="endDate">
    </div>
    <p class="block w-full">Accomplishments:</p>
    <a href="#" class="bg-indigo-500 text-white flex m-auto p-3" @click.prevent="showAccomplishment">Add Accomplishment</a>
    <div class="mb-5 w-full flex flex-wrap" v-if="createAccomplishment">
      <template v-for="(accomplishment, index) in accomplishments">
        <label class="block w-full" for="accomplishment">Accomplishment</label>
        <div class="flex nowrap w-full">
          <input class="block w-full" type="text" id="accomplishment" v-model="accomplishment.accomplishment">
          <a class="inputBtn" href="#"  @click.prevent="addAccomplishment"> + </a>
          <a class="inputBtn" href="#" @click.prevent="removeAccomplishment(index)"> - </a>
        </div>
      </template>
    </div>
    <p class="block w-full">Challenges:</p>
    <a href="#" class="bg-indigo-500 text-white flex m-auto p-3" @click.prevent="showChallenge">Add Challenge</a>
    <div class="mb-5 w-full flex flex-wrap" v-if="createChallenge">
      <template v-for="(challenge, index) in challenges">
        <label class="block w-full" for="challenge">Challenge</label>
         <div class="flex nowrap w-full">
          <input class="block w-full" type="text" id="challenge" v-model="challenge.challenge">
          <a class="inputBtn" href="#"  @click.prevent="addChallenge"> + </a>
          <a class="inputBtn" href="#" @click.prevent="removeChallenge(index)"> - </a>
         </div>
      </template>
    </div>
    <a href="#" class="block w-full mt-3 mb-6 text-center btn bg-green-600 text-white text-center m-auto p-3" @click.prevent="submitProgress($event)">Submit</a>
  </form>
  </div>

</template>

<script>

import axios from "axios";
import moment from "moment";
import gql from 'graphql-tag';

export default {

  name: "Progress",

  props: ['username', 'id', 'session_name'],

  data(){
    return {
      accomplishment: '',
      accomplishments: [{accomplishment: ''}],
      createChallenge: false,
      challenge: '',
      challenges: [{'challenge': ''}],
      createAccomplishment: false,
      comment: '',
      currentUser: this.username,
      displayProgress: false,
      loggedInUser: '',
      // allProgress: [],
      sessions: [],
      sessionId: parseInt(this.id),
      summary: '',
    }
  },

  apollo: {
    allProgress: {
      query: gql`query allProgress($username: String!, $sessionId: ID!){
        allProgress(username: $username, sessionId: $sessionId) {
          id
          summary
          comments
          dateStart
          dateEnd
          session {
            id
          }
          accomplishment {
            accomplishment
          }
        }
      }`,
      variables() {
         console.log(this.sessionId)
        return {
          username: this.username,
          sessionId: this.sessionId
        }
      },
    }
    // update: data => data.allProgress
  },

  created() {




    // axios({
    //   url: 'http://localhost:8000/graphql',
    //   method: 'post',
    //   data: {
    //     query:
    //         `
    //       {
    //         allProgress(username: "${this.username}", sessionId: "${this.sessionId}") {
    //             id
    //             summary
    //             comments
    //             dateStart
    //             dateEnd
    //             session {
    //               id
    //             }
    //             accomplishment {
    //               accomplishment
    //             }
    //           }
    //         }
    //       `
    //   }
    // })
    // .then((response) => {
    //   console.log(response.data)
    //   this.progress = response.data.data.allProgress
    //   // this.loggedInUser = response.data.data.userAccess
    // })
    // .catch(function (error) {
    //   console.log(error.response)
    // })
  },

  methods: {
    addAccomplishment(){
      this.accomplishments.push({'accomplishment': ''})
    },

    addChallenge(){
      this.challenges.push({'challenge': ''})
    },

    addProgress(){
      this.displayProgress = !this.displayProgress
    },

    dateFilter(value){
      let date = value
      return moment(date).format('MMM Do, YYYY')
    },

    removeAccomplishment(index){
      this.accomplishments.splice(index,1)
    },

    removeChallenge(index){
      this.challenges.splice(index,1)
    },

    showAccomplishment(){
      this.displayProgress = true
      this.createAccomplishment = true
    },

    showChallenge(){
      this.displayProgress = true
      this.createChallenge = true
    },

    submitProgress(event){
      let comment = this.comment
      let summary = this.summary
      let accomplishments = this.accomplishments
      let challenges = this.challenges
      let username = this.username
      let startDate = moment(this.startDate).format()
      let endDate = moment(this.endDate).format()
      let axiosConfig = {
        headers: {
            'Content-Type': 'application/graphql',
        }
      };

      // apollo: {
      //   gql `
      //       mutation {
      //         createProgressInput(progress: {dateStart: "${startDate}", dateEnd: "${endDate}", comments: "${comment}", summary: "${summary}"}, challenge: {challenge: "${challenges}"}, accomplishments: ${JSON.stringify(accomplishments)}, session: { name:"Session 1 - Fall 2021/Winter 2022", id: 1}, username: "${username}"){
      //           progress {
      //             comments
      //             summary
      //             id
      //             challenge {
      //               challenge
      //               id
      //               progress {
      //                 id
      //               }
      //             }
      //             accomplishment {
      //               accomplishment
      //               id
      //               progress {
      //                 id
      //               }
      //             }
      //             session {
      //               name
      //               dateSessionStart
      //               dateSessionEnd
      //             }
      //           }
      //           ok
      //         }
      //       }
      //     `
      // }

      // TODO: Use Apollo to properly pass objects
      // axios({
      //   url: 'http://localhost:8000/graphql',
      //   method: 'post',
      //   data: {
      //     query: `
      //       mutation {
      //         createProgressInput(progress: {dateStart: "${startDate}", dateEnd: "${endDate}", comments: "${comment}", summary: "${summary}"}, challenge: {challenge: "${challenges}"}, accomplishments: ${JSON.stringify(accomplishments)}, session: { name:"Session 1 - Fall 2021/Winter 2022", id: 1}, username: "${username}"){
      //           progress {
      //             comments
      //             summary
      //             id
      //             challenge {
      //               challenge
      //               id
      //               progress {
      //                 id
      //               }
      //             }
      //             accomplishment {
      //               accomplishment
      //               id
      //               progress {
      //                 id
      //               }
      //             }
      //             session {
      //               name
      //               dateSessionStart
      //               dateSessionEnd
      //             }
      //           }
      //           ok
      //         }
      //       }
      //     `
      //   },
      //   axiosConfig
      // })
      // .then((response) => {
      //   console.log(response.data)
      //   console.log(response.data.ok)
      //   this.displayProgress = !this.displayProgress
      // })
      // .catch(function(error){
      //   console.log(error.response)
      // })
    }
  }
}

</script>