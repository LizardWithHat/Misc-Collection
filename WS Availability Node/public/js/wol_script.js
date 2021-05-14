	var buttons = document.getElementsByClassName('wolbutton');
		for (var i = 0; i < buttons.length; i++) {
			var cur_button = buttons[i]
			if(cur_button.getAttribute('id').slice(4).includes('vap')){
				cur_button.setAttribute("disabled", "true");
			} else {
				cur_button.addEventListener('click', send_wol_package, false)
			}
		}
		function send_wol_package(){
			computername = this.getAttribute('id').slice(4)
			var mac_address;
			
			switch(computername){
				case "computer01":
					mac_address = "FF:FF:FF:FF:FF:FF";
					break;
				case "computer02":
					mac_address = "FF:FF:FF:FF:FF:FF";
					break;
				case "computer03":
					mac_address = "FF:FF:FF:FF:FF:FF";
					break;
				default:
					// Computer not in list, disable WOL button
					this.setAttribute("disabled", "true");
			}
			
			fetch(window.location.origin+"/wake_up_pc?computer_mac="+mac_address).then(response => {
				if(response.status === 200 || response.status === 304){
                    window.alert("Computer is wakign up.")
                } else {
                    window.alert("An error occured while waking up the computer.")
                }                   
                }).catch(function() {
                console.log("error?");
            });
		}