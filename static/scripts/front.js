document.addEventListener('DOMContentLoaded', () => {
	document.querySelector('.msg_send_btn').onclick = () => {
		let template = document.querySelector('#out-msg');
		let msg = template.cloneNode(true);
		msg.content.querySelector('p').innerHTML = document.querySelector('.write_msg').value;
		console.log(msg);
		document.querySelector('.msg_history').append(msg.content);
	}
});