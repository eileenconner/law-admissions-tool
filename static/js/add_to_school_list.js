// Make an add to school list button w ajax

function schoolAdded(data) {
    console.log(data);

}

// add school to list in database
function addSchoolToList(evt) {
   evt.preventDefault();

   var listInputs = {
        "school_id": $(evt.currentTarget).data("schoolId"),
        "admission_chance": $(evt.currentTarget).data("admissionChance")
   };

   console.log(listInputs);

   // add school to School_list for user and disable button
   $.post('/add_school_to_list', listInputs, schoolAdded);
   $(this).prop("disabled", true);
   $(this).attr("value", "Added to your list");
}

$(".school_add_button").on("click", addSchoolToList);
