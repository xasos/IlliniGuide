$(function() {
    $(".autocomplete1").autocomplete({
        source: function(request, response) {
            $.getJSON("/autocomplete", {
                q: request.term
            }, function(data) {
                response(data.matching_results);
            });
        },
        minLength: 2,
        select: function(event, ui) {
            window.location.href = "/search/" + ui.item.value;
        }
    });
});
$(function() {
    $(".autocomplete2").autocomplete({
        search: function(event, ui) {
            $('.quicksearch').empty();
        },
        source: function(request, response) {
            $.getJSON("/autocomplete", {
                q: request.term,
                d: function() {
                        var url = window.location.pathname.split('/');
                        if (url.length > 2 && url[1] == "dept") {
                            return url[2].toUpperCase();
                        } else {
                            return null;
                        }
                    },
                r: function() {
                        if ($('.autocomplete2').attr('id') == "profqs" || $('.autocomplete2').attr('id') == "allprofqs") {
                            return 'professor';
                        } else if ($('.autocomplete2').attr('id') == "classqs" || $('.autocomplete2').attr('id') == "allclassqs") {
                            return 'class';
                        } else if ($('.autocomplete2').attr('id') == "alldeptqs") {
                            return "department"
                        } else {
                            return null;
                        }
                    }
            }, function(data) {
                response(data.matching_results);
            });
        },
        minLength: 2
    }).data('ui-autocomplete')._renderItem = function(ul, item) {
        if ($('.autocomplete2').attr('id') == "profqs" || $('.autocomplete2').attr('id') == "allprofqs") {
            return $('<li/>')
                .data('item.autocomplete', item)
                .append("<a href=\'/professor/" + item.value.replace(/\s+/g, '') + "\'>" + item.value + "</a>")
                .appendTo($('.quicksearch'));
        } else if ($('.autocomplete2').attr('id') == "classqs" || $('.autocomplete2').attr('id') == "allclassqs") {
            return $('<li/>')
                .data('item.autocomplete', item)
                .append("<a href=\'/dept/" + item.value.split()[0] + "/class/" + item.value.split()[1]+ "\'>" + item.value + "</a>")
                .appendTo($('.quicksearch'));
        } else if ($('.autocomplete2').attr('id') == "alldeptqs") {
            return $('<li/>')
                .data('item.autocomplete', item)
                .append("<a href=\'/dept/" + item.value.split()[0] + "\'>" + item.value + "</a>")
                .appendTo($('.quicksearch'));
        } else {
            return $('<li/>')
                .data('item.autocomplete', item)
                .append(item.value)
                .appendTo($('.quicksearch'));
        }
    };
});


$(document).ready(function() {
    $(".autocomplete2").focus(function() {
        $(".alllist").hide(0);
    });
});

$(document).ready(function() {
    $(".autocomplete2").focusout(function() {
        if (!$(this).val()) {
            $('.quicksearch').empty();
            $(".alllist").show(0);
        }
    });
});

$(function() {
    $( ".tabs" ).tabs();
});

$(function() {
    $("#navbarsearch").click(function() {
        $( "#searchtoggle" ).toggle( "slide" );
    });
});
