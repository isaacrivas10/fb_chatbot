function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    expires= d.setTime(d.getTime() + (exdays*24*60*60*1000));
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function checkCookie(cookieName) {
    var cookie = getCookie(cookieName);
    if (cookie != "") {
        return true;
    } else {
        return false;
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function deleteCookie(cookieName){
  document.cookie = cookieName+"=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}