
// Make an add to school list button w ajax!

function schoolAdded() {
    (gray out button (or toggle checkbox if using))
}

function addSchoolToList(evt) {
   evt.preventDefault();

   var listInputs = {
        "user_id": $(" (user id from session) ").val()
        "school_id": $(" (school id from school in for loop) ").val()
        "admission_chance": $(" (safety, match, or stretch, hardcoded w/in for loop) ").val()
   }

   $.post('/add_school_to_list', listInputs, schoolAdded); 
}

$("#school_add_button").on("click", addSchoolToList);



