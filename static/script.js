var request = new XMLHttpRequest();
request.open("POST", "/listmessages");
request.onload = () => {
    var data = JSON.parse(request.responseText);
    localStorage.setItem("room_id", data["room_id"]);
    for(var i=0; i<data["message"].length; i++){
        if(data["room_id"]==data["message"][i]["room_id_n"]){
        const li = document.createElement('li');
        const response = data["message"][i];
        li.innerHTML = `<div>USERNAME: ${response["username"]}</div> <div class="msg-data">${response["selection"]}</div> <div class="sm">${response["time"]}</div>`;
        document.getElementById("message_dict").append(li);
        socket.removeAllListeners();
    };}
};
request.send();
var socket =io.connect(location.protocol+'//'+document.domain+':'+location.port);
socket.on('connect',()=>{
    document.querySelector("#send").onclick=()=>{
        const selection = document.querySelector('#messages').value;
        socket.emit('send message', {'selection': selection});
        socket.removeAllListeners();
    };
});
socket.on('sent messages', data=>{
    if (data["room_id"] === localStorage.room_id){
        const li = document.createElement('li');
        li.innerHTML = `<div>USERNAME: ${data["username"]}</div><div class="msg-data">${data["selection"]}</div><div>${data["time"]}</div>`;
        document.querySelector('#message_dict').append(li);
        socket.removeAllListeners();
    };
});