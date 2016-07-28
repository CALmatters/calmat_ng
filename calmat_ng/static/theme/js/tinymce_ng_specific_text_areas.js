//  Todo:  Generalize this with the tiny_mce inits
//  Todo:  use this selector across full site, and configure what fields in admin
tinymce.init({
  selector: 'fieldset.tinymce-editable textarea',
  extended_valid_elements:'script[language|type|src]',
  height: 500,
  plugins: [
    'advlist autolink lists link image imagetools charmap print preview anchor ',
    'searchreplace visualblocks code fullscreen textcolor ',
    'insertdatetime media table contextmenu paste code'
  ],
  file_picker_callback: function(callback, value, meta) {
        ImageLibraryPicker(callback, value, meta);
  },
  contextmenu: "image",
  toolbar: 'insertfile undo redo | styleselect | forecolor backcolor | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
  content_css: [
    '/static/css/tinymce_style.css'
  ],
   textcolor_map: [
    "000000", "Black",
    "993300", "Burnt orange",
    "333300", "Dark olive",
    "003300", "Dark green",
    "003366", "Dark azure",
    "000080", "Navy Blue",
    "333399", "Indigo",
    "333333", "Very dark gray",
    "800000", "Maroon",
    "FF6600", "Orange",
    "808000", "Olive",
    "008000", "Green",
    "008080", "Teal",
    "0000FF", "Blue",
    "666699", "Grayish blue",
    "808080", "Gray",
    "FF0000", "Red",
    "FF9900", "Amber",
    "99CC00", "Yellow green",
    "339966", "Sea green",
    "33CCCC", "Turquoise",
    "3366FF", "Royal blue",
    "800080", "Purple",
    "999999", "Medium gray",
    "FF00FF", "Magenta",
    "FFCC00", "Gold",
    "FFFF00", "Yellow",
    "00FF00", "Lime",
    "00FFFF", "Aqua",
    "00CCFF", "Sky blue",
    "993366", "Red violet",
    "FFFFFF", "White",
    "FF99CC", "Pink",
    "FFCC99", "Peach",
    "FFFF99", "Light yellow",
    "CCFFCC", "Pale green",
    "CCFFFF", "Pale cyan",
    "99CCFF", "Light sky blue",
    "CC99FF", "Plum"
  ]
});