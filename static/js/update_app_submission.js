
function submissionUpdated(data) {
    console.log(data);
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
    $(this).attr("value", "Application completed!");
}

$(".app-submitted").on("click", submitApp);