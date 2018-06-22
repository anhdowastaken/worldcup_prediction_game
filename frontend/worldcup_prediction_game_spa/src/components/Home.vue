<template>
    <div>
        <move-top></move-top>
        <div class="header-background">
            <div class="header-background-under"></div>
        </div>

        <div class="container">
            <div class="header">
                <nav>
                    <ul class="nav nav-pills pull-left">
                        <li>
                            <span class="fa fa-user"
                                  style="font-size: 24px;
                                         color: white;
                                         margin-top: 5px;
                                         padding-right: 10px;
                                         border-right:  solid 2px white;
                                         padding-top: 2px;
                                         padding-bottom: 2px;
                                         cursor: pointer;"
                                  v-on:click.stop.prevent="goToUserCP()">
                            </span><span class="fa fa-trophy"
                                         style="font-size: 24px;
                                                color: white;
                                                margin-top: 5px;
                                                padding-left: 10px;
                                                padding-top: 2px;
                                                padding-bottom: 2px;
                                                cursor: pointer;"
                                         v-on:click.stop.prevent="goToRanking()"></span>
                        </li>
                    </ul>
                    <ul class="nav nav-pills pull-right">
                        <li><logout></logout></li>
                    </ul>
                </nav>
                <account-info></account-info>
            </div>

            <loader v-if="!isFetchingCompleted"></loader>
            <div v-else class="row matches">
                <match v-for="match in matches" v-bind:match="match" :key="match.num"></match>
            </div>
        </div>

    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'
import { key_jwt, key_user_data } from '@/common'
import Logout from '@/components/Logout'
import AccountInfo from '@/components/AccountInfo'
import Match from '@/components/Match'
import Loader from '@/components/Loader'
import MoveTop from '@/components/MoveTop'
import { fetchMatchesWithPredictions } from '@/api'

export default {
    name: 'Home',
    components: {
        Logout,
        AccountInfo,
        Match,
        Loader,
        MoveTop
    },
    data () {
        return {
            isFetchingCompleted: false
        }
    },
    computed: mapState({
        matches: state => state.matches,
        jwt: function(state) {
            if (state.jwt) {
                return state.jwt 
            } else {
                return localStorage.getItem(key_jwt)
            }
        }
    }),
    beforeMount() {
        fetchMatchesWithPredictions(this.jwt)
            .then((response) => {
                this.isFetchingCompleted = true
                if (response.status === 200) {
                    let matches = response.data
                    // Find most recent match
                    let found_most_recent = false
                    for (let i = 0; i < matches.length; i++) {
                        let match = matches[i]
                        let match_time = match.date.replace(/-/g, "/") + ' ' + match.time + ' ' + (match.timezone ? match.timezone : '')
                        let d = new Date(match_time)
                        let diff = d.getTime() - Date.now()
                        if (diff > 0) {
                            found_most_recent = true
                            match['most_recent'] = true
                            break
                        }
                    }
                    this.setMatches({ matches: matches })
                    if (found_most_recent) {
                        this.$nextTick(() => {
                            // FIXME: Should use pure JS instead of jQuery?
                            $('html, body').animate({ scrollTop: $('.match.most-recent').offset().top }, 2000)
                        })
                    }
                }
            })
            .catch(error => {
                this.isFetchingCompleted = true
                if (error.response.data['message']) {
                    this.setNotificationContent({ header: 'Error',
                                                  body: error.response.data['message'] })
                    this.showNotification()
                    // There is problem with authentication
                    // Back to login
                    if (error.response.status == 401) {
                        this.setNotificationRedirectAfterClose({ redirect: true,
                                                                 component_name: 'Login' })
                        this.$store.dispatch('logout')
                    }
                } else if (error) {
                    this.setNotificationContent({ header: 'Error',
                                                  body: error })
                    this.showNotification()
                } else {
                    this.setNotificationContent({ header: 'Error',
                                                  body: 'Error' })
                    this.showNotification()
                }
            })
    },
    methods: {
        ...mapMutations([
            'setMatches',
            'setNotificationContent',
            'showNotification',
            'setNotificationRedirectAfterClose'
        ]),
        goToUserCP: function() {
            this.$router.push({ name: 'UserCP' })
        },
        goToRanking: function() {
            this.$router.push({ name: 'Ranking' })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header-background {
    background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1));
    /* background: linear-gradient(to right,
                              rgba(0, 78, 161, 1),
                              rgba(134, 60, 186, 1),
                              rgba(185, 35, 163, 1)),
                url('../assets/header_background_image.png'); */
    /* background-image: url('../assets/header_background_image.png'); */
    /* background-size: contain; */
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

.header, .matches {
    padding-right: 5px;
    padding-left: 5px;
}

/* Custom page header */
.header {
    position: relative;
    padding-top: 10px;
    padding-bottom: 10px;
    height: 350px;
    min-height: 350px;
}

/* Customize container */
@media (min-width: 768px) {
    .container {
        max-width: 730px;
        margin-top: 20px;
    }
}

/* Supporting matches content */
.matches {
    margin: 10px 0;
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
