// let user remove a school from their list of selected schools.

function schoolRemoved(data) {
    // remove entire <li> element for removed school
    var schoolId = "li#" + data["school_removed"];
    console.log(schoolId);
    $(schoolId).remove();

}

function removeSchool(evt) {
    evt.preventDefault();

    var removeThisSchool = {
        "school_id": $(evt.currentTarget).data("schoolIdNum")
    };

    console.log(removeThisSchool);

    $.post('/remove_school.json', removeThisSchool, schoolRemoved);
}

$(".school-remove").on("click", removeSchool);