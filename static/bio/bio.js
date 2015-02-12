$(document).ready(function(){

var $body = $("body");

/*listens for ajax calls to implement loading wheel
http://stackoverflow.com/questions/1964839/jquery-please-wait-loading-animation
*/
$(document).on({
  ajaxStart: function(){
$body.addClass("loading"); },
  ajaxStop: function(){
$body.removeClass("loading");}
});

  //handlebars.js
  var source = $("#bio-template").html();
  var template = Handlebars.compile(source);
  var html = template();
  $("#handlebars_container").html(html);

  // max avatar image upload 2.5 MB
  var avatar = document.getElementById("id_image");
  var gallery = document.getElementById("id_gallery");

  //event listener for avatar and gallery image forms 
  avatar.addEventListener("change", function(){
   upload_handler(avatar);
  }, false); 

  gallery.addEventListener("change", function(){
    upload_handler(gallery);
  }, false);

  //gallery.onchange = upload_handler(gallery);
  function upload_handler(calling_elem) {
    var file = calling_elem.files[0];
    var $limit = '';

    if (calling_elem == document.getElementById("id_image")) {
      $limit = document.getElementById("file_size_msg_box1");
    } else {
      $limit = document.getElementById("file_size_msg_box2");
    };

    // upload if < 2.5MB
    if (file.size < 2500001) {
      // no limit warning msg
      $($limit).css('visibility','hidden');
      var name = file.name;
      
      /***
       create thumbnail preview 
       ***/
      var img = document.createElement("img");     
      var reader = new FileReader();
      reader.onload = function(e) {
        img.src = e.target.result;
      }
      reader.readAsDataURL(file);

      var canvas = document.createElement("canvas");
      var ctx = canvas.getContext("2d");

      var dataurl = '';
      // 'virtual' thumbnail image sizing and drawn on 
      //canvas (document.createElement)
      //img.onload to force image draw on canvas
      img.onload = function(){
        ctx.drawImage(img, 0, 0);
      
        var MAX_WIDTH = 180;
        var MAX_HEIGHT = 250;
        var width = img.width;
        var height = img.height;
  
        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          };
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          };
        };
        canvas.width = width;
        canvas.height = height;
      
        ctx.drawImage(img, 0, 0, width, height); 
        // dataurl = base64 encoded thumbnail
        dataurl = canvas.toDataURL();
      
      //determine which div to show image preview
      var div_preview =''; 
      if (calling_elem == document.getElementById("id_image")) {
        div_preview = "image_preview";
      } else {
        div_preview = "gallery_preview";
      };
      // append actual image to appropriate preview div
      $("#" + div_preview).append($("<img>", {
        src : dataurl,
        id: name,
        style: 'display:inline-block;position:absolute;margin:auto;top:0;left:0;bottom:0;right:0;'
      }));
  
        //end img.onload
        };
      if (calling_elem == document.getElementById("id_image")) {
        document.getElementById("image_form").submit();
      } else {
        document.getElementById("gallery_form").submit();
        get_gallery();
      }
      $("#"+name).hide();
    // filesize > 2.5 MB warning messages
    } else {
      $($limit).css('visibility','visible'); 
    }
  // end upload_handler()
  };


/* getJSON calls below */

function save(form, focusedElement){
 /**
  * .blur() event handler for input fields on form that sends form to server
  * @param form
  * @return JSON
  */

  var data={};
  for (var i=0; i < form[0].elements.length; i++) {      
    var name = form[0].elements[i].name;
    var value = form[0].elements[i].value;    
    data[name]=value;
  }

  var url = "/my_account/save/";

  $.getJSON(url ,data, function(response) { 
    var source = $("#bio-template").html();
    var template = Handlebars.compile(source);
    var html = template(response);
    $("#handlebars_container").html(html);
  });
  // 1000 ms wait before focus on input box
  setTimeout(function() {
    $("#" + focusedElement).focus();
  }, 1000);
}

function remove(element) {
 /**
  * sends request to server to 
  * delete data in database
  * @param the element that was clicked in the DOM
        which coorelates to an input field
  * @return JSON updated dictionary of filled fields 
  */

  var url = "/my_account/delete/";
  $.getJSON(url, {"element":element}, function(response) {
    var source = $("#bio-template").html();
    var template = Handlebars.compile(source);
    var html = template(response);
    $("#handlebars_container").html(html);
  });
}

/* .blur() + .click() event listener for field add and delete
   setTimeout enforced to workaround Handlebars.js template rendering
*/
var $form = $("#form");
$("#ancestor").on("blur", ".blur", function(){

  var focusedElement = document.activeElement;

  setTimeout(function(){
  focusedElement = document.activeElement.name;
  }, 1);

  setTimeout(function(){
  save( $form, focusedElement );
  }, 1);
});

$("#ancestor").on("click", ".delete", function() {
  var $element = $(this).attr("name");
  remove($element);
});

function get_gallery() {
/**
  request to server to update thumbnails in gallery
  @params
    none
  @returns
    a list of serving urls for each gallery photo 
  */

  var url = "/my_account/thumbnail/";
  $.getJSON(url, function(response) {
    var source = $("#gallery-template").html();
    var template = Handlebars.compile(source);
    var html = template(response);
    $("#handlebars_gallery_container").html(html);
  });

}

// get the initial state of the users answers stored in db onpageload
save($form);
get_gallery();
//end jQuery
});
