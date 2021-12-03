function create_navbar_item (link, icon, text){
    /*the wrapping li*/
    let nav_item = document.createElement("li");
    nav_item.setAttribute("class", "nav-item d-flex active");
    /*the a (inside li)*/
    let nav_link = document.createElement("a");
    nav_link.setAttribute("href", link);
    nav_link.setAttribute("class", "nav-link");
    /*the icon and span (inside a)*/
    let nav_icon = document.createElement("i");
    nav_icon.setAttribute("class", icon);
    let nav_span = document.createElement("span"); 
    nav_span.setAttribute("class", "clearfix d-none d-sm-inline-block")
    let nav_word = document.createTextNode(text);
    /*connect them*/
    nav_span.appendChild(nav_word);
    nav_link.appendChild(nav_icon);
    nav_link.appendChild(nav_span);
    nav_item.appendChild(nav_link);
    /*attach it*/
    element=document.getElementsByClassName("navbar-nav ms-auto").item(0);
    element.appendChild(nav_item);
};

