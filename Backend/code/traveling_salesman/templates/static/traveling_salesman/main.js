<script>
function show(){
    var pswrd = document.getElementById('password');
    var icon = document.querySelector('.fas');
    if (pswrd.type === "password") {
        pswrd.type = "text";
        icon.style.color = "#4CAF50";
    }else{
        pswrd.type = "password";
        icon.style.color = "grey";
    }
}
</script>