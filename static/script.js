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


function makeTableMatches(matches) {
	var table = document.getElementById("Matchtable");

	matches.forEach(match => {
		console.log(match)
	})
		 
}

function loadMatches() {
	
	fetch("/api/matches", {
	  method: "GET",
	})
	  .then(response => {
	    if (!response.ok) {
	      throw new Error("Failed to fetch matches");
	    }
	    return response.json();
	  })
	  .then(matches => {
	    makeTableMatches(matches);   
	  })
	  .catch(error => {
	    console.error(error);
	  });
}


function getMatchesData() {
  
        loadMatches();
		
}
