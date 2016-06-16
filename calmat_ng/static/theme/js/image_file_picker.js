function ImageLibraryPicker(callback, value, meta) {

    var image_url = "/admin/media_manager/mediaitem/?_popup=1000";

    tinyMCE.activeEditor.windowManager.open({
        file : image_url,
        title : 'Image Browser',
        width : 1200,
        height : 800,
        resizable : "yes",
        inline : "yes",
        close_previous : "no"
    }, {
          oninsert: function (url) {
            callback(url);
          }
        }
    );
}
