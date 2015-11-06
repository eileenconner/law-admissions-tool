
// Make an add to school list button w ajax!

function schoolAdded(data) {
    console.log("It worked!");
    //(gray out button and remove ability to click, hide button, or toggle checkbox if using
}

// add school to list in database
function addSchoolToList(evt) {
   evt.preventDefault();

   var listInputs = {
        "school_id": $(evt.currentTarget).data("schoolId"),
        "admission_chance": $(evt.currentTarget).data("admissionChance")
   };

   console.log(listInputs);

   $.post('/add_school_to_list', listInputs, schoolAdded);
}

$(".school_add_button").on("click", addSchoolToList);



