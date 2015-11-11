// update user lsat score

function callbackFunction(data){
    console.log(data);
}

function updateUserLsat(evt) {
    evt.preventDefault();

    var formInput = {
        "lsat": $("#lsat").val(),
    };

    console.log(formInput);

    $.post('/update_user_lsat.json', formInput, callbackFunction);
}

$("#update-lsat").on("submit", updateUserLsat);