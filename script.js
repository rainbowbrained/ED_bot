// Wait for the document to load before running the script 
(function ($) {
  
  // We use some Javascript and the URL #fragment to hide/show different parts of the page
  // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#Linking_to_an_element_on_the_same_page
  $(window).on('load hashchange', function(){
    
    // First hide all content regions, then show the content-region specified in the URL hash 
    // (or if no hash URL is found, default to first menu item)
    $('.content-region').hide();
    
    // Remove any active classes on the main-menu
    $('.main-menu a').removeClass('active');
    var region = location.hash.toString() || $('.main-menu a:first').attr('href');
    
    // Now show the region specified in the URL hash
    $(region).show();
    
    // Highlight the menu link associated with this region by adding the .active CSS class
    $('.main-menu a[href="'+ region +'"]').addClass('active'); 

    // Alternate method: Use AJAX to load the contents of an external file into a div based on URL fragment
    // This will extract the region name from URL hash, and then load [region].html into the main #content div
    // var region = location.hash.toString() || '#first';
    // $('#content').load(region.slice(1) + '.html')
    
  });
  
})(jQuery);

Telegram.WebApp.ready();

var initData = Telegram.WebApp.initData || '';
var initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};
Telegram.WebApp.expand();
window.alert(initData);
window.alert(initDataUnsafe);

function SubmitFood(event) {
  event.preventDefault();
  var time_food = document.getElementById( "input_time_food" ).value ;
  var place_food = document.getElementById( "input_place_food" ).value ;

  var protein = document.getElementById( "input_protein" ).value ;
  var fats = document.getElementById( "input_fats" ).value ;
  var carbs = document.getElementById( "input_carbs" ).value ;
  var fiber = document.getElementById( "input_fiber" ).value ;
  var calcium = document.getElementById( "input_calcium" ).value ;
  var happy_food = document.getElementById( "input_happy_food" ).value ;
  var hunger = document.getElementById( "rangeList_hunger" ).value ;
  var satiety = document.getElementById( "rangeList_satiety" ).value ;
  var comment = document.getElementById( "personal_comment" ).value ;

  var reason = ''
  var emotions = ''
  var compensate = ''
  var check = document.getElementById( "hunger_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "people_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "boredom_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "schedule_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "habit_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "food_near_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "emotion_food_reason" ) ;
  check.checked ? reason += '1' : reason += '0' ;
  check = document.getElementById( "other_food_reason" ) ;
  check.checked ? reason += document.getElementById( "other_food_reason_text" ).value : reason += '0' ;

  check = document.getElementById( "happiness" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "anger" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "anxiety" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "disgust" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "shame" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "surprise" ) ;
  check.checked ? emotions += '1' : emotions += '0' ;
  check = document.getElementById( "other" ) ;
  check.checked ? emotions += document.getElementById( "other_emotions" ).value : emotions += '0' ;


  check = document.getElementById( "no_compensate" ) ;
  check.checked ? compensate += '1' : compensate += '0' ;
  check = document.getElementById( "vomit" ) ;
  check.checked ? compensate += '1' : compensate += '0' ;
  check = document.getElementById( "diuretic" ) ;
  check.checked ? compensate += '1' : compensate += '0' ;
  check = document.getElementById( "laxative" ) ;
  check.checked ? compensate += '1' : compensate += '0' ;
  check = document.getElementById( "sport" ) ;
  check.checked ? compensate += '1' : compensate += '0' ;
  check = document.getElementById( "other_compensate" ) ;
  check.checked ? compensate += document.getElementById( "other_compensate_text" ).value : compensate += '0' ;
  
  var text = JSON.stringify({ compensate: compensate, emotions: emotions,  reason: reason,
    comment: comment, satiety: satiety, hunger:hunger, happy_food:happy_food,
    calcium:calcium, fiber:fiber, carbs:carbs, fats:fats, protein:protein,
    place_food:place_food, time_food:time_food});
  Telegram.WebApp.ready();
  console.log(text);
  window.alert(text);
  var user_id = Telegram.WebApp.initDataUnsafe.user.id 
  window.alert(text);
  window.alert(user_id);
  Telegram.WebApp.sendData(text);
  Telegram.WebApp.close();
}

