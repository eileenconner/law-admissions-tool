
function submissionUpdated(data) {
    var schoolId = "span#" + data["school_id"];
    console.log(schoolId);

    $(schoolId).text("Yes");
}

// call route and pass it data 
function submitApp(evt) {
    evt.preventDefault();

    var appSubmitted = {
        "school_id": $(evt.currentTarget).data("schoolId")
    };

    console.log(appSubmitted);

    // disable button and change value on click
    $.post('/update_app_submission.json', appSubmitted, submissionUpdated);
    $(this).prop("disabled", true);
    $(this).attr("value", "Hooray! It's done!");
}

$(".app-submitted").on("click", submitApp);