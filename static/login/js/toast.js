// Paths to your SVG files
const successIconPath = '/images/correct.svg';
const errorIconPath = '/images/errore.svg';

// Function to show toast
function showToast(message, type) {
    var toast = $("#toast");
    var toastIcon = $("#toast-icon");
    var toastMessage = $("#toast-message");

    toastMessage.text(message);
    toast.removeClass("success error"); // Remove any previous types

    if (type === "success") {
        toast.addClass("success");
        toastIcon.attr("src", successIconPath);
    } else if (type === "error") {
        toast.addClass("error");
        toastIcon.attr("src", errorIconPath);
    }

    toast.addClass("show");

    // Remove toast on click
    toast.off('click').on('click', function () {
        toast.removeClass("show");
    });

    // Automatically hide the toast after 3 seconds
    setTimeout(function () {
        toast.removeClass("show");
    }, 5000);
}