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
      <div class="links flex">
        <a  class="px-6 bg-edit flex items-center"><img class="icon " :src=editIcon alt="Edit Icon"></a>
        <router-link class="px-6 flex items-center bg-arrow" :to="{ name: 'progress', params: { username: username, session_name: session_name }}">
          <img class="icon" :src=arrowRightIcon alt="Right Arrow Icon">
        </router-link>
      </div>
    </div>

    <a href="#" class="block mb-8" @click.prevent="addProgress">Add Progress +</a>
    <form @submit="createProgressInput" method="post" v-if="displayProgress" class="flex flex-wrap content-center">
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
    <a href="#" class="block w-full mt-3 mb-6 text-center btn bg-green-600 text-white text-center m-auto p-3" @click.prevent="createProgressInput($event)">Submit</a>
  </form>
  </div>

</template>

<script>
import moment from "moment";
import gql from 'graphql-tag';
import Edit from "../../icons/edit-solid.svg";
import ArrowRight from "../../icons/arrow-right-solid.svg";

const GET_PROGRESS = gql`query allProgress($username: String!, $sessionId: ID!){
    allProgress(username: $username, sessionId: $sessionId) {
      id
      summary
      comments
      dateStart
      dateEnd
      session {
        id
        name
        dateSessionStart
        dateSessionEnd
      }
      accomplishment {
        accomplishment
      }
    }
  }`

const ADD_PROGRESS = gql`mutation ($comments: String!, $summary: String!, $username: String!, $startDate: DateTime!, $endDate: DateTime!, $challenges: [ChallengeInput], $accomplishments: [AccomplishmentInput], $sessionId: Int, $sessionName: String){
  createProgressInput(progress: {dateStart: $startDate, dateEnd: $endDate, comments: $comments, summary: $summary}, challenges: $challenges, accomplishments: $accomplishments, session: {name: $sessionName, id: $sessionId}, username: $username){
    progress {
      comments
      summary
      id,
      dateStart,
      dateEnd,
      challenge {
        challenge
        id
        progress {
          id
        }
      }
      accomplishment {
        accomplishment
        id
        progress {
          id
        }
      }
      session {
        id
        name
        dateSessionStart
        dateSessionEnd
      }
    }
    ok
  }
}`;


export default {

  name: "Progress",

  props: ['username', 'id', 'session_name'],

  data(){
    return {
      accomplishment: '',
      accomplishments: [{accomplishment: ''}],
      arrowRightIcon: ArrowRight,
      createChallenge: false,
      challenge: '',
      challenges: [{challenge: ''}],
      createAccomplishment: false,
      comment: '',
      currentUser: this.username,
      displayProgress: false,
      editIcon: Edit,
      loggedInUser: '',
      allProgress: [],
      sessions: [],
      sessionId: parseInt(this.id),
      summary: '',
    }
  },

  apollo: {
    allProgress: {
      query: GET_PROGRESS,
      variables() {
        return {
          username: this.username,
          sessionId: this.sessionId
        }
      },
    },
  },

  created() {

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

    createProgressInput(event){
      this.$apollo.mutate({
        mutation: ADD_PROGRESS,
        variables: {
          comments: this.comment,
          summary: this.summary,
          accomplishments: this.accomplishments,
          challenges: this.challenges,
          username: this.username,
          startDate: moment(this.startDate).format(),
          endDate: moment(this.endDate).format(),
          sessionName: this.session_name,
          sessionId: this.sessionId
        },
        update: (cache, result) => {
          // the new post returned from the server
          let newProgress = result.data.createProgressInput.progress
          console.log("new")
          console.log(newProgress)
          // an "identification" needed to locate the right data in the cache
          let cacheId = {
            query: GET_PROGRESS,
            variables: { username: this.username, sessionId: this.sessionId },
          }

          // get the cached data
          const data = cache.readQuery(cacheId)

          const newData = [ ...data.allProgress, newProgress ]

          // update the cache with the new data
          cache.writeQuery({
            ...cacheId,
            data: { allProgress: newData }
          })
        },
        // optimisticResponse: {
        //   __typename: 'Mutation',
        //   createProgressInput: {
        //     __typename: 'CreateProgressInput',
        //     ok: true,
        //     progress: {
        //       comments: this.comment,
        //       summary: this.summary,
        //       challenge: {
        //         challenge: this.challenge,
        //         id: "challenge-",
        //         progress: {
        //           id: this.id
        //         }
        //       },
        //       accomplishment: {
        //         accomplishment: this.accomplishment,
        //         id: "accomplishment-",
        //         progress: {
        //           id: this.id
        //         }
        //       },
        //       session: {
        //         // id: this.allProgress[0].session.id,
        //         // name: this.allProgress[0].session.name,
        //         // dateSessionStart: this.allProgress[0].session.dateSessionStart,
        //         // dateSessionEnd: this.allProgress[0].session.dateSessionEnd
        //       },
        //       username: this.username,
        //       dateStart: moment(this.startDate).format(),
        //       dateEnd: moment(this.endDate).format(),
        //       id: this.id,
        //     },
        //     id: 'xyz-?',
        //   },
        // }
      }).then((data) => {
        // Result
        this.displayProgress = false
        console.log("data")
        console.log(data)
      }).catch((error) => {
        // Error
        console.log(error.clientErrors)
        console.log(error.message)
        console.log(error.extraInfo)
      })
    }
  }
}

</script>