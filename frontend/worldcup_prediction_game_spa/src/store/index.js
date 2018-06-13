import Vue from 'vue'
import Vuex from 'vuex'

// imports of AJAX functions go here
import { fetchMatchesWithPredictions } from '@/api'

Vue.use(Vuex)

const state = {
    // The state object will serve as the single source of truth where all
    // the important application-level data is contained within the store.
    // This state object will contain data that can be accessed and watched for
    // changes by any components interested in them such as the Home component.
    matches: []
}

const actions = {
    // The actions object is where I will define what are known as action methods.
    // Action methods are referred to as being "dispatched" and they're used to
    // handle asynchronous operations such as AJAX calls to an external service or API.
    loadMatchesWithPredictions: function(context, { user_id }) {
        return fetchMatchesWithPredictions(user_id)
            .then((response) => context.commit('setMatches', { matches: response.data }))
    }
}

const mutations = {
    // The mutations object provides methods which are referred to being "committed"
    // and serve as the one and only way to change the state of the data in the state object.
    // When a mutation is committed any components that are referencing
    // the now reactive data in the state object are updated with the new values, causing the UI to update and re-render its elements.
    setMatches(state, payload) {
        state.matches = payload.matches
    }
}

const getters = {
    // The getters object contains methods also, but in this case they serve to
    // access the state data utilizing some logic to return information.
    // Getters are useful for reducing code duplication and promote reusability across many components.
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store