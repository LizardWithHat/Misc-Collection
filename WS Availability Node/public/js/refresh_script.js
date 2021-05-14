	async function refresh_pc_status(){
			var computername = this.getAttribute('id').slice(8)
			var buttonContainer = this.parentElement.parentElement;
			buttonContainer.setAttribute("class", "container alert alert-info");
			fetch(window.location.origin+"/query_pc?computer="+computername).then(response => {
					if(!response.ok){
						console.log("Es ist ein allgemeiner Fehler aufgetreten");
					}
					return response.json();
			}).then(response => {
					var message = response.message;
					var table = document.getElementById("users_"+computername);
					var usernode = document.createElement("pre");
					var usertext = document.createTextNode(message);
					table.innerHTML = "";
					//Richtige Hintergrundfarbe setzen
					if(message.includes("Kein Benutzer")){
						buttonContainer.setAttribute("class", "container alert alert-success");
						usertext = document.createTextNode("Kein Benutzer angemeldet");
					} else if(message.includes("Fehler")){
						buttonContainer.setAttribute("class", "container alert alert-danger");
						usertext = document.createTextNode("Computer nicht erreichbar. Eventuell ist er ausgeschaltet.");
					} else {
						buttonContainer.setAttribute("class", "container alert alert-warning");
					}
					usernode.appendChild(usertext);
					table.appendChild(usernode);
                }).catch(function() {
					console.log("Es ist ein Fehler aufgetreten.");
				});
			return "Done";
		}
	async function initialize_refresh_buttons(){
		var buttons = document.getElementsByClassName('refreshbutton');
		for (var i = 0; i < buttons.length; i++) {
			var cur_button = buttons[i]
			cur_button.addEventListener('click', refresh_pc_status, false);
			// Ein mal zu Anfang ausführen
			cur_button.click();
		}
	}		
	
	initialize_refresh_buttons();