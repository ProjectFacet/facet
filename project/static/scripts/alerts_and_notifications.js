// /**
//  * @author Batch Themes Ltd.
//  */
// (function() {
//     'use strict';
//     $(function() {
//         var config = $.localStorage.get('config');
//         $('body').attr('data-layout', config.layout);
//         $('body').attr('data-palette', config.theme);
//         $('body').attr('data-direction', config.direction);
//
//         $('.btn-notify').on('click', function() {
//             var action = $(this).data('action');
//             if (action === 'success') {
//                 $.notify("Access granted", {
//                     className: 'success',
//                     globalPosition: 'top right',
//                     autoHideDelay: 10000,
//                 });
//             } else if (action === 'info') {
//                 $.notify("Do not press this button", {
//                     className: 'info',
//                     globalPosition: 'top left',
//                     autoHideDelay: 10000,
//                 });
//             } else if (action === 'warn') {
//                 $.notify("Warning: Self-destruct in 3.. 2..", {
//                     className: 'warn',
//                     globalPosition: 'bottom left',
//                     autoHideDelay: 10000,
//                 });
//             } else if (action === 'error') {
//                 $.notify("BOOM!", {
//                     className: 'error',
//                     globalPosition: 'bottom right',
//                     autoHideDelay: 10000,
//                 });
//             }
//         });
//
//         $('.btn-swal').on('click', function() {
//             var action = $(this).data('action');
//             if (action === 'basic') {
//                 swal('The Internet?', 'That thing is still around?');
//             }
//             if (action === 'auto-close') {
//                 swal({
//                     title: 'Auto close alert!',
//                     text: 'I will close in 2 seconds.',
//                     timer: 2000
//                 });
//             }
//             if (action === 'html') {
//                 swal({
//                     title: 'HTML example',
//                     html: 'You can use <b>bold text</b>, ' + '<a href="//github.com">links</a> ' + 'and other HTML tags'
//                 });
//             }
//             if (action === 'confirm') {
//                 swal({
//                     title: 'Are you sure?',
//                     text: 'You will not be able to recover this imaginary file!',
//                     type: 'warning',
//                     showCancelButton: true,
//                     confirmButtonColor: '#3085d6',
//                     cancelButtonColor: '#d33',
//                     confirmButtonText: 'Yes, delete it!',
//                     closeOnConfirm: false
//                 }, function() {
//                     swal('Deleted!', 'Your file has been deleted.', 'success');
//                 });
//             }
//             if (action === 'cancel') {
//                 swal({
//                     title: 'Are you sure?',
//                     text: 'You will not be able to recover this imaginary file!',
//                     type: 'warning',
//                     showCancelButton: true,
//                     confirmButtonColor: '#3085d6',
//                     cancelButtonColor: '#d33',
//                     confirmButtonText: 'Yes, delete it!',
//                     cancelButtonText: 'No, cancel plx!',
//                     confirmButtonClass: 'confirm-class',
//                     cancelButtonClass: 'cancel-class',
//                     closeOnConfirm: false,
//                     closeOnCancel: false
//                 }, function(isConfirm) {
//                     if (isConfirm) {
//                         swal('Deleted!', 'Your file has been deleted.', 'success');
//                     } else {
//                         swal('Cancelled', 'Your imaginary file is safe :)', 'error');
//                     }
//                 });
//             }
//         });
//         $('.btn-toast').on('click', function() {
//             var type = $(this).data('type')
//             if (type === 'success') {
//                 toastr.options = {
//                     positionClass: 'toast-top-right'
//                 };
//                 toastr.success('Great idea!');
//             }
//             if (type === 'warning') {
//                 toastr.options = {
//                     positionClass: 'toast-bottom-right'
//                 };
//                 toastr.warning('Warning!');
//             }
//             if (type === 'danger') {
//                 toastr.options = {
//                     positionClass: 'toast-bottom-left'
//                 };
//                 toastr.error('Danger!');
//             }
//             if (type === 'info') {
//                 toastr.options = {
//                     positionClass: 'toast-top-left'
//                 };
//                 toastr.info('Excellent!');
//             }
//         });
//     });
// })();
