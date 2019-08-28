document.addEventListener('DOMContentLoaded', () => {
	// Make 'enter' key submit message
	let msg = document.querySelector('.write_msg');
	msg.addEventListener('keyup', event => {
		event.preventDefault();
		if (event.keyCode == 13) {
			document.querySelector('.msg_send_btn').click();
		}
	});

});