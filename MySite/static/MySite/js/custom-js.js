var num = 1;

function addQuestion() {
    var newdiv = document.createElement("div");
    newdiv.innerHTML = "<div id=\"question_" + (++num) + "\">\n" +
        "                    <label>\n" +
        "                        Вопрос " + num + "\n" +
        "                    </label>\n" +
        "                    <input type=\"text\" class=\"form-control\" required name='question_" + num + "'>\n" +
        "                    Ответы:\n" +
        "                    <div class=\"input-group mt-3 mb-3\">\n" +
        "                        <div class=\"input-group-prepend\">\n" +
        "                        <span class=\"input-group-text\">\n" +
        "                            <input type=\"checkbox\" name='checkbox_" + num + "_1'>\n" +
        "                        </span>\n" +
        "                        </div>\n" +
        "                        <input type=\"text\" class=\"form-control\" required name='answer_" + num + "_1'>\n" +
        "                    </div>\n" +
        "                </div>" +
        "                <div class=\"row\">\n" +
        "                    <a class=\"btn btn-secondary\" id='id_a_question_" + num + "' onclick='addAnswer("+num+")'>Добавить ответ</a>\n" +
        "                </div>\n" +
        "                <hr>"
    document.getElementById("questions").appendChild(newdiv);
    return false;

}

function addAnswer(x) {
    var elem = document.getElementById("question_"+x);
    var num_ans = (elem.getElementsByTagName('input').length - 1)/2 + 1
    var newdiv = document.createElement("div");
    newdiv.innerHTML = "<div class=\"input-group mt-3 mb-3\">\n" +
        "                        <div class=\"input-group-prepend\">\n" +
        "                        <span class=\"input-group-text\">\n" +
        "                            <input type=\"checkbox\" name='checkbox_"+ x + "_" + num_ans + "'>\n" +
        "                        </span>\n" +
        "                        </div>\n" +
        "                        <input type=\"text\" class=\"form-control\" required name='answer_" + x + "_" + num_ans + "'>\n" +
        "                    </div>"
    document.getElementById("question_"+x).appendChild(newdiv);
    return false;
}

$(document).ready(function(){
// = Вешаем событие прокрутки к нужному месту
    //   на все ссылки якорь которых начинается на #
    $('a[href^="#"]').bind('click.smoothscroll',function (e) {
        e.preventDefault();

        var target = this.hash,
        $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top-($('ul').height()+ 100)
        }, 900, 'swing', function () {
            window.location.hash = target;
        });
    });

});