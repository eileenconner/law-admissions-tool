function callbackFunction(data){
    console.log(data);
}

function updateUserStats(evt) {
    evt.preventDefault();

    var listInputs = {
        "gpa": $("#gpa").val(),
        "lsat": $("#lsat").val()
    };

    console.log(listInputs);

    $.post('/update_user_stats.json', listInputs, callbackFunction);
}

$("#update-stats").on("submit", updateUserStats);