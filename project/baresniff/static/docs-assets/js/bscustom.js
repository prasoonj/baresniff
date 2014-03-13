$(document).ready(function(){
    //Handles menu drop down
    $('.dropdown-menu').find('form').click(function (e) {
        e.stopPropagation();
    });
});

// app list js from: http://bootsnipp.com/snippets/featured/dropdown-userlist-plus-administration-v23
$(document).ready(function() {
    var panels = $('.user-infos');
    var panelsButton = $('.dropdown-user');
    panels.hide();

    //Click dropdown
    panelsButton.click(function() {
        //get data-for attribute
        var dataFor = $(this).attr('data-for');
        var idFor = $(dataFor);

        //current button
        var currentButton = $(this);
        idFor.slideToggle(400, function() {
            //Completed slidetoggle
            if(idFor.is(':visible'))
            {
                currentButton.html('<span class="glyphicon glyphicon-chevron-up"></span>');
            }
            else
            {
                currentButton.html('<span class="glyphicon glyphicon-chevron-down"></span>');
            }
        })
    });


    $('[data-toggle="tooltip"]').tooltip();

    $('#button-register').click(function(e) {
        e.preventDefault();
        alert("This is a demo.\n :-)");
    });
    
    $('#btn-register-new-app').click(function(e) {
    	e.preventDefault();
    	window.location.href="/app_register?back=" + window.location.href;
    });

//for adding new input fields on app_registration form    
    var next = textNext = dateNext = geoNext = ltextNext = urlNext = emailNext = intNext = 1;
    var listNext = dictNext = fileNext = imageNext = 1;
    $(".add-more").click(function(e){
        e.preventDefault();
        field = e.target.id + "_";
        if (field == 'ShortTextField_'){
        	var addto = "#" + field + textNext;
        	var addRemove = "#" + field + (textNext);
        	textNext += 1;
        	next = textNext;
        }
        if (field == 'CustomDateTimeField_'){
        	var addto = "#" + field + dateNext;
        	var addRemove = "#" + field + (dateNext);
        	dateNext += 1;
        	next = dateNext;
        }
        if (field == 'LongTextField_'){
        	var addto = "#" + field + ltextNext;
        	var addRemove = "#" + field + (ltextNext);
        	ltextNext += 1;
        	next = ltextNext;
        }
        if (field == 'CustomURLField_'){
        	var addto = "#" + field + urlNext;
        	var addRemove = "#" + field + (urlNext);
        	urlNext += 1;
        	next = urlNext;
        }
        if (field == 'CustomEmailField_'){
        	var addto = "#" + field + emailNext;
        	var addRemove = "#" + field + (emailNext);
        	emailNext += 1;
        	next = emailNext;
        }
        if (field == 'CustomIntField_'){
        	var addto = "#" + field + intNext;
        	var addRemove = "#" + field + (intNext);
        	intNext += 1;
        	next = intNext;
        }
        if (field == 'CustomListField_'){
        	var addto = "#" + field + listNext;
        	var addRemove = "#" + field + (listNext);
        	listNext += 1;
        	next = listNext;
        }
        if (field == 'CustomDictField_'){
        	var addto = "#" + field + dictNext;
        	var addRemove = "#" + field + (dictNext);
        	dictNext += 1;
        	next = dictNext;
        }
        if (field == 'CustomFileField_'){
        	var addto = "#" + field + fileNext;
        	var addRemove = "#" + field + (fileNext);
        	fileNext += 1;
        	next = fileNext;
        }
        if (field == 'CustomImageField_'){
        	var addto = "#" + field + imageNext;
        	var addRemove = "#" + field + (imageNext);
        	imageNext += 1;
        	next = imageNext;
        }
        if (field == 'CustomGeoPointField_'){
        	var addto = "#" + field + geoNext;
        	var addRemove = "#" + field + (geoNext);
        	geoNext += 1;
        	next = geoNext;
        }
        var newIn = '<input autocomplete="off" class="input" id="' + field + next + '" name="' + field + next + '" type="text" placeholder="field name">';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove_' + field + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="field">';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(addRemove).after(removeButton);
        // $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#" + field + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);  
        
            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#" + this.id.substring(7);
                $(this).remove();
                $(fieldID).remove();
            });
    });

});

//custom field search
$(document).ready(function() {
    var activeSystemClass = $('.list-group-item.active');

    //something is entered in search form
    $('#system-search').keyup( function() {
       var that = this;
        // affect all table rows on in systems table
        var tableBody = $('.table-list-search tbody');
        var tableRowsClass = $('.table-list-search tbody tr');
        $('.search-sf').remove();
        tableRowsClass.each( function(i, val) {
        
            //Lower text for case insensitive
            var rowText = $(val).text().toLowerCase();
            var inputText = $(that).val().toLowerCase();
            if(inputText != '')
            {
                $('.search-query-sf').remove();
                tableBody.prepend('<tr class="search-query-sf"><td colspan="6"><strong>Searching for: "'
                    + $(that).val()
                    + '"</strong></td></tr>');
            }
            else
            {
                $('.search-query-sf').remove();
            }

            if( rowText.indexOf( inputText ) == -1 )
            {
                //hide rows
                tableRowsClass.eq(i).hide();
                
            }
            else
            {
                $('.search-sf').remove();
                tableRowsClass.eq(i).show();
            }
        });
        //all tr elements are hidden
        if(tableRowsClass.children(':visible').length == 0)
        {
            tableBody.append('<tr class="search-sf"><td class="text-muted" colspan="6">No entries found.</td></tr>');
        }
    });
});

/* base.html image overflow in marketing sections */
$( document ).ready(function() {
    $("[rel='tooltip']").tooltip();    
 
    $('.thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(250); //.fadeIn(250)
        },
        function(){
            $(this).find('.caption').slideUp(250); //.fadeOut(205)
        }
    ); 
});