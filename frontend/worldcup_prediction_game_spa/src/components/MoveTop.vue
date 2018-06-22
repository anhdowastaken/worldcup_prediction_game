<template>
    <div class="fa fa-angle-double-up move-top-button"
         v-on:click.stop.prevent="moveTop()"></div>
</template>

<script>
export default {
    name: 'MoveTop',
    data() {
        return {

        }
    },
    methods: {
        moveTop: function() {
            // FIXME: Should use pure JS instead of jQuery?
            // window.scrollTo(0, 0)
            this.$nextTick(() => {
                $('html, body').animate({ scrollTop: 0 }, 1000)
            })
        }
    }
}
</script>

<style scoped>
.move-top-button {
    position: fixed;
    bottom: 0;
    right: 0;
    font-size: 30px;
    margin-right: 2px;
    margin-bottom: 15px;
    color: #3B5998;
    z-index: 9999;
    cursor: pointer;
}
</style>
