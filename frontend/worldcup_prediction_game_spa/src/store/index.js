import Vue from 'vue'
import Vuex from 'vuex'

// imports of AJAX functions go here
import { fetchMatchesWithPredictions } from '@/api'
import { submitLogin } from '@/api'
import { submitLogout } from '@/api'
import { isValidJwt, EventBus } from '@/utils'

Vue.use(Vuex)

const state = {
    // The state object will serve as the single source of truth where all
    // the important application-level data is contained within the store.
    // This state object will contain data that can be accessed and watched for
    // changes by any components interested in them such as the Home component.
    matches: [],
    userData: {},
    jwt: ''
}

const actions = {
    // The actions object is where I will define what are known as action methods.
    // Action methods are referred to as being "dispatched" and they're used to
    // handle asynchronous operations such as AJAX calls to an external service or API.
    loadMatchesWithPredictions(context, { jwt }) {
        return fetchMatchesWithPredictions(jwt)
            .then((response) => context.commit('setMatches', { matches: response.data }))
    },
    login(context, { username, password }) {
        return submitLogin(username, password)
            .then(response => {
                context.commit('setJwtToken', { jwt: response.data['token'] })
                context.commit('setUserData', { userData: response.data['user_data'] })
            })
            .catch(error => {
                console.log('Error Authenticating: ', error)
                EventBus.$emit('failedAuthentication', error)
            })
    },
    logout(context, { jwt }) {
        return submitLogout(jwt)
            .then(response => {
                context.commit('setJwtToken', { jwt: '' })
                context.commit('setUserData', { userData: {} })
            })
    }
}

const mutations = {
    // The mutations object provides methods which are referred to being "committed"
    // and serve as the one and only way to change the state of the data in the state object.
    // When a mutation is committed any components that are referencing
    // the now reactive data in the state object are updated with the new values, causing the UI to update and re-render its elements.
    setMatches(state, payload) {
        state.matches = payload.matches
    },
    setUserData(state, payload) {
        console.log('setUserData payload = ', payload)
        state.userData = payload.userData
    },
    setJwtToken(state, payload) {
        console.log('setJwtToken payload = ', payload)
        localStorage.token = payload.jwt
        state.jwt = payload.jwt
    }
}

const getters = {
    // The getters object contains methods also, but in this case they serve to
    // access the state data utilizing some logic to return information.
    // Getters are useful for reducing code duplication and promote reusability across many components.
    isAuthenticated (state) {
        return isValidJwt(state.jwt)
        // return isValidJwt(localStorage.token)
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store