
function submissionUpdated(data) {
    console.log(data);
    // changes all text spans to "yes"!
    //$("span#submitted").text("Yes");
}

// call route and pass it data 
function submitApp(evt) {
    evt.preventDefault();

    var appSubmitted = {
        // don't need app_submitted since can hardcode in the 1 value
        //"app_submitted": $(evt.currentTarget).data("appSubmitted"),
        "school_id": $(evt.currentTarget).data("schoolId")
    };

    console.log(appSubmitted);

    // disable button and change value on click
    $.post('/update_app_submission.json', appSubmitted, submissionUpdated);
    $(this).prop("disabled", true);
    $(this).attr("value", "Hooray! It's done!");
    //$(this).attr("span#submitted").text("Yes");
}


$(".app-submitted").on("click", submitApp);