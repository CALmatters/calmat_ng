tinymce.PluginManager.add('atoms', function(editor, url) {


  editor.addButton('atoms', {
    text: 'Insert Atoms',
    icon: false,
    onclick: function() {
      // Open window
      editor.windowManager.open({
        title: 'Insert Atoms Button',
        body: [
          {type: 'textbox', name: 'title', label: 'Title'}
        ],
        onsubmit: function(e) {
          // Insert content when the window form is submitted
          editor.insertContent('Title: ' + e.data.title);
        }
      });
    }
  });

  // Adds a menu item to the tools menu
  editor.addMenuItem('atoms',
      {
    text: 'Insert Atoms',
    context: 'tools',
    onclick: function() {
      // Open window with a specific url
      editor.windowManager.open(
          {
            file: '/static/theme/js/atom_chooser.html',
            width: 520 + parseInt(editor.getLang('example.delta_width', 0)),
            height: 350 + parseInt(editor.getLang('example.delta_height', 0)),
            inline: 1
          }, {
            plugin_url: url, // Plugin absolute URL
            some_custom_arg: 'custom arg' // Custom argument
          });
    }}
  );

});