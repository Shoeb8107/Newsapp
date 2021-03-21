$(function () {

  var loadComm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-comment").modal("show");
      },
      success: function (data) {
        $("#modal-book").modal("hide");
        $("#modal-comment .modal-content").html(data.html_form);
      }
    });
  };



 
  var loadForm = function () {
    console.log("create new comment")
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book").modal("hide");
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };




  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var deleteForm = function () {
    
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function(data){
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);


      }}
      
    });
    return false;
  };

 


  /* Binding */

  // Create book

  $(".js-comment").click(loadComm);

  
  //$(".js-create-book").click(loadForm);
  $(document).on('click', '.js-create-book', function (e) {
    console.log("create new comment")
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book").modal("hide");
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  

  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", deleteForm);


  });

