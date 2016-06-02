
function handle_click(editor) {

  editor.windowManager.open(
      {
        file: '/static/theme/js/atom_chooser.html',
        width: 520 + parseInt(editor.getLang('example.delta_width', 0)),
        height: 350 + parseInt(editor.getLang('example.delta_height', 0)),
        inline: 1
      });
}


tinymce.PluginManager.add('atoms', function(editor, url) {


  editor.addButton('atoms', {
    text: 'Insert Atoms',
    icon: false,
    onclick: function() {
      handle_click(editor);
    }});

  // Adds a menu item to the tools menu
  editor.addMenuItem('atoms',
      {
    text: 'Insert Atoms',
    context: 'tools',
    onclick: function() {
        handle_click(editor);
    }}
  );

});