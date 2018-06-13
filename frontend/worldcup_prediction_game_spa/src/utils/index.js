import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt) {  
    if (!jwt || jwt.split('.').length < 3) {
        return false
    }
    
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
    const now = new Date()
    
    return now < exp
}

export function isEmpty(obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
        return false;
    }
    
    return JSON.stringify(obj) === JSON.stringify({});
}

export function msToTime(s) {
    let ms = s % 1000;
    s = (s - ms) / 1000;
    let secs = s % 60;
    s = (s - secs) / 60;
    let mins = s % 60;
    s = (s - mins) / 60
    let hrs = s % 24;
    let days = (s - hrs) / 24
    
    // return hrs + ':' + mins + ':' + secs + '.' + ms;
    return (days ? days + 'd:' : '') + (hrs ? hrs + 'h:' : '') + mins + 'm'
}

