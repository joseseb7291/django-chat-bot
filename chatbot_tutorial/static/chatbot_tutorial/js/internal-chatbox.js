// Function to simply format the text in the right way. May end up being more complicated when you have MCQs, etc.
function generate_formatted_chat_message(data) {
  if (data.type == "text") {
    message_text = '<span class="message-text">' + data.text + "</span>";
    return message_text;
  }
  return "";
}

// Function that adds a message to the chat window
function add_message_to_chat(data, formatted_div) {
  var chat = $("#messages-container");
  chat.append(
    '<div class="msg-row"><div class="col-xs-11 col-sm-11 col-md-11 col-lg-11 no-sides-padding msg-animate"><div class="bot-icon-div">Bot:</div><div class="panel message-panel bot-msg "><div class="panel-body bot-msg-body"><div><div class="message-text">' +
      formatted_div +
      "</div></div></div></div></div></div>"
  );
  $("#body-container").scrollTop($("#body-container")[0].scrollHeight);
}

// Function taht is called when the server sends a message via websockets to my front end.
function processAndDisplayChatMessage(message) {
  var content_data = JSON.parse(message.data);
  var formatted_div = generate_formatted_chat_message(content_data.message);
  if (formatted_div.length > 0) {
    add_message_to_chat(content_data.message, formatted_div);
  }
}

function requestJoke(type) {
  if (!$("#userName").val()) {
    alert("Select User");
    return;
  }
  message = {};
  message.type = type;
  message.user = $("#userName").val();
  message.timestamp = new Date();

  chatsock.send(JSON.stringify(message));
  $("#message").val("").focus();
  return false;
}
