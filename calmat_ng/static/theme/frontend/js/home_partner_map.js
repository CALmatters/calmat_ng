/* Map init
-----------------------------------------------------*/

// Access Token
L.mapbox.accessToken = 'pk.eyJ1IjoiY2FsbWF0dGVycyIsImEiOiJjaXEzMDNra2UwMWE4Zmhubm96Zmt4MmF6In0.xObupd_m6jENGrLbrYuuVQ';

// Build Mapbox object
var map = L.mapbox.map('partnerMap', null, {
        minZoom: 5,
        maxZoom: 9,
    }).setView([37.5, -119.5], 6);

// Disable map settings
map.scrollWheelZoom.disable();
map.doubleClickZoom.disable();

// Set custom California tile layer
var styleLayer = L.mapbox.styleLayer('mapbox://styles/calmatters/ciq4fg3z10078bem5fox82d1y');
styleLayer.addTo(map);

// All sidebar partner links
var $partnerList = jQuery('#partnerList a.maplink');


/* Partner locations
-----------------------------------------------------*/

var partnerLayer = L.mapbox.featureLayer();

partnerLayer.on('layeradd', function(e){
    var marker = e.layer,
        feature = marker.feature,
        icon = feature.properties.icon;

        // class_name = 'partner-marker-icon' + ' partner-marker-' + feature.properties.partner_type;

    marker.setIcon(L.divIcon(icon));
    // marker.setIcon(L.divIcon(feature.properties.icon));
});

// Load geoJsonData, from home view `partner_map`
partnerLayer.setGeoJSON(geoJsonData) // geoJsonData from home view
            .eachLayer(function(partner){
                // Get marker id (i.e. slug) from properties
                var slug = partner.feature.properties.slug;
                // Find the sidebar link and add click event handler
                $partnerList.filter('#'+slug)
                    .on('click', function(evt){
                        evt.preventDefault();
                        var $this = jQuery(this) // sidebar link <a>

                        // Clear map and links if clicked twice
                        if( $this.hasClass('active') ){
                            clear_map();
                            $this.blur();
                        }
                        else {
                        // Update map
                            // Clear active marker
                            clear_active_markers();
                            // Set active class
                            partner._icon.className += ' active';
                            // Center map on marker
                            // map.setView(partner.getLatLng(), 6);
                            // Build tooltip content markup
                            toggle_tooltip( build_tooltip( partner.feature ) );
                            // Update sidebar link active
                            $partnerList.removeClass('active');
                            $this.addClass('active');                                    
                        }
                    });
            })
            .addTo(map);


/* Tool Tips
-----------------------------------------------------*/

var $info = jQuery('#partnerInfo');
var $imageList = jQuery('#partnerImgList');

var active_class = ' active';

// Marker hover action
partnerLayer.on('mouseover', function(e) {
    // Force the popup closed.
    e.layer.closePopup();

    // Clear active classes
    clear_active_markers();

    // Update icon class for active state
    e.layer._icon.className += active_class;

    // Build tooltip content markup
    toggle_tooltip( build_tooltip( e.layer.feature ) );

    // Highlight sidebar link
    var partner_id = e.layer.feature.properties.slug;
    $partnerList.removeClass('active')
                .filter('#'+partner_id).addClass('active');

});

// Clear the tooltip when map is clicked.
map.on('move', clear_map);
map.on('click', clear_map);


/* Utitilities
-----------------------------------------------------*/

// Remove the 'active' class from all partner markers
function clear_active_markers(){
    partnerLayer.eachLayer(function(layer){
        var base_class_name = 'leaflet-marker-icon';
        var orig_class_name = layer.feature.properties.icon.className;
        layer._icon.className = base_class_name + " " + orig_class_name;
    });
    $partnerList.removeClass('active');
}

// Write the content required to update the tooltip
function build_tooltip(feature){
    var prop = feature.properties;
    var content = '';

    // Add image if exists
    var img = $imageList.find('img#' + feature.properties.slug).attr('src');
    console.log(img);
    if( img != undefined ){
        content += '<div class="partnerInfoImage">';
        content += '<a href="' + prop.url + '"><img src="' + img + '" /></a>';
        content += '</div>';
    }

    // Add title and description
    content += '<div class="partnerInfoText">';
    content += '<h3><a href="' + prop.url + '">' + prop.title + '</a></h3>';
    if( prop.description != "" ){
        content += '<div class="partnerDescription">' + prop.description + '</div>';
    }
    content += '</div>';

    return content;
}

// Update the tooltip content and animate in/out
function toggle_tooltip(content){
    // test that content is HTML string to add to tooltip
    // otherwise, content will be false or map object move event
    if( typeof(content) == 'string' ){
        // Animate in
        var opacity_level = 1;
        $info.html(content).promise().done(function(){
            $info.stop().animate({ opacity: 1}, 200);
        });
    } else {
        // Animate out
        var opacity_level = 0;
        $info.stop().animate({ opacity: 0}, 200, function(){
            $info.html(content);
        });
    }        
}

function clear_map(){
    clear_active_markers();
    toggle_tooltip();
}

/* Disable popups
-----------------------------------------------------*/
partnerLayer.on('click', function(e){
    e.layer.closePopup();
});
