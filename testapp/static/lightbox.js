
	$(document).ready(function() {
			$(".lightbox").fancybox({
				wrapCSS    : 'fancybox-custom',
				closeClick : true,

				openEffect : 'elastic',
				closeEffect: 'elastic',

				helpers : {
					title : {
						type : 'inside'
					},
					overlay : {
						css : {
							'background' : 'rgba(238,238,238,0.85)'
						}
					}
				}
			});
		}