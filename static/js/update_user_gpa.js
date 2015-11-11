// update user gpa

function callbackFunction(data){
    var obj = JSON.parse(data);
    $("span#user-gpa").replaceWith("data[0]");
}

function updateUserGpa(evt) {
    evt.preventDefault();

    var formInput = {
        "gpa": $("#gpa").val(),
    };

    console.log(formInput);

    $.post('/update_user_gpa.json', formInput, callbackFunction);
}

$("#update-gpa").on("submit", updateUserGpa);