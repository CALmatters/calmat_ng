tinymce.init({
  selector: 'textarea',
  extended_valid_elements:'script[language|type|src]',
  height: 500,
  plugins: [
    'advlist autolink lists link image imagetools charmap print preview anchor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code'
  ],
  file_picker_callback: function(callback, value, meta) {
        ImageLibraryPicker(callback, value, meta);
  },
  contextmenu: "image",
  toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
  content_css: [
    '/static/css/tinymce_style.css'
  ]
});