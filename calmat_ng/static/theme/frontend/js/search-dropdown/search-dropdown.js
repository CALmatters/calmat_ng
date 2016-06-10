/*
* searchDropdown converts select elements and converts them into searchable dropdown menues.
* This was created as a response to dropdown menus becoming too large to easily find the
* article the user wants to select.
*
* This module requires the zelect.js jQuery library. It also requires the custom-made
* search-dropdown.css stylesheet to appear correctly.
*
* At the moment this module only targets 'select' elements within .dynamic-inline divs.
* Further modification to this code will be required to have it target other select elements
* in the DOM.
*
*/

var searchDropdown = {
    variables: {
        allBlogPostsWithAuthor: []
    },
    
    settings: {
        zelect: { // other zelect settings can be found here: https://github.com/mtkopone/zelect
            throttle: 0
        }
    },

    selectors: {
        $dynamic_fieldset__select: function(){
            return "select#id_article";
        },
        $dynamic_inline__select: function(){
            return "select[id^='id_related_post']";
        },
        $zelect: function(){
            return jQuery("div.zelect");
        }
    },
    
    init: function(){
        var self = this;

        this.getAllBlogPosts(function(data){
            //  Add author to already on-page Article options
            self.appendAdditionalBlogDataToOptions(self.selectors.$dynamic_fieldset__select());
            self.appendAdditionalBlogDataToOptions(self.selectors.$dynamic_inline__select());

            //  Make zelect convert it to be searchable
            jQuery(self.selectors.$dynamic_fieldset__select()).zelect(self.settings.zelect);
            jQuery(self.selectors.$dynamic_inline__select()).zelect(self.settings.zelect);

            self.renderArrowIcons();
        });
        
        
    },
    
    // This will prepend arrow svg's to the DOM so users intuitively know it is a dropdown menu.
    renderArrowIcons: function(){
        var self = this,
            $zelect = this.selectors.$zelect(),
            img_src = "/static/theme/frontend/img/search-dropdown/arrow-icon.svg";
        
        $zelect.prepend(
            "<img src='" + img_src + "' class=\"zelect__up-arrow arrow\">"
            + "<img src='" + img_src + "' class=\"zelect__down-arrow arrow\">"
        );
    },
    
    // Makes an API call to '/api/all-blog-posts-with-author/' to retrieve additional data about each article that we will appened.
    getAllBlogPosts: function(callback){
        var self = this;
        
        jQuery.ajax({
            url: '/api/all-blog-posts-with-author/',
            success: function(data){
                self.variables.allBlogPostsWithAuthor = data;
                callback(data);
            },
            error: function(err){
                callback(err);
            }
        })
    },
    
    /*
    * This will loop through all option elements in the DOM within .dynamic-line.
    * It will compair the the 'value' attribute of each option element, which is technically the article id, with
    * the id found allBlogPostsWithAuthor. 'allBlogPostsWithAuthor' is the json data retrieved earlier from
    * the api. If a match is found, the additional data will be added to the element innerHTML.
    *
    * Essentially this will convert an option element like <option value="91">News Analysis: More than friends?</option>
    * into <option value="91">Laurel Rosenhall | News Analysis |  More than friends?</option> so it is entirely searchable.
    */
    appendAdditionalBlogDataToOptions: function(q){
        var self = this,
            allOptions = document.querySelectorAll(q);
        
        for(var i=0, allOptionLength = allOptions.length; i < allOptionLength; i++){
            var _optionValue = allOptions[i].getAttribute('value'),
                _optionText = allOptions[i].text,
                allBlogPosts = self.variables.allBlogPostsWithAuthor;
                
                for(e in allBlogPosts){
                    var _blogPostID = allBlogPosts[e]['id'],
                        _blogPostAuthor = (allBlogPosts[e]['authors'] == null) ? "":allBlogPosts[e]['authors'] + " | ";
                    
                    if(_optionValue == _blogPostID){
                        allOptions[i].innerHTML = _blogPostAuthor + _optionText.replace(':',' | ')
                    }
                }
        }
    }
    
};