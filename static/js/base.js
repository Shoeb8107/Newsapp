
 		function valthisform(){
            var checkedSource = true;

            var categoryTech = document.getElementById("categoryTech").checked;
            var categoryPolitics = document.getElementById("categoryPolitics").checked;
           var categorySport = document.getElementById("categorySport").checked;
           var checkedCategory = false;



           if(categoryTech===true || categoryPolitics===true || categorySport===true){
               checkedCategory = true;
           }

           if(checkedSource ===false && checkedCategory===false){
               document.getElementById('error_message').innerHTML = '<div class="alert alert-danger card-header text-center flashit"><strong>Warning!</strong> No source and category selected!</div>';
               event.preventDefault();
           }
           else if(checkedSource ===false ){
               document.getElementById('error_message').innerHTML = '<div class="alert alert-danger card-header text-center flashit"><strong>Warning!</strong> No source selected!</div>';
               event.preventDefault();
           }
           else if( checkedCategory===false){
               document.getElementById('error_message').innerHTML = '<div class="alert alert-danger card-header text-center flashit"><strong>Warning!</strong> No  category selected!</div>';
               event.preventDefault();
           }

   }


   
		$(document).ready(function() {
			setTimeout(function(){
				$('body').addClass('loaded');
				$('h1').css('color', '#22222')
				}, 3000);

        });
        
