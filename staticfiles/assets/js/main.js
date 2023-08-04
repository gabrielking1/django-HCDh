;(function($){
    "use strict";

    $(document).ready(function(){

        /*------------------------------------
            Product Details Slider
        ------------------------------------*/
        var productDetailSlider = $('.single-thumbnail-slider');
        var pThumbanilSlider = $('.product-thumbnail-carousel');

        if (productDetailSlider.length) {
            productDetailSlider.slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: true,
                asNavFor: '.product-thumbnail-carousel'
            });
        }
        if (pThumbanilSlider.length) {
            pThumbanilSlider.slick({
                slidesToShow: 3,
                slidesToScroll: 1,
                asNavFor: '.single-thumbnail-slider',
                dots: false,
                centerMode: false,
                focusOnSelect: true,
                vertical: true,
                arrows:false,
                prevArrow: '<div class="slick-prev"><i class="fa fa-angle-double-up"></i></div>',
                nextArrow: '<div class="slick-next"><i class="fa fa-angle-double-down"></i></div>',
                responsive: [
                    {
                      breakpoint: 1024,
                      settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: true,
                        dots: false
                      }
                    },
                    {
                      breakpoint: 600,
                      settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2
                      }
                    },
                    {
                      breakpoint: 480,
                      settings: {
                        slidesToShow: 3,
                        slidesToScroll: 1,
                        centerMode: true,
                        vertical:false
                      }
                    },
                    {
                      breakpoint: 300,
                      settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1,
                        centerMode: false,
                        vertical:false
                      }
                    }
                    // You can unslick at a given breakpoint now by adding:
                    // settings: "unslick"
                    // instead of a settings object
                  ]
              });
        }
        


         /*--------------------
            wow js init
        ---------------------*/
        
        if( $( window.width ) > 768 ) {
            new WOW().init();
        }

        /*-------------------------
            magnific popup activation
        -------------------------*/
        $('.video-play-btn,.video-popup,.small-vide-play-btn').magnificPopup({
            type: 'video'
        });

        /*------------------
            back to top
        ------------------*/
        $(document).on('click', '.back-to-top', function () {
            $("html,body").animate({
                scrollTop: 0
            }, 2000);
        });

        /*------------------------------
            counter section activation
        -------------------------------*/
        var counternumber = $('.count-num');
        counternumber.counterUp({
            delay: 20,
            time: 3000
        });

        /*-------------------------------
            Portfolio filter 
        ---------------------------------*/
        var $Container = $('.portfolio-masonry');
        if ($Container.length > 0) {
            $('.portfolio-masonry').imagesLoaded(function () {
                var festivarMasonry = $Container.isotope({
                    itemSelector: '.masonry-item', // use a separate class for itemSelector, other than .col-
                    masonry: {
                        gutter: 0
                      }
                });
                $(document).on('click', '.portfolio-menu li', function () {
                    var filterValue = $(this).attr('data-filter');
                    festivarMasonry.isotope({
                        filter: filterValue
                    });
                });
            });
            $(document).on('click','.portfolio-menu li' , function () {
                $(this).siblings().removeClass('active');
                $(this).addClass('active');
            });
        }
        
        /*---------------------------
            Testimonial carousel
        ---------------------------*/
        var $testimonialCarousel = $('.testimonial-carousel');
        if ($testimonialCarousel.length > 0) {
            $testimonialCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: false,
                nav: false,
                animateOut: 'fadeOut',
                animateIn: 'fadeIn',
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 1
                    },
                    960: {
                        items: 1
                    },
                    1200: {
                        items: 1
                    },
                    1920: {
                        items: 1
                    }
                }
            });
        }
        

        var $sliderBg = $('.bg-image-slider-init');
        if ($sliderBg.length > 0) {
            $sliderBg.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: false,
                nav: true,
                navText: ['<span class="fas fa-chevron-left fa-2x"></span>','<span class="fas fa-chevron-right fa-2x"></span>'],
            
                animateOut: 'fadeOut',
                animateIn: 'fadeIn',
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 1
                    },
                    960: {
                        items: 1
                    },
                    1200: {
                        items: 1
                    },
                    1920: {
                        items: 1
                    }
                }
            });
        }

        /*---------------------------
            Our Work carousel
        ---------------------------*/
        var $OurWorkCarousel = $('.our-work-carousel');
        if ($OurWorkCarousel.length > 0) {
            $OurWorkCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: true,
                nav: true,
                navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
                smartSpeed: 2000,
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 2
                    },
                    960: {
                        items: 2
                    },
                    1200: {
                        items: 3
                    },
                    1920: {
                        items: 3
                    }
                }
            });
        }

        /*---------------------------
            Our Work carousel
        ---------------------------*/
        var $OurWorkCarousel = $('.our-work-carousel');
        if ($OurWorkCarousel.length > 0) {
            $OurWorkCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: true,
                nav: true,
                navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
                smartSpeed: 2000,
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 2
                    },
                    960: {
                        items: 2
                    },
                    1200: {
                        items: 3
                    },
                    1920: {
                        items: 3
                    }
                }
            });
        }

        /*---------------------------
            Brand carousel
        ---------------------------*/
        var $BrandCarousel = $('.brand-carousel');
        if ($BrandCarousel.length > 0) {
            $BrandCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: false,
                nav: false,
                smartSpeed: 2000,
                responsive: {
                    0: {
                        items: 1
                    },
                    360: {
                        items: 1
                    },
                    460: {
                        items: 2
                    },
                    599: {
                        items: 2
                    },
                    768: {
                        items: 3
                    },
                    960: {
                        items: 4
                    },
                    1200: {
                        items: 5
                    },
                    1920: {
                        items: 5
                    }
                }
            });
        }

        /*---------------------------
           Team carousel
        ---------------------------*/
        var $teamCarousel = $('.team-carousel');
        if ($teamCarousel.length > 0) {
            $teamCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: false,
                nav: false,
                smartSpeed: 2000,
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 2
                    },
                    960: {
                        items: 2
                    },
                    1200: {
                        items: 4
                    },
                    1920: {
                        items: 4
                    }
                }
            });
        }

        /*---------------------------
           Testimonial Two carousel
        ---------------------------*/
        var $testimonialTwoCarousel = $('.testimonial-carousel-two');
        if ($testimonialTwoCarousel.length > 0) {
            $testimonialTwoCarousel.owlCarousel({
                loop: true,
                autoplay: true, //true if you want enable autoplay
                autoPlayTimeout: 1000,
                margin: 30,
                dots: false,
                nav: false,
                smartSpeed: 2000,
                responsive: {
                    0: {
                        items: 1
                    },
                    460: {
                        items: 1
                    },
                    599: {
                        items: 1
                    },
                    768: {
                        items: 2
                    },
                    960: {
                        items: 2
                    },
                    1200: {
                        items: 2
                    },
                    1920: {
                        items: 3
                    }
                }
            });
        }
        
        /*----------------------
            Search Popup
        -----------------------*/
        var bodyOvrelay =  $('#body-overlay');
        var searchPopup = $('#search-popup');

        $(document).on('click','#body-overlay',function(e){
            e.preventDefault();
        bodyOvrelay.removeClass('active');
            searchPopup.removeClass('active');
        });
        $(document).on('click','#search',function(e){
            e.preventDefault();
            searchPopup.addClass('active');
        bodyOvrelay.addClass('active');
        });
    

    });


    //define variable for store last scrolltop
    var lastScrollTop = '';

    $(window).on('scroll', function () {
        
        //back to top show/hide
       var ScrollTop = $('.back-to-top');
       if ($(window).scrollTop() > 500) {
           ScrollTop.fadeIn(500);
       } else {
           ScrollTop.fadeOut(500);
       }

       /*--------------------------
        sticky menu activation
       -------------------------*/
        var st = $(this).scrollTop();
        var mainMenuTop = $('.navbar-area');
        if ($(window).scrollTop() > 500) {
            if (st > lastScrollTop) {
                // hide sticky menu on scrolldown 
                mainMenuTop.removeClass('nav-fixed');
                
            } else {
                // active sticky menu on scrollup 
                mainMenuTop.addClass('nav-fixed');
            }

        } else {
            mainMenuTop.removeClass('nav-fixed ');
        }

        lastScrollTop = st;
       
    });
           

    $(window).on('load',function(){

        /*-----------------
            preloader
        ------------------*/
        var preLoder = $("#preloader");
        preLoder.fadeOut(1000);

        /*-----------------
            back to top
        ------------------*/
        var backtoTop = $('.back-to-top')
        backtoTop.fadeOut();

        /*---------------------
            Cancel Preloader
        ----------------------*/
        $(document).on('click','.cancel-preloader a',function(e){
            e.preventDefault();
            $("#preloader").fadeOut(2000);
        });

    });

    /*--------------------------------------
        Quality Card
    ---------------------------------------*/
    $(document).on('mouseover','.quality-card-wrapper',function() {
        $(this).addClass('quality-card-active');
        $('.quality-card-wrapper').removeClass('quality-card-active');
        $(this).addClass('quality-card-active');
    });

    /*===================================
     Popup
    =====================================*/
    $('.test-popup-link').magnificPopup({
        type:'video',
    });
    /*===================================
     Slider
    =====================================*/
    
    $('.slider').slick({
        infinite: true,
        autoplay:false,
        autoplaySpeed:4000,
        slidesToShow: 1,
        slidesToScroll: 1,
        dots: true,
        arrows: true,
        appendArrows: $('.header-slider-controller'),
        prevArrow: '<div class="header-prev-arrow"><i class="fas fa-chevron-left"></i></div>',
        nextArrow: '<div class="header-next-arrow"><i class="fas fa-chevron-right"></i></div>',
        responsive: {
            0: {
                items: 1,
                dots: true,
                arrows: false
            },
            460: {
                items: 1,
                dots: true,
                arrows: false
            },
            599: {
                items: 1,
                dots: true,
                arrows: false
            },
            768: {
                items: 1,
                dots: true,
                arrows: false
            },
            800: {
                items: 1,
                dots: true,
                arrows: false
            },
            1200: {
                items: 1,
                dots: true,
                arrows: false
            },
            1920: {
                items: 1
            }
        }

    });
    $('.slider2').slick({
        autoplay:false,
        autoplaySpeed:1500,
        asNavFor: '.slider3',
        arrows: false,
        dots:true
    });
    $('.slider3').slick({
        autoplay:false,
        autoplaySpeed:1500,
        asNavFor: '.slider2',
        arrows: false,
    });
    $('.blog-slider').slick({
        infinite: true,
        autoplay:true,
        autoplaySpeed:4000,
        slidesToShow: 1,
        slidesToScroll: 1,
        dots: false,
        arrows: true,
        appendArrows: $('.blog-slider-controller'),
        prevArrow: '<div class="blog-prev-arrow"><i class="fas fa-chevron-left"></i></div>',
        nextArrow: '<div class="blog-next-arrow"><i class="fas fa-chevron-right"></i></div>'
    });
 
    $('.multiple-items').slick({
        autoplay:true,
        autoplaySpeed:1500,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1
       
      });

      $('#multiple-card').slick({
        autoplay:true,
        autoplaySpeed:1500,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 991,
                settings: {
                  slidesToShow: 2,
                  slidesToScroll: 1
                }
            },
            {
              breakpoint: 599,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1
              }
            }
            // You can unslick at a given breakpoint now by adding:
            // settings: "unslick"
            // instead of a settings object
          ]
      });

       $('.image-popup').magnificPopup({
        type:'image'
    });

    if($("#mycountdown").length > 0){
        $("#mycountdown").countdown("2019/10/20", function(event) {
            $('.days').text(
                event.strftime('%D')
            );
            $('.hours').text(
                event.strftime('%H')
            );
            $('.mins').text(
                event.strftime('%M')
            );
            $('.secs').text(
                event.strftime('%S')
            );
     });
    }

    
    $('.children').on("click",function(){
        $(this).find(".dropdown").toggle();
    });

    
    var $nicePageScrl = $('#pagescroll');
    if($nicePageScrl.length > 0){
        $("#pagescroll").niceScroll({cursorborder:"",cursorcolor:"var( --main-color-one)", cursorwidth:"5px",}); 
    }

    $(".current-year").text((new Date).getFullYear());

    /*===================================
     Slider
    =====================================*/
    setInterval(() => {
        var currentIndex = $('div.active').index() + 1;
        $('.current').html(currentIndex);
    }, 1);

    // from right to left
    var $popupOffCan = $('#popup-menu');
    if ($popupOffCan.length > 0) {
        $('#popup-menu').PopupLayer({ 
            to: 'left',
            blur: true,
            content: $(".slide-sidebar-area").css("display", "block"),
            backgroundColor: "#F9C935", 
            closeBtn: $(".close")
        });
    }

})(jQuery);
