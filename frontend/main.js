
// 
const util = {
    getCookie: cname => {
        const name = cname + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ')
                c = c.substring(1);
            if (c.indexOf(name) == 0)
                return c.substring(name.length, c.length);
        }
        return "";
    },

    redirect: url => window.location = url,
    
};

// automatically check authentication, if it's invalid, redirect to login page
(function checkAuth() {
    if (!util.getCookie('authToken'))
        window.location = 'login.html';
})();

