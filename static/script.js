async function userLogin(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    // alert(username);
    
    fetch("/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
        headers: { "Content-Type": "application/json" },
        credentials: "include",  // ← REQUIRED
    });
}