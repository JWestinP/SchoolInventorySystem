function show_hide_pop_up(){
    var popup_form = document.getElementById("popup_form");

    if (popup_form.style.display == "none"){
        popup_form.style.display = "block";
    }
    else {
        popup_form.style.display = "none";
    }
}