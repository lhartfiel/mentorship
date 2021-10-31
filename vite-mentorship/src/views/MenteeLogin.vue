<template>
  <div class="container mx-auto px-1">
    <h1 class="text-3xl xl:text-7xl">Mentee Login: </h1>
    <form @submit.prevent="submit">
      <div class="flex justify-center flex-wrap">
        <label class="block w-full mr-3" for="username">Username:</label>
        <input id="username" type="text" name="username" v-model="form.username">
      </div>
      <div class="flex justify-center flex-wrap">
        <label class="block w-full mr-3" for="first_name">First Name:</label>
        <input id="first_name" type="text" name="full_name" v-model="form.first_name">
      </div>
      <div class="flex justify-center flex-wrap">
        <label class="block w-full mr-3" for="last_name">Last Name:</label>
        <input id="last_name" type="text" name="full_name" v-model="form.last_name">
      </div>
      <div class="flex justify-center flex-wrap">
        <label class="block w-full mr-3" for="password">Password:</label>
        <input id="password" type="password" name="password" v-model="form.password">
      </div>
      <button class="btn bg-green-500 text-white" type="submit"> Submit</button>
    </form>
  </div>

</template>

<script>

  export default {
    name: "MenteeLogin",

    data(){
      return {
        form: {
          username: "",
          first_name: "",
          last_name: "",
          password: "",
        },
      }
    },

    methods: {
      submit(){
        console.log('hi')
      }
    }
  }
</script>