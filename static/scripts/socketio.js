document.addEventListener('DOMContentLoaded', () => {
	var socket = io.connect('http://' + document.domain + ':' + location.port);

	let room = 'lounge';
	joinRoom(room);

	// Display incoming messages
	socket.on('message', data => {

		// Managing system messages and ordinary msgs
		if (data.username) {
			
			// How msg should look (in or our)
			if (current_user_username == data.username) {
				var template = document.querySelector('#out-msg');
			} else {
				var template = document.querySelector('#in-msg');
			}

			// Creating clone from template
			let msg = template.cloneNode(true);
			msg.content.querySelector('.username').innerHTML = data.username;
			msg.content.querySelector('p').innerHTML = data.msg;
			msg.content.querySelector('.time_date').innerHTML = data.time_stamp;
			document.querySelector('.msg_history').append(msg.content);
			// span_username.innerHTML = data.username;
		} else {
			printSysMsg(data.msg);
		}

	});

	// Send message
	document.querySelector('.msg_send_btn').onclick = () => {
		socket.send({'msg': escapeHtml(document.querySelector('.write_msg').value),
					 'username': username,
					 'room': room});
		// Clear input area
		document.querySelector('.write_msg').value = '';
	}

	// Room selection
	document.querySelectorAll('.chat_list').forEach(div => {
		div.onclick = () => {

			// Handling "active room" class
			// Removing active_chat class from all rooms
			Array.from(document.querySelectorAll('.chat_list')).map(item => {item.classList.remove('active_chat')})
			// Adding active_chat class to the selected room
			div.classList.add('active_chat');

			// Switching room
			let newRoom = div.getElementsByTagName('h5')[0].innerHTML;
			if (newRoom == room) {
				msg = `You are already in ${room} room.`
				printSysMsg(msg);

			} else {
				leaveRoom(room);
				joinRoom(newRoom);
				room = newRoom;
			}
		}
	});

	// Leave room
	function leaveRoom(room) {
		socket.emit('leave', {'username': username, 'room': room});
	}

	// Join room
	function joinRoom(room) {
		socket.emit('join', {'username': username, 'room': room});
		// Clear message area
		document.querySelector('.msg_history').innerHTML = '';
		// Autofocus on text box
		document.querySelector('.write_msg').focus();
	}


	// Reloading chat
	socket.on('chatReload', function() {
		location.reload()
	});

	// Print system message
	function printSysMsg(msg) {
		const p = document.createElement('p');
		p.innerHTML = msg;
		document.querySelector('.msg_history').append(p);
	}

	// Escaping html
	var entityMap = {
	  '&': '&amp;',
	  '<': '&lt;',
	  '>': '&gt;',
	  '"': '&quot;',
	  "'": '&#39;',
	  '/': '&#x2F;',
	  '`': '&#x60;',
	  '=': '&#x3D;'
	};

	function escapeHtml (string) {
	  return String(string).replace(/[&<>"'`=\/]/g, function (s) {
	    return entityMap[s];
	  });
	}


	// // Display USERS dict - for dev purposes only
	// setInterval(getRooms, 1000);

	// function getRooms() {
	// 	var xhttp = new XMLHttpRequest();
 //  		xhttp.onreadystatechange = function() {
 //    	  if (this.readyState == 4 && this.status == 200) {
 //      		document.getElementById("rooms_info").innerHTML =
 //      		this.responseText;
 //    	  }
 //  		};
 //    	xhttp.open("GET", "/rooms_info", true);
 //    	xhttp.send();
	// }

	// Display count of users in rooms
	setInterval(updateUsers, 1000);

	function updateUsers() {
		var xhttp = new XMLHttpRequest();
  		xhttp.onreadystatechange = function() {
    	  if (this.readyState == 4 && this.status == 200) {
    	  	let response = JSON.parse(this.responseText);
    	  	document.querySelectorAll('.chat_list').forEach(div => {
				div.querySelector('.chat_date').innerHTML = Object.keys(response[div.getElementsByTagName('h5')[0].innerHTML.toLowerCase()]).length;
    	    });
  		  };
  		};
    	xhttp.open("GET", "/room_users", true);
    	xhttp.send();
	}

});