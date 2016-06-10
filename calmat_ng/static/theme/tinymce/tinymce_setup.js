/*
    CALmatters customized version of the Mezzanine default
    TinyMCE editor config file originally found in the Mezzanine
    app `core/static/mezzanine/js/tinymce_setup.js`

    This file is specified to be used in `mezzcms/settings.py` via
    the TINYMCE_SETUP_JS setting.
*/

function CustomFileBrowser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        // file: window.__filebrowser_url + '?pop=2&type=' + type,
        file: '/admin/media_manager/mediaitem/?_popup=2',
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "yes",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no"
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}



jQuery(function($) {

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init({

            // main settings
            mode : "specific_textareas",
            editor_selector : "mceEditor",
            theme: "advanced",
            language: "en",
            dialog_type: "window",
            editor_deselector : "mceNoEditor",
            skin: "thebigreason",

            // general settings
            width: '800px',
            height: '450px',
            indentation : '10px',
            fix_list_elements : true,
            remove_script_host : true,
            accessibility_warnings : false,
            object_resizing: false,
            //cleanup: false, // SETTING THIS TO FALSE WILL BREAK EMBEDDING YOUTUBE VIDEOS
            forced_root_block: "p",
            remove_trailing_nbsp: true,

            external_link_list_url: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,

            // callbackss
            file_browser_callback: "CustomFileBrowser",

            // theme_advanced
            theme_advanced_toolbar_location: "top",
            theme_advanced_toolbar_align: "left",
            theme_advanced_statusbar_location: "",
            theme_advanced_buttons1: "example,|,bold,italic,|,link,unlink,|,image,|,media,charmap,|,code,|,table,|,bullist,numlist,blockquote,|,undo,redo,|,search,replace,|,fullscreen,|",
            theme_advanced_buttons2: "formatselect,styleselect",
            theme_advanced_buttons3: "",
            theme_advanced_path: false,
            theme_advanced_blockformats: "p,h1,h2,h3,h4,pre",
            theme_advanced_resizing : true,
            theme_advanced_resize_horizontal : false,
            theme_advanced_resizing_use_cookie : true,
            advlink_styles: "intern=internal;extern=external",

            /* IDMLOCO: Additional styles and config
               Style Formats: http://archive.tinymce.com/wiki.php/Configuration3x:style_formats
            ------------------------------------------------------------------------*/
            style_formats : [
                {title : 'Largest [p]', block: 'p', classes: 'cm_largest'},
                {title : 'Large [p]', block: 'p', classes: 'cm_large'},
                {title : 'Small [p]', block: 'p', classes: 'cm_small'},
                {title : 'Inline Styles'},
                {title : 'Largest text', inline: 'span', classes: 'cm_largest'},
                {title : 'Large text', inline: 'span', classes: 'cm_large'},
                {title : 'Small text', inline: 'span', classes: 'cm_small'},
                {title : 'Color styles'},
                {title : 'Orange text', inline: 'span', classes: 'cm_orange'},
                {title : 'Green text', inline: 'span', classes: 'cm_green'},
                {title : 'Blue text', inline: 'span', classes: 'cm_blue'},
                {title : 'Gray text', inline: 'span', classes: 'cm_gray'},
            ],

            // plugins
            plugins: "inlinepopups,contextmenu,tabfocus,searchreplace,fullscreen,advimage,advlink,paste,media,table,example",
            advimage_update_dimensions_onchange: true,
            
            // remove MS Word's inline styles when copying and pasting.
            paste_remove_spans: true,
            paste_auto_cleanup_on_paste : true,
            paste_remove_styles: true,
            paste_remove_styles_if_webkit: true,
            paste_strip_class_attributes: true,

            // don't strip anything since this is handled by bleach
            valid_elements: "+*[*]",
            valid_children: "+button[a]",

            // IDMLOCO:ronchambers what code to insert?
/*
            setup: function (editor) {
/*
                 editor.addButton('insertatom', {
                    title: 'Insert Atom',
                    icon: false,
                    menu: [
                        {text: 'Menu item 1', onclick: function() {editor.insertContent('Menu item 1');}},
                        {text: 'Menu item 2', onclick: function() {editor.insertContent('Menu item 2');}}
                    ]
                });
*/
/*
                editor.addButton('custominsert', {
                    icon: false,
                    text: 'Boom',
                    title: 'Insert Atomic Content',
                    onclick: function () {
                        editor.focus();
                        editor.label = ' Insert some Code';
                        editor.selection.setContent('[ atom ' + atom_id + ' display=');
                    }
                });
*/
//             },

            // IDMLOCO: Add custom style sheet for TinyMCE
            // -- http://archive.tinymce.com/wiki.php/Configuration3x:content_css
            content_css: window.__tinymce_css + ',' + "/static/theme/tinymce/css/custom_editor_styles.css",

    	});

    }

});
