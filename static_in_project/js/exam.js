const url = window.location.href
const examBox = document.getElementById('exam-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')


const activateTimer = (time) => {
    console.log(time)
    if(time.toString().length < 2){
        timerBox.innerHTML = `<b>0${time}:00</b>`
    }else{
        timerBox.innerHTML = `<b>${time}:00</b>`
    }
    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds --
        if(seconds < 0){
            seconds = 59
            minutes --
        }
        if(minutes.toString().length < 2){
            displayMinutes = '0'+minutes
        }else{
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2){
            displaySeconds = '0'+seconds
        }else{
            displaySeconds = seconds
        }
        if(minutes === 0 && seconds === 0){
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')

            })
        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 500)
}
try{
$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        const data = response.data
        data.forEach(el => {
            for(const [question, answers] of Object.entries(el)){
                examBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    examBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question} - ${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        });
        activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    }
})}
catch (error) {
    console.log("################################# GRESKA #########################")
}

const examForm = document.getElementById('exam-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')