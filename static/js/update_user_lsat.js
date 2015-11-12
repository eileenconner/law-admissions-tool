// update user lsat score

// replace text display with new lsat value
function lsatCallback(data){
    console.log(data["lsat"]);
    var replacementLsat = data["lsat"];
    $("span#user-lsat").text(replacementLsat);
}

// send new lsat data to route
function updateUserLsat(evt) {
    evt.preventDefault();

    var formInput = {
        "lsat": $("#lsat").val(),
    };

    $.post('/update_user_lsat.json', formInput, lsatCallback);
}

// on submit, update user lsat & display new value
$("#update-lsat").on("submit", updateUserLsat);