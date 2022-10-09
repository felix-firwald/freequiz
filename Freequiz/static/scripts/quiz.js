console.log('script is starting now')

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
                quizBox.innerHTML += `
                    <br>
                `
                questions = response.questions
                questions.forEach(el => {
                    for (const [question, variants] of Object.entries(el)) {
                        quizBox.innerHTML += `
                            <div class="card shadow-sm col-4 top-50 start-50 translate-middle-x">
                                <div class="card-body">
                                    <div class="mb-2">
                                        <h4 class="card-title">${question}</h4>
                        `
                        variants.forEach(variant => {
                            quizBox.innerHTML += `
                                
                                    <div class="card-body">
                                        <div class="mb-2">
                                            <div class="form-check">
                                                <input 
                                                    type="checkbox"
                                                    class="form-check-input"
                                                    id="${question}-${variant}"
                                                    name="${question}"
                                                    value="${variant}"
                                                >
                                                <label class="form-check-label" for="${question}">${variant}</label>
                                            </div>
                            `
                        });
                        quizBox.innerHTML += `
                                    </div>
                                </div>    
                            </div>
                            <br>
                        `
                    }
                });
                quizBox.innerHTML += `
                    <div class="text-center">
                        <div class="container col-4">
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-outline-dark mt-3 ">Закончить тест</button>
                            </div>
                        </div>
                    </div>
                `
            },
            error: function(error) {
                console.log(error);
            }
        })
    })
});

console.log('script is ending now')