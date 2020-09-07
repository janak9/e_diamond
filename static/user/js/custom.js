(function($) {
    "use strict";
	
	/* ..............................................
	   Loader 
	   ................................................. */
	$(window).on('load', function() {
		$('.preloader').fadeOut();
		$('#preloader').delay(550).fadeOut('slow');
		$('body').delay(450).css({
			'overflow': 'visible'
		});
	});

	/* ..............................................
	   Fixed Menu
	   ................................................. */

	$(window).on('scroll', function() {
		if ($(window).scrollTop() > 50) {
			$('.main-header').addClass('fixed-menu');
		} else {
			$('.main-header').removeClass('fixed-menu');
		}
	});

	/* ..............................................
	   Gallery
	   ................................................. */

	$('#slides-shop').superslides({
		inherit_width_from: '.cover-slides',
		inherit_height_from: '.cover-slides',
		play: 5000,
		animation: 'fade',
	});

	$(".cover-slides ul li").append("<div class='overlay-background'></div>");

	/* ..............................................
	   Map Full
	   ................................................. */

	$(document).ready(function() {
		$(window).on('scroll', function() {
			if ($(this).scrollTop() > 100) {
				$('#back-to-top').fadeIn();
			} else {
				$('#back-to-top').fadeOut();
			}
		});
		$('#back-to-top').click(function() {
			$("html, body").animate({
				scrollTop: 0
			}, 600);
			return false;
		});
	});

	/* ..............................................
	   Special Menu
	   ................................................. */

	var Container = $('.container');
	Container.imagesLoaded(function() {
		var portfolio = $('.special-menu');
		portfolio.on('click', 'button', function() {
			$(this).addClass('active').siblings().removeClass('active');
			var filterValue = $(this).attr('data-filter');
			$grid.isotope({
				filter: filterValue
			});
		});
		var $grid = $('.special-list').isotope({
			itemSelector: '.special-grid'
		});
	});

	/* ..............................................
	   BaguetteBox
	   ................................................. */

	baguetteBox.run('.tz-gallery', {
		animation: 'fadeIn',
		noScrollbars: true
	});

	/* ..............................................
	   Offer Box
	   ................................................. */

	$('.offer-box').inewsticker({
		speed: 3000,
		effect: 'fade',
		dir: 'ltr',
		font_size: 13,
		color: '#ffffff',
		font_family: 'Montserrat, sans-serif',
		delay_after: 1000
	});

	/* ..............................................
	   Tooltip
	   ................................................. */

	$(document).ready(function() {
		$('[data-toggle="tooltip"]').tooltip();
	});

	/* ..............................................
	   Owl Carousel Instagram Feed
	   ................................................. */

	$('.main-instagram').owlCarousel({
		loop: true,
		margin: 0,
		dots: false,
		autoplay: true,
		autoplayTimeout: 3000,
		autoplayHoverPause: true,
		navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
		responsive: {
			0: {
				items: 2,
				nav: true
			},
			600: {
				items: 4,
				nav: true
			},
			1000: {
				items: 8,
				nav: true,
				loop: true
			}
		}
	});

	/* ..............................................
	   Featured Products
	   ................................................. */

	$('.featured-products-box').owlCarousel({
		loop: true,
		rewind: true,
		margin: 0,
		dots: false,
		autoplay: true,
		autoplayTimeout: 3000,
		autoplayHoverPause: true,
		navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
		responsive: {
			0: {
				items: 1,
				nav: true
			},
			600: {
				items: 3,
				nav: true
			},
			1000: {
				items: 4,
				nav: true,
				loop: false
			}
		}
	});

	/* ..............................................
	   Scroll
	   ................................................. */

	$(document).ready(function() {
		$(window).on('scroll', function() {
			if ($(this).scrollTop() > 100) {
				$('#back-to-top').fadeIn();
			} else {
				$('#back-to-top').fadeOut();
			}
		});
		$('#back-to-top').click(function() {
			$("html, body").animate({
				scrollTop: 0
			}, 600);
			return false;
		});
	});


	/* ..............................................
	   Slider Range
	   ................................................. */

	$(function() {
		const min_amount = $("#min_amount").val();
		const max_amount = $("#max_amount").val();
		$("#slider-price").slider({
			range: true,
			min: 0,
			max: 100000,
			values: [min_amount, max_amount],
			slide: function(event, ui) {
				$("#min_amount").val(ui.values[0]);
				$("#max_amount").val(ui.values[1]);
				$("#amount").val("Rs. " + ui.values[0] + " - Rs. " + ui.values[1]);
			}
		});
		$("#min_amount").val(min_amount);
		$("#max_amount").val(max_amount);
		$("#amount").val("Rs. " + min_amount + " - Rs. " + max_amount);
	});

	$(function() {
		const min_size = $("#min_size").val();
		const max_size = $("#max_size").val();
		$("#slider-size").slider({
			range: true,
			min: 0.01,
			max: 10.00,
			step: 0.01,
			values: [min_size, max_size],
			slide: function(event, ui) {
				$("#min_size").val(ui.values[0]);
				$("#max_size").val(ui.values[1]);
				$("#size").val(ui.values[0] + " - " + ui.values[1]);
			}
		});
		$("#min_size").val(min_size);
		$("#max_size").val(max_size);
		$("#size").val(min_size + " - " + max_size);
	});

	$(function() {
		const min_diameter = $("#min_diameter").val();
		const max_diameter = $("#max_diameter").val();
		$("#slider-diameter").slider({
			range: true,
			min: 0.01,
			max: 12.00,
			step: 0.01,
			values: [min_diameter, max_diameter],
			slide: function(event, ui) {
				$("#min_diameter").val(ui.values[0]);
				$("#max_diameter").val(ui.values[1]);
				$("#diameter").val(ui.values[0] + " - " + ui.values[1]);
			}
		});
		$("#min_diameter").val(min_diameter);
		$("#max_diameter").val(max_diameter);
		$("#diameter").val(min_diameter + " - " + max_diameter);
	});

	/* ..............................................
	   NiceScroll
	   ................................................. */

	$(".brand-box").niceScroll({
		cursorcolor: "#9b9b9c",
	});
	
	
}(jQuery));