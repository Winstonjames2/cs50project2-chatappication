from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app=Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
socketio=SocketIO(app)

chatrooms=[]
usernames=[]
message_dict={}
message_list=[]

@app.route("/")
def index():
    if session.get("message_f"):
        return render_template("index.html",message_f=session["message_f"])
    return render_template("index.html")

@app.route("/join",methods=["POST"])
def join():
    session["message_f"]=""
    room_id=request.form.get("room_id")
    username=request.form.get("username")
    print(type(room_id),type(username))
    if request.method=="POST":
        try:
            int(room_id)
            if username!="" and room_id!="":
                if username in usernames and room_id in chatrooms:
                    session["message_f"]="ERROR, USERNAME Already USED {}".format(room_id)
                    return redirect("/")
                elif room_id in chatrooms:
                    usernames.append(username)
                    session["room_id"]=room_id
                    session["username"]=username
                else:
                    usernames.append(username)
                    chatrooms.append(room_id)
                    session["room_id"]=room_id
                    session["username"]=username
                return redirect("room/{}/{}".format(2589,room_id))
            else:
                session["message_f"]="ERROR!, CREDENTIALS INVALID"
        except:
            session["message_f"]="ERROR!, CREDENTIALS INVALID"
    return redirect("/")

@app.route("/logout")
def logout():
    session["username"]=None
    session["room_id"]=None
    return redirect("/")

@app.route("/room/{}/<int:room_id>".format(2589))
def room(room_id):
    return render_template("message.html")

@socketio.on("send message")
def send(data):
    selection=data["selection"]
    time=datetime.now().strftime("%Y-%m-%d %H:%M")
    response_dict = {"selection": selection, "time": time, "username": session["username"]}
    res=response_dict
    res["room_id_n"]=session["room_id"]
    message_list.append(res)
    emit("sent messages",{**response_dict,**{"room_id":session["room_id"]}},broadcast=True)

# @app.route("/private")
# def index2():
#     return render_template("secret.html")

# @app.route("/private/4481/<int:p_room_id>")
# def private(p_room_id):
#     return render_template("message.html")

# @app.route("/c_j",methods=["POST"])
# def p_join():
#     if request.method=="POST":
#         p_room_id=request.form.get("p_room_id")
#         username=request.form.get("username")
#         p_s_code=request.form.get("p_s_code")

#         c_p_room_id=request.form.get("c_p_room_id")
#         c_username=request.form.get("c_username")
#         c_p_s_code=request.form.get("c_p_s_code")
#         if p_room_id !="" and username!="" and p_s_code!="":
#             session["p_room_id"]=p_room_id
#             session["username"]=username
#             session["p_s_code"]=p_s_code
#             return redirect("/private/4481/{}".format(p_room_id))
#         elif c_p_room_id!="" and c_username!="" and c_p_s_code!="":
#             session["c_p_room_id"]=c_p_room_id
#             session["c_username"]=c_username
#             session["c_p_s_code"]=c_p_s_code
#             return redirect("/private/4481/{}".format(p_room_id))
#         else:
#             return redirect("/private")

@app.route("/listmessages",methods=["POST","GET"])
def listmessages():
    return jsonify({**{"message":message_list},**{"room_id":session["room_id"]}})