
// Make an add to school list button w ajax!

function schoolAdded(data) {
    console.log(data);

    // $('#school_id').remove(); // This does not work!

    // how to use json object (data arg) to make individual button clicked disappear/etc ?

    // can we refer to id attribute defined dynamically w jinja?
    // can pass that back in as key or value in json object. how to use afterward?
    // want to gray out button and remove ability to click, hide button, or toggle checkbox if using
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
// could you gray out the button w an unclick here?
// tried & that doesn't work either. plus better design decision to do it after server response




