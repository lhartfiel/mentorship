<template>
  <div class="container max-w-screen-md m-auto">
    <h1 class="text-6xl mb-6">Welcome Mentor! {{username}}</h1>

    <h2 class="text-4xl">Current Progress:</h2>
    <div class="progress" v-for="item in progress">
      <div class="b-shadow p-3 my-3">
        <p class="mb-4" v-if="item.dateStart">{{ dateFilter(item.dateStart) }} - {{ dateFilter(item.dateEnd) }}</p>
        <p class="text-lg font-bold" v-if="item.comments">Comments:</p>
        <div class="comments" v-if="item.comments">
          <p>{{ item.comments }}</p>
        </div>

        <div class="summary" v-if="item.summary">
          <p class="text-lg font-bold">Summary:</p>
          <p v-html="item.summary"></p>
        </div>
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
    <div class="mb-5 w-full flex flex-wrap" v-if="addAccomplishment">
      <label class="block w-full" for="accomplishment">Accomplishment</label>
      <input class="block w-full" type="text" id="accomplishment" v-model="accomplishment">
    </div>
    <p class="block w-full">Challenges:</p>
    <a href="#" class="bg-indigo-500 text-white flex m-auto p-3" @click.prevent="showChallenge">Add Challenge</a>
    <div class="mb-5 w-full flex flex-wrap" v-if="addChallenge">
      <label class="block w-full" for="challenge">Challenge</label>
      <input class="block w-full" type="text" id="challenge" v-model="challenge">
    </div>
    <a href="#" class="block w-full mt-3 mb-6 text-center btn bg-green-600 text-white text-center m-auto p-3" @click.prevent="submitProgress($event)">Submit</a>
  </form>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: "Dashboard",

  props: ['username'],

  data(){
    return {
      accomplishment: '',
      addAccomplishment: false,
      addChallenge: false,
      challenge: '',
      comment: '',
      progress: [],
      summary: '',
      displayProgress: false
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
            allProgress {
              id
              summary
              comments
              dateStart
              dateEnd
              session {
                id
              }
            }
          }
        `
      }
    })
    .then((response) => {
      console.log(response.data.data.allProgress)
        this.progress = response.data.data.allProgress
    })
    .catch(function(error){
      console.log(error.response)
    })
  },

  methods: {
    addProgress(){
      this.displayProgress = !this.displayProgress
    },

    dateFilter(value){
      let date = value
      return moment(date).format('MMM Do, YYYY')
    },

    showAccomplishment(){
      this.displayProgress = true
      this.addAccomplishment = !this.addAccomplishment
    },

    showChallenge(){
      this.displayProgress = true
      this.addChallenge = !this.addChallenge
    },

    submitProgress(event){
      let comment = this.comment
      let summary = this.summary
      let accomplishment = this.accomplishment
      let challenge = this.challenge
      let startDate = moment(this.startDate).format()
      let endDate = moment(this.endDate).format()
      console.log(startDate)

      axios({
        url: 'http://localhost:8000/graphql',
        method: 'post',
        data: {
          query: `
            mutation {
              createProgressInput(progress: {dateStart: "${startDate}", dateEnd: "${endDate}", comments: "${comment}", summary: "${summary}"}, challenge: {challenge: "${challenge}"}, accomplishment: {accomplishment: "${accomplishment}"}){
                progress {
                  comments
                  summary
                  id
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
                    name
                    dateSessionStart
                    dateSessionEnd
                  }
                }
                ok
              }
            }
          `
        }
      })
      .then((response) => {
        console.log(response.data)
        console.log(response.data.ok)
        this.displayProgress = !this.displayProgress
      })
      .catch(function(error){
        console.log(error.response)
      })
    }
  }
}

</script>

<style>

.b-shadow {
  box-shadow: -1px 2px 15px -4px #BABABA;
}
</style>