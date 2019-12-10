$(function(){
	$('.button_drawer').click(function(){
		$('.content').fadeToggle(300, function(){
			$('.mobile_navigation').toggle("slide",{direction: 'left'},0);
		});	
	});
	console.log('%c Greetings from the developer! ', 'font-size: 20px;');
	console.log('%c Created by- Kishor Malakar (https://fb.com/kishor.malakar) ', 'font-size: 15px;');
	console.log('%c All rights reserved ', 'font-size: 15px;');
});