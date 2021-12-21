import { createApp, provide, h } from 'vue'
import { ApolloClient, createHttpLink, InMemoryCache, gql } from '@apollo/client/core';
import { createApolloProvider } from '@vue/apollo-option'
import App from './App.vue'
import router from "./router/index"
import './index.css'


const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: 'http://localhost:8000/graphql',
  connectToDevTools: true
})

// Cache implementation
const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
  link: httpLink,
  cache
})

const apolloProvider = createApolloProvider({
  defaultClient: apolloClient,
})

const app  = createApp({
    render: ()=>h(App)
});
app.component('App', App)
app.use(apolloProvider)
app.use(router)
app.mount('#app')

