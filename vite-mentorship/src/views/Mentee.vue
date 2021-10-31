
<template>
  <h1 class="text-3xl xl:text-7xl">Mentee!</h1>
  <div class="flex justify-center">
    <router-link to="/mentee/login" class="btn bg-red-500 text-white mr-3">Login!</router-link>
    <router-link to="/mentor/signup"  class="btn bg-indigo-500 text-white">Sign Up!</router-link>
  </div>

</template>

<script>

export default {
  name: "Mentee",
}

</script>
