$(document).ready(function () {

   var tabMenuItems = $('.site-select');
   var subscriptionForm = $('.sub-form');
   var categoryDrp = $('#categoryDrp');
   // var sitesDrp = $('#siteDrp');

    var fetchSiteSongs = function (e) {
        e.preventDefault();
        var thisTab = $(this);
        var url = thisTab.attr('data-url');
        var eTarget = $(e.target);
        var siteCard = $('.site-card');
        $.get(url, function (data) {
            console.log('data', data);
            $(".songs-list-table").find('tbody').html(data.songs_html_list);
            tabMenuItems.removeClass('active');
            eTarget.addClass('active');
            siteCard.find('.card-title').html(data.site_info.title);
            siteCard.find('.archive-link').attr('href', data.site_info.a_link);
            if(data.site_info.propp){
                siteCard.find('.card-text').html(data.site_info.propp)
            }
            else{siteCard.find('.card-text').html("No description available")}
        }, 'json')
    };

    var subscribe = function (e) {
        e.preventDefault();
        var thisForm = $(this);
        var url = thisForm.attr('action');
        var data = thisForm.serialize();
        data = data.concat('&action=subscribe');
        console.log('serialized', data);
        $.post(url, data, function (resp) {
            if(resp.OK_message){
                $.toaster(resp.OK_message, 'Success', resp.toast_color);
                thisForm[0].reset();
            }
            else {$.toaster(resp.ERR_message, 'Error', 'danger');}
        }, 'json')
    };

    var fetchSitesByCategory = function (e) {
        var url = e.data.url;
        var drp = e.data.drp;
        PerformAjaxForCategoryDropdown.call(this, url, drp);
    };

    function PerformAjaxForCategoryDropdown(url, drp) {
        var thisDrp = $(this);
        if(thisDrp.val() !== ""){
            $.get(url, {'category': thisDrp.val()}, function (data) {
            drp.html(" ");
            if(data.sites.length > 0 && data.status === 'OK'){
                 $(data.sites).each(function (index, value) {
                $("<option/>", {
                    val: value.slug,
                    text: value.name
                }).appendTo(drp)
            })
            }
            else{drp.append($('<option value="">No sites available</option>'))}
        }, 'json')
        }
        else {console.log('nothing selected')}


    }

    function setLinkState() {

    }

    tabMenuItems.click(fetchSiteSongs);
    subscriptionForm.submit(subscribe);
    // categoryDrp.change({url: '/sites/fetch_sites_by_cat_ajax', drp:sitesDrp}, fetchSitesByCategory);

});