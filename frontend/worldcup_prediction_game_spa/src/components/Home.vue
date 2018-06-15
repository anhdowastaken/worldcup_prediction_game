<template>
    <div>
        <div class="header-background">
            <div class="header-background-under"></div>
        </div>

        <div class="container">
            <div class="header">
                <nav>
                    <ul class="nav nav-pills pull-right">
                        <li><logout></logout></li>
                    </ul>
                </nav>
                <account-info></account-info>
            </div>

            <div class="row matches">
                <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
            </div>
        </div>

    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { key_jwt, key_user_data } from '@/common'
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
                return sessionStorage.getItem(key_jwt)
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
.header-background {
    background: linear-gradient(to right, #004EA1, #863CBA, #B923A3);
    height: 350px;
    min-height: 350px;
    position: absolute;
    z-index: -99;
    width: 100%;
}

.header-background-under {
    z-index: -100;
    opacity: 0.5;
    background: black;
    top: 0;
    height: 350px;
    min-height: 350px;
    position: absolute;
    width: 100%;
}

.header,
.matches {
  padding-right: 10px;
  padding-left: 10px;
}

/* Custom page header */
.header {
    position: relative;
    padding-top: 10px;
    padding-bottom: 10px;
    height: 350px;
    min-height: 350px;
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
/* .container-narrow > hr {
  margin: 20px 0;
} */

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
