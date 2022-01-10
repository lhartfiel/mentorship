import { createApp, provide, h } from 'vue'
import { ApolloClient, createHttpLink, InMemoryCache, gql, from } from '@apollo/client/core';
import { createApolloProvider } from '@vue/apollo-option'
import { onError } from "@apollo/client/link/error";
import App from './App.vue'
import router from "./router/index"
import './index.css'


const httpLink = createHttpLink({
  uri: 'http://localhost:8000/graphql',
  connectToDevTools: true
})

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );

  if (networkError) console.log(`[Network error]: ${networkError}`);
});


// Cache implementation
const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
  link: from([errorLink, httpLink]),
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

