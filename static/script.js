async function userLogin(){
    var user = document.getElementById("username").value;
    var pass = document.getElementById("password").value;
    
    // alert(username);
    
    fetch("/api/login", {
        method: "POST",
        body: JSON.stringify({
        	username: user, 
        	password: pass }),
        headers: { "Content-Type": "application/json" },
        credentials: "include"
    });
}
