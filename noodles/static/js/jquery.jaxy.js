(function( $ ){
	var fromBottom = function(pagination){
		
		if (pagination)
			return (parseInt((parseInt($("body").height()) - $(window).height()) - parseInt($(window).scrollTop())) - pagination.offset().top);
		else{
			return 10000000;
		}
		
	}
	
	$.fn.jaxy = function( options ) {  
	
		var settings = {
			"loadImg": "img/loading.gif",
			"fromBottom": 500,
			"paginator": ".jaxy-paginator",
			"paginatorOlder": ".jaxy-older",
			"paginatorNewer": ".jaxy-newer"
		};
	
		return this.each(function() {        
			var ele = $(this);
			if ( options ) { $.extend( settings, options ); }
			
			
			
			$(window).scroll(function(){
				var paginEle = $(settings.paginator);
				if ($(settings.paginator).length < 1){
					paginEle = undefined;
				}
				if (fromBottom(paginEle) < settings.fromBottom){
					var pagination = $(settings.paginator);
					var link = pagination.find(settings.paginatorOlder);
					if (link.length > 0){
						var href = link.attr("href");
						pagination.remove();
						$.ajax({
							url: href,
							success: function(data){
								$(data).appendTo(ele);
								$(settings.paginatorNewer).hide();
							}
						});
						
					}
				}
			});
		});
	
	};
})( jQuery );