	var buttons = document.getElementsByClassName('rdpbutton');
		for (var i = 0; i < buttons.length; i++) {
			var cur_button = buttons[i]
			cur_button.addEventListener('click', generate_rdp_file, false)
		}
		function generate_rdp_file(){
			var element = document.createElement('a');
			computername = this.getAttribute('id').slice(4)
			if(!computername.includes("vap")){
				window.alert("Please keep the amount of loggind in users below 3!")
				}
			var connectionname;
			
			switch(computername){
				case "computer01":
					connectionname = "192.168.0.101"
					break;
				case "computer02":
					connectionname = "192.168.0.102"
					break;
				case "computer03":
					connectionname = "192.168.0.103"
					break;
				default:
					connectionname = computername + ".local";
			}
			
			element.setAttribute('href', 'data:application/x-rdp;charset=utf-8,' + encodeURIComponent("full address:s:"+connectionname+"\ngatewaycredentialssource:i:0"));
			element.setAttribute('download', "connection.rdp");
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
		}