<template>
  <div class="container max-w-screen-md m-auto">
    <h1 class="text-6xl mb-6">Welcome, {{username}}!</h1>

    <h2 class="text-3xl">Sessions:</h2>
    <div class="sessions" v-for="(session, index) in allSessions" :key="`session-${session.id}`">
      <div class="flex justify-between b-shadow  my-6 text-left">
        <div class="session-info p-6">
          <h3 class="text-xl">{{ session.name }}</h3>
          <p class="mb-4" v-if="session.dateSessionStart">{{ dateFilter(session.dateSessionStart) }} - {{ dateFilter(session.dateSessionEnd) }}</p>
        </div>
        <div class="links flex">
          <a @click.prevent="editForm(index, session.dateSessionStart, session.dateSessionEnd, session.name, session.id)" class="px-6 bg-edit flex items-center"><img class="icon " :src=editIcon alt="Edit Icon"></a>
          <router-link class="px-6 flex items-center bg-arrow" :to="{ name: 'progress', params: { username: username, id: parseInt(session.id), session_name: session.name }}">
            <img class="icon" :src=arrowRightIcon alt="Right Arrow Icon">
          </router-link>
        </div>
      </div>

      <form @submit="editSessionInput" method="post" v-if="editSession && index === editIndex" class="flex flex-wrap content-center">
        <div class="mb-5 w-full flex flex-wrap">
          <label class="block w-full" for="edit-name">Session Name</label>
          <input class="block w-full" type="textarea" id="edit-name" v-model="editName" @change="editSessionInput($event)">
        </div>
        <div class="mb-5 w-full flex flex-wrap">
          <label class="block w-full" for="edit-startDate">Session Start Date</label>
          <input class="block w-full" type="date" id="edit-startDate" v-model="editStartDate" @change="editSessionInput($event)">
        </div>
        <div class="mb-5 w-full flex flex-wrap">
          <label class="block w-full" for="edit-endDate">Session End Date</label>
          <input class="block w-full" type="date" id="edit-endDate" v-model="editEndDate" @change="editSessionInput($event)">
        </div>
        <a href="#" class="block w-full mt-3 mb-6 text-center btn bg-green-600 text-white text-center m-auto p-3" @click.prevent="createSessionInput($event)">Submit</a>
      </form>
    </div>

    <a href="#" class="block mb-8" @click.prevent="addSession">Add Session +</a>

    <!--    Create Session Form-->
    <form @submit="createSessionInput" method="post" v-if="displaySession" class="flex flex-wrap content-center">
      <div class="mb-5 w-full flex flex-wrap">
        <label class="block w-full" for="name">Session Name</label>
        <input class="block w-full" type="textarea" id="name" v-model="name">
      </div>

      <div class="mb-5 w-full flex flex-wrap">
        <label class="block w-full" for="startDate">Session Start Date</label>
        <input class="block w-full" type="date" id="startDate" v-model="startDate">
      </div>
      <div class="mb-5 w-full flex flex-wrap">
        <label class="block w-full" for="startDate">Session End Date</label>
        <input class="block w-full" type="date" id="endDate" v-model="endDate">
      </div>
      <a href="#" class="block w-full mt-3 mb-6 text-center btn bg-green-600 text-white text-center m-auto p-3" @click.prevent="createSessionInput($event)">Submit</a>
    </form>
  </div>

</template>

<script>
import gql from 'graphql-tag'
import moment from 'moment'
import Edit from '../../icons/edit-solid.svg'
import ArrowRight from '../../icons/arrow-right-solid.svg'

const ADD_SESSION = gql`mutation ($id: Int, $name: String!, $dateSessionStart: DateTime!, $dateSessionEnd: DateTime!) {
  createSessionInput(session: {id: $id, name: $name, dateSessionStart: $dateSessionStart, dateSessionEnd: $dateSessionEnd}){
  session {
      name
      dateSessionStart
      dateSessionEnd
      id
    }
  }
}`

// const EDIT_SESSION = gql`mutation ($id: Int!, $name: String!, $dateSessionStart: DateTime!, $dateSessionEnd: DateTime!) {
//   createSessionInput(session: {id: $id, name: $name, dateSessionStart: $dateSessionStart, dateSessionEnd: $dateSessionEnd}){
//   session {
//       name
//       dateSessionStart
//       dateSessionEnd
//       id
//     }
//   }
// }`

const ALL_SESSIONS = gql`query allSessions{
  allSessions{
    name
    dateSessionStart
    dateSessionEnd
    id
  }
}`

export default {
  name: "Dashboard",

  props: ['username', 'test'],


  data(){
    return {
      allSessions: [],
      arrowRightIcon: ArrowRight,
      cachedData: {},
      currentUser: this.username,
      displaySession: false,
      editIndex: -1,
      editSession: false,
      editEndDate: "",
      editStartDate: "",
      editName: "",
      editId: Number,
      sessionProgress: false,
      showEditForm: false,
      editIcon: Edit,
      loggedInUser: '',
    }
  },

  apollo: {
    allSessions: {
      query: ALL_SESSIONS
    }
  },

  methods: {
    addSession(){
      this.displaySession = !this.displaySession
    },

    editForm(index, dateStart, dateEnd, name, id){
      this.editIndex = index
      this.editSession = !this.editSession
      this.editName = name
      this.editId = id
      this.editStartDate = moment(dateStart).format('YYYY-MM-DD')
      this.editEndDate = moment(dateEnd).format('YYYY-MM-DD')
    },

    dateFilter(value) {
      let date = value
      return moment(date).format('MMM Do, YYYY')
    },

    createSessionInput(){
      this.$apollo.mutate({
        mutation: ADD_SESSION,
        variables: {
          id: this.id,
          name: this.name,
          dateSessionStart: moment(this.startDate).format(),
          dateSessionEnd: moment(this.endDate).format(),
        },
        update: (cache, result) => {
          let newSession = result.data.createSessionInput
          this.cachedData = newSession
          // an "identification" needed to locate the right data in the cache
          let cacheId = {
            query: ALL_SESSIONS,
          }

          // get the cached data
          const data = cache.readQuery(cacheId)

          const newData = [ ...data.allSessions, newSession ]

          // update the cache with the new data
          cache.writeQuery({
            ...cacheId,
            data: { allSessions: newData }
          })
        },
        // optimisticResponse: { //This is not working
        //   __typename: 'CreateSessionInput',
        //   createSessionInput: {
        //     // ok: true,
        //     session: {
        //       __typename: 'SessionType',
        //       name: this.name,
        //       dateSessionStart: moment(this.dateSessionStart).format(),
        //       dateSessionEnd: moment(this.dateSessionEnd).format(),
        //       id: this.editId,
        //     },
        //   },
        // }
      }).then((data) => {
        // Result
        console.log(data)
        this.displaySession = !this.displaySession
        this.sessionProgress = false
      })
    },


    // TODO: May need to create a new schema for editing in order to pass the original ID; Otherwise a new entry is created.
    editSessionInput() {
      this.$apollo.mutate({
        mutation: ADD_SESSION,
        variables: {
          id: this.editId,
          name: this.editName,
          dateSessionStart: moment(this.editStartDate).format(),
          dateSessionEnd: moment(this.editEndDate).format(),
        },
        // update: (cache, result) => {
        //   this.editSession = !this.editSession
        //   // the updated post returned from the server
        //   console.log(result.data.createSessionInput.session)
        //   let updatedSession = result.data.createSessionInput.session
        //   this.cachedData = updatedSession
        //   // an "identification" needed to locate the right data in the cache
        //   let cacheId = {
        //     query: ALL_SESSIONS,
        //   }
        //
        //   // get the cached data
        //   const data = cache.readQuery(cacheId)
        //
        //   const newData = [data]
        //
        //
        //   cache.modify({
        //     allSessions(existing, {toReference}){
        //       return [...existingAllsessions, toReference(updatedSession)]
        //     }
        //   })
        //
        //   // update the cache with the new data
        //   cache.writeQuery({
        //     ...cacheId,
        //     data: {allSessions: newData}
        //   })
        //   // cache.writeData({
        //   //   ...cacheId,
        //   //   data: {allSessions: newData}
        //   // })
        // },
        // optimisticResponse: {
        //   __typename: 'Mutation',
        //   createSessionInput: {
        //     __typename: 'createSessionInput',
        //     ok: true,
        //     session: {
        //       name: this.editName,
        //       dateSessionStart: moment(this.editStartDate).format(),
        //       dateSessionEnd: moment(this.editEndDate).format(),
        //       id: this.editId,
        //     },
        //     id: 'id-'
        //   },
        // }
      }).then((data) => {
        // Result
        this.editSession = !this.editSession
        this.sessionProgress = false
        // console.log(data)
      })
    }

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

.icon {
  width: 48px;
}

.bg-edit {
  background-color: mediumpurple;
}

.bg-arrow {
  background-color: aquamarine;
}
</style>