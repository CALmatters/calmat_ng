



// var args = top.tinymce.activeEditor.windowManager.getParams();
//
// console.log(args);

var f = document.forms[0];
// Get atoms by select element options in parent window dialog.
var atom_m2m_selections = window.parent.document.getElementById('id_atoms_to').childNodes;
// Clone the child <option> elements into a new array.
var atoms = [];
for (i = 0; i < atom_m2m_selections.length; i++) {
        atoms[i] = atom_m2m_selections[i].cloneNode(true);
}
// Define the select elements for choosing atom params.
var atom_select = document.getElementById('atomSelect');
var atom_display_select = document.getElementById('atomDisplaySelect');

// Remove the placeholder options.
var placeholder = atom_select.options[0];
atom_select.removeChild(placeholder);

// Append all atom options (with IDs as values) to atom dropdown element.
for (i = 0; i < atoms.length; i++) {
        atom_select.appendChild(atoms[i]);
}

var insert_btn = document.getElementById('insert');
insert_btn.addEventListener('click', function(evt){

        var f = document.forms[0];
        // Get selected atom ID from form dropdown.
        var selected_atom_id = f.atomselect.options[f.atomselect.selectedIndex].value;
        // Get selected atom display type from form dropdown.
        var display_type = f.atomdisplayselect.options[f.atomdisplayselect.selectedIndex].value;
        // Build the shortcode.
        var shortcode = '[ atom ' + selected_atom_id +  ' display=' + display_type + ' ]';

        console.log(shortcode);

        // 	// Insert the shortcode at cursor.
        top.tinymce.activeEditor.execCommand('mceInsertContent', false, shortcode);
        top.tinymce.activeEditor.windowManager.close();

});

