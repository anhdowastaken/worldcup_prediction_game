<template>
    <div class="container">
        <div class="header clearfix">
            <nav>
                <ul class="nav nav-pills pull-right">
                    <li role="presentation"><logout></logout></li>
                </ul>
            </nav>
            <account-info></account-info>
        </div>

        <div class="row matches">
            <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import Logout from '@/components/Logout'
import AccountInfo from '@/components/AccountInfo'
import Match from '@/components/Match'

export default {
    name: 'Home',
    components: {
        Logout,
        AccountInfo,
        Match
    },
    data () {
        return {

        }
    },
    computed: mapState({
        matches: state => state.matches,
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return localStorage.jwt
            }
        }
    }),
    beforeMount() {
        this.$store.dispatch('loadMatchesWithPredictions', { jwt: this.jwt })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header,
.matches {
  padding-right: 15px;
  padding-left: 15px;
}

/* Custom page header */
.header {
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e5e5;
}
/* Make the masthead heading the same height as the navigation */
.header h3 {
  margin-top: 0;
  margin-bottom: 0;
  line-height: 40px;
}

/* Customize container */
@media (min-width: 768px) {
  .container {
    max-width: 730px;
    margin-top: 20px;
  }
}
.container-narrow > hr {
  margin: 20px 0;
}

/* Supporting matches content */
.matches {
  margin: 20px 0;
}

/* Responsive: Portrait tablets and up */
@media screen and (min-width: 768px) {
  /* Remove the padding we set earlier */
  .header,
  .matches {
    padding-right: 0;
    padding-left: 0;
  }
  /* Space out the masthead */
  .header {
    margin-bottom: 10px;
  }
}
</style>
