<template>
    <div class="loader">
        <div class="loader-bar"></div>
        <div class="loader-bar"></div>
        <div class="loader-bar"></div>
    </div>
</template>

<script>
export default {
    name: 'Loader',
    data() {
        return {

        }
    },
    methods: {

    }
}
</script>

<style scoped>
.loader {
    margin-top: 50px;
    text-align: center;
}
.loader-bar {
    display: inline-block;
    width: 4px;
    height: 20px;
    border-radius: 4px;
    animation: loading 1s ease-in-out infinite;
}
.loader-bar:nth-child(1) {
    background-color: rgba(0, 78, 161, 1);
    animation-delay: 0;
}
.loader-bar:nth-child(2) {
    background-color: rgba(134, 60, 186, 1);
    animation-delay: 0.09s;
}
.loader-bar:nth-child(3) {
    background-color: rgba(185, 35, 163, 1);
    animation-delay: .18s;
}

@keyframes loading {
    0% {
        transform: scale(1);
    }
    20% {
        transform: scale(1, 2.2);
    }
    40% {
        transform: scale(1);
    }
}
</style>
