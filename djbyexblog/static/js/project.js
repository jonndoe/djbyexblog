/* Project specific Javascript goes here. */



// Toggle between hiding and showing post replies/comments by style:block or none
//document.getElementById("myBtn").click();
function hideBlogCommentsFunctionByStyle(id) {
    var x = document.getElementById(id);
    if (x.style.display == "none") {
        x.style.display = "block";
    } else {
        x.style.display = 'none';
    }
}
