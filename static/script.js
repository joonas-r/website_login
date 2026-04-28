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


async function loadMatches() {
  try {
    const response = await fetch("/api/matches");
    if (!response.ok) {
      throw new Error("Failed to fetch matches");
    }
    const matches = await response.json();
    return matches.json();
  } catch (err) {
    console.error(err);
  }
}


async function getMatchesData() {
        var table = document.getElementById("Matchtable")
        const matchesJSON = loadMatches()
        console.log(matchesJSON)
}