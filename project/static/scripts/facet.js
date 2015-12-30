// Comment Forms
// 
// $('#wf-comment').on('submit'), function(evt){
//   event.preventDefault();
//   console.log("form submitted");
//   create_comment();
// }),
//
// function create_comment() {
//   console.log("create comment is working")
//   $.ajax({
//     url : "comment/new",
//     type : "POST",
//     data: { wf-comment : $('#wf-comment').val() },
//
//     success : function(json) {
//       $('#wf-comment').val('');
//       console.log(json);
//       console.log("success");
//     },
//
//     error: function(xhr, errmsg, err) {
//       $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//           " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//     }
//   });
//   console.log($('#wf-comment').val())
// };
