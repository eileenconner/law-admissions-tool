// update user gpa

// replace text display with new gpa value
function gpaCallback(data){
    console.log(data["gpa"]);
    var replacementGpa = data["gpa"];
    $("span#user-gpa").text(replacementGpa);
}

// send new gpa data to route
function updateUserGpa(evt) {
    evt.preventDefault();

    var formInput = {
        "gpa": $("#gpa").val(),
    };

    $.post('/update_user_gpa.json', formInput, gpaCallback);
}

// on submit, update user gpa & display new value
$("#update-gpa").on("submit", updateUserGpa);