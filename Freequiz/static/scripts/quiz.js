console.log('script is starting now')

const targettt = document.getElementById("timerDown");

const url = window.location.href

const quizBox = document.getElementById("quiz-box")

$(document).ready(function() {
            $('#startTest').click(function(e) {
                        var button = $(this);
                        button.disabled = true;
                        setTimeout(
                            button.slideUp(200),
                            1000
                        )
                        document.getElementById("tabulation").remove();
                        $.ajax({
                                    type: 'GET',
                                    url: `${url}data`,
                                    success: function(response) {
                                            console.log(response);
                                            let timer = response.timelimit

                                            var content_for_adding = `<br>`
                                            questions = response.questions

                                            if (questions.length == 0) {
                                                quizBox.innerHTML = `<br>
                    <div class="card shadow-sm col-4 bg-light top-50 start-50 translate-middle-x">
                        <div class="card-body">
                            <div class="mb-2">
                            <br>
                                <div class="container">
                                    <div class="row">
                                        <svg 
                                            xmlns="http://www.w3.org/2000/svg"
                                            width="80" 
                                            height="80"
                                            fill="#6c757d" 
                                            class="bi bi-slash-circle" 
                                            viewBox="0 0 16 16">
                                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path d="M11.354 4.646a.5.5 0 0 0-.708 0l-6 6a.5.5 0 0 0 .708.708l6-6a.5.5 0 0 0 0-.708z"/>
                                        </svg>
                                    </div>
                                </div><br>
                                <p class="text-center font-weight-light text-secondary">К сожалению, вопросов в тесте нет<br>Обратитесь с этой проблемой к автору</p>
                    `
                                            } else {
                                                qs = Object.entries(questions)
                                                for (var question of qs) {
                                                    content_for_adding += `
                                <div class="notification card shadow-sm col-4 border-0 top-50 start-50 translate-middle-x">
                                    <div class="card-body">
                                        <div class="mb-2">
                                            <h4 class="card-title">${question[0]}</h4><hr>
                            `
                                                    question[1].forEach(([id, text, type]) => {
                                                                if (text != null) {
                                                                    content_for_adding += `
                                            <div class="mb-2">
                                                <div class="form-check">
                                                    <input 
                                                        type="${type}"
                                                        class="${(type == 'text') ? 'form-control TEXT_INPUT': 'form-check-input VARIANT'}"
                                                        id="${id}"
                                                        name="${question}"
                                                        value="${(type == 'text') ? '' : text}"
                                                    >
                                                    ${(type == 'text') ? '': `<label class="form-check-label" for="${id}">${text}</label>`}
                                                </div>
                                            </div>
                                        `
                            }
                        });
                        content_for_adding += `
                                        </div>
                                    </div>    
                                </div>
                                <br>
                            `
                    }

                    quizBox.innerHTML += content_for_adding
                    quizBox.innerHTML += `
                        <div class="text-center">
                            <div class="container col-4">
                                <div class="d-grid gap-2">
                                    <button type="submit" class="btn btn-outline-dark rounded-pill">Закончить тест</button>
                                </div>
                            </div>
                        </div>
                    `


                    setInterval(updateCount, 1000);

                    function updateCount() {
                        const minutes = Math.floor(timer / 60);
                        let seconds = timer % 60;
                        seconds = seconds < 10 ? "0" + seconds : seconds;
                        text = `${minutes}:${seconds}`;
                        if ((minutes == 0) && (seconds == 0)) {
                            sendData();
                            targettt.innerHTML = `Время вышло!`;
                            quizBox.innerHTML = `<br>
                                <div class="text-center">
                                    <div class="container col-4">
                                        <div class="d-grid gap-2">
                                            <button type="submit" class="btn btn-outline-dark rounded-pill">Посмотреть результат</button>
                                        </div>
                                    </div>
                                </div>
                            `
                        } else {
                            targettt.innerHTML = text;
                            timer = timer - 1;
                        }
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        })
    })
});

const quizForm = document.getElementById("quiz-form")
const csrf = document.getElementsByName("csrfmiddlewaretoken")

function sendData() {

    const elements = [...document.getElementsByClassName("form-check-input VARIANT")];
    let data = {};
    data['csrfmiddlewaretoken'] = csrf[0].value
    let questions = [];
    elements.forEach(el => {
        if (el.checked) {
            questions.push(el.id)
        }
    })

    data.questions = questions
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: `${url}send_answer`,
        data: data,
        success: function(response) {
            console.log(response)
            targettt.remove()
            quizBox.innerHTML = `<br>
                <div class="text-center">
                    <div class="container col-4">
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-outline-dark rounded-pill">Посмотреть результат</button>
                        </div>
                    </div>
                </div>
            `
        },
        error: function(error) {
            console.log(error)
        }
    })
}
quizForm.addEventListener("submit", e => {
    e.preventDefault();

    sendData();
})

// if (data[el.name]) {
//    data[el.name].push(el.value)
//} else {
//    data[el.name] = [el.value]
//}