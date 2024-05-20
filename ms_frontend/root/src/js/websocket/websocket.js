websocket_obj = {
  active_game: null,
  other_user_name: null,
  username: null,
  avatar: '../../backend/media/avatars/Abitur_Jaderberg.JPG',
  blocked_by: [],
  blocked_user: [],
  new_private_chat_name: null,
  chat_name: null,
  chat_id: null,
  chat_is_private: null,
  new_chat_name: null,

  onlineStats: [
    {
      user_id: null,
      stat: null,
    }
  ],
  all_user: [
    {
      id: null,
      name: null,
    }
  ],
  chat_data: [
    {
      chat_id: null,
      chat_name: null,
      private_chat_names: [],
      isPrivate: null,
      last_message: null,
      avatar: null,
      is_read: null,
    }
  ],
  messages: [
    {
      id: 0,
      sender_id: null,
      sender: null,
      text: null,
      timestamp: 0,
    }
  ],
  game: [
    {
      game_id: 0,
      invites: 0,
      key_code: 0,
      left_pedal: 0,
      right_pedal: 0,
      is_host: false,
      active_state: false,
      ball_x: 0,
      ball_y: 0,
      host_score: 0,
      guest_score: 0,

      // game_joined: false,
      // hostName: null,
      guestName: null
    }
  ],
  userInCurrentChat: [
    {
      user_name: null,
      user_id: null
    }
  ],

  invited_user_name: null,
  message: null,
  sender: null,
  websocket: null,
  user_id: null,
  game_stats: null,
  history: null,
  tourn_history: null,
  tourns: [],
  chatbot: [
    {
      game_type: null,
      user_one_name: null,
      user_one_id: null,
      user_two_name: null,
      user_two_id: null,
      user_three_name: null,
      user_three_id: null,
      user_four_name: null,
      user_four_id: null,
    }
  ]
}
async function establishWebsocketConnection() {
  websocket_obj.websocket = new WebSocket(`wss://${window.location.hostname}/ws/init/${websocket_obj.user_id}/`);
  websocket_obj.websocket.onopen = function () {
    sendDataToBackend('get_all_user')
    sendDataToBackend('get_avatar')
  };

  websocket_obj.websocket.onmessage = async function (event) {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case 'all_chat_messages':
        if (data.chat_id === websocket_obj.chat_id) {
          await renderProfile()
          websocket_obj.messages = data
          await renderMessages()
        }
        break
      case 'online_stats':
        websocket_obj.onlineStats = data.online_stats
        await renderMessages()
        break
      case 'user_left_chat_info':
        break
      case 'online_stats_on_disconnect':
        websocket_obj.onlineStats = data.online_stats
        await renderMessages()
        break
      case 'user_in_current_chat':
        websocket_obj.userInCurrentChat = data.user_in_chat
        break
      case 'current_users_chats':
        if (data.user_id === websocket_obj.user_id) {
          websocket_obj.chat_data = data.users_chats
          await renderChat()
        }
        break
      case 'created_chat':
        if (data.message === 'ok') {
          websocket_obj.chat_id = data.chat_id
          await sendDataToBackend('get_current_users_chats')
          await setMessageWithTimout('info_create_chat', 'Created chat successfully', 5000)
        } else {
          await setErrorWithTimout('info_create_chat', 'Error: ' + data.message, 5000)
        }
        break
      case 'created_private_chat':
          if (data.message === 'ok') {
            await setMessageWithTimout('info_create_private_chat', 'Created chat successfully', 5000)
          } else {
            await setErrorWithTimout('info_create_private_chat', 'Error: ' + data.message, 5000)
          }
        break
      case 'invited_user_to_chat':
        if (data.message !== 'ok') {
          await setErrorWithTimout('message_with_timeout', data.message, 5000)
        } else {
          await renderChat()
          await setMessageWithTimout('message_with_timeout', 'Invite send successfully', 5000)
        }
        break
      case 'render_left':

        websocket_obj.game.left_pedal = data.new_pedal_pos
        // console.log("new left_pedal: ", websocket_obj.game.left_pedal);
        await update();
        break
      case 'render_right':
        // console.log("RENDER_RIGHT");
        websocket_obj.game.right_pedal = data.new_pedal_pos
        await update();
        break
      case 'init_game':
        console.log(data);
        websocket_obj.game.active_state = true
        joinedGameSuccessfully(websocket_obj.game.game_id)
        initGame(data);
        break
      case 'game_start':
        
        console.log("GAME START");
        document.getElementById("waitingScreen").style.display = "none";
        launchGame();
        sendDataToBackend('request_score')
        // startCountdownAnimation();
        break
      case 'ball_update':
        // console.log("BALL_UPDATE");
        // websocket_obj.game.ball_x = data.ball_x
        const canvas = document.getElementById("pongCanvas");
        websocket_obj.game.ball_x = data.ball_x * canvas.width / 4;
        websocket_obj.game.ball_y = data.ball_y * canvas.height / 2;
        // console.log("ball_y: ", websocket_obj.game.ball_y);
        await update();
        break
      case 'score_update':
        console.log("SCORE_UPDATE");
        websocket_obj.game.host_score = data.host_score
        websocket_obj.game.guest_score = data.guest_score
        // console.log("host_score: ", websocket_obj.game.host_score);
        // console.log("guest_score: ", websocket_obj.game.guest_score);
        await updateScore();
        break
      case 'game_over':
        console.log("GAME OVER");
        gameOver(data);
        break
      case 'reset_stable_id':
        console.log("RESET STABLE ID");
        websocket_obj.game.active_state = false
        sendDataToBackend('reset_stable_id')
        break
      case 'opponent_disconnected':
        console.log("YOUR APPONENT LEFT THE GAME");
        websocket_obj.game.host_score = 0
        websocket_obj.game.guest_score = 0
        websocket_obj.game.game_id = 0
        await updateScore();
        break
      case 'chatbot_trigger':
        websocket_obj.chatbot.user_one_name = data.data[0].user_one_str
        websocket_obj.chatbot.user_one_id = data.data[0].user_one_num
        websocket_obj.chatbot.user_two_name = data.data[0].user_two_str
        websocket_obj.chatbot.user_two_id = data.data[0].user_two_num
        if (data.data.length == 1) {
          websocket_obj.chatbot.game_type = 'final'
        } else if (data.data.length == 2) {
          websocket_obj.chatbot.game_type = 'semi_final'
          websocket_obj.chatbot.user_three_name = data.data[1].user_one_str
          websocket_obj.chatbot.user_three_id = data.data[1].user_one_num
          websocket_obj.chatbot.user_four_name = data.data[1].user_two_str
          websocket_obj.chatbot.user_four_id = data.data[1].user_two_num
        }
        await sendDataToBackend('inform_chatbot_new_game')
        break
      case 'blocked_user_info':
        await sendDataToBackend('get_blocked_by_user')
        await sendDataToBackend('get_blocked_user')
        break
      case 'unblocked_user_info':
        await sendDataToBackend('get_blocked_by_user')
        await sendDataToBackend('get_blocked_user')
        break
      case 'message_save_success':
        await sendDataToBackend('get_current_users_chats')
        break
      case 'message_save_success_bot':
        await sendDataToBackend('get_current_users_chats')
        await sendDataToBackend('get_chat_messages')
        break
      case 'blocked_by_user':
        websocket_obj.blocked_by = data.blocked_by
        break
      case 'blocked_user':
        websocket_obj.blocked_user = data.blocked_user
        break
      case 'all_user':
        websocket_obj.all_user = data.all_user
        break
      case 'get_avatar':
        if (data.avatar) {
          websocket_obj.avatar = data.avatar
        } else { // default avatar
          websocket_obj.avatar = 'https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png'
        }
        break
      case 'recieve_invites':
      // websocket_obj.game.invites = data.matches
        websocket_obj.game.invites = JSON.parse(data.matches);
  
        console.log('DATA: ', websocket_obj.game.invites)
        console.log('joined value: ', data.joined_game);
        if (data.joined_game)
          console.log('already in a game+#++##+##+#+#+#++#+#');
        else
          renderInvites();
        break
      case 'recieve_tourns':
        console.log('recieve_tourns');
        websocket_obj.game.invites = JSON.parse(data.matches)
        console.log('DATA: ', websocket_obj.game.invites)
        if (userState.currPage !== 'tournPage')
          renderTourns();
        else
          joinTourn(userState.tournId, websocket_obj.game.invites);
        // console.log('DATA: ', websocket_obj.game.invites[1][1])
        break
      case 'recieve_tourn_history':
        websocket_obj.tourn_history = JSON.parse(data.matches)
        console.log('DATA: ', websocket_obj.game.invites)
        displayTournHistory();
        // if (userState.currPage !== 'tournPage')
        //   renderTourns();
        // else
        //   joinTourn(userState.tournId, websocket_obj.game.invites);
        // console.log('DATA: ', websocket_obj.game.invites[1][1])
        break
      case 'recieve_stats':
        console.log('recieve_stats')
        console.log(data)
        websocket_obj.game_stats = data.stats;
        displayStats();
        // getUserStats(data.stats);
        break
      case 'recieve_history':
        console.log('recieve_history')
        websocket_obj.history = data.history;
        displayHistory();
        break
      case 'set_message_stat':
        break
      case 'inform_chatbot':
        if (websocket_obj.user_id === data.user_id) {
          // console.log("I ["+websocket_obj.username+"] got INFORM_CHATBOT through ws")
          websocket_obj.other_user_name = data.other_user_name
          await sendDataToBackend('save_chatbot_message')
        }
        break
      case 'already_in_game':
        console.log('already_in_game')
        requestInvites()
        break
      case 'inform_chatbot_new_game':
        if (await user_got_invited(data.data)) {
          websocket_obj.chatbot = data.data
          await sendDataToBackend('send_chatbot_message_new_game')
        }
        break
      default:
        console.log('SOMETHING ELSE [something wrong in onmessage type]')
        console.log('DATA: ', data)
    }
  };

  websocket_obj.websocket.onerror = function (error) {
    console.error("WebSocket error:", error);
    logoutUser()
  };

  websocket_obj.websocket.onclose = function (event) {
    console.log("WebSocket closed:", event);
    logoutUser()
  };
}

const sendError = async (error) => {
  console.error('Error: Failed to receive ws data: ', error)
}

async function sendDataToBackend(request_type) {
  return new Promise((resolve, reject) => {
    if (websocket_obj.websocket.readyState === WebSocket.OPEN) {
      let type = 'none'
      let data = 'none'
      let logicType = 'none'

      switch (request_type) {
        case 'send_chat_message':
          type = 'save_message_in_db',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'sender': websocket_obj.sender,
            'message': websocket_obj.message,
          }
          break
        case 'get_chat_messages':
          type = 'send_chat_messages',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_online_stats':
          type = 'send_online_stats',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_user_in_current_chat':
          type = 'send_user_in_current_chat',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_current_users_chats':
          type = 'send_current_users_chats',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'set_user_left_chat':
          type = 'send_user_left_chat',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'set_new_chat':
          type = 'send_created_new_chat',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'chat_name': document.getElementById('new_chat_name').value,
            'isPrivate': false,
          }
          break
        case 'set_new_private_chat':
          type = 'send_created_new_private_chat',
          logicType = 'chat'
            data = {
              'user_id': websocket_obj.user_id,
              'chat_id': websocket_obj.chat_id,
              'chat_name': websocket_obj.new_private_chat_name
            }
          break
        case 'set_invited_user_to_chat':
          type = 'set_invited_user_to_chat',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'invited_user_name': websocket_obj.invited_user_name
          }
          break
        case 'game_new_move':
          // const canvas = document.getElementById("pongCanvas");
          console.log("in game_new_move");
          console.log(websocket_obj.game.is_host);
          // prev_pos =  websocket_obj.game.left_pedal;
          if (websocket_obj.game.is_host === true)
            pedal_pos = websocket_obj.game.left_pedal
          else
            pedal_pos = websocket_obj.game.right_pedal
          // console.log(prev_pos);

          // pedal_pos = pedal_pos * 2 / canvas.height;
          // console.log("pedal_pos: ", pedal_pos);
          type = 'send_game_scene'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            // 'chat_id': websocket_obj.chat_id,
            'game_id': websocket_obj.game.game_id,
            'key_code': websocket_obj.game.key_code,
            'prev_pos': pedal_pos,
            // 'is_host': websocket_obj.game.is_host,
          }
          break
        case 'init_game':
          console.log("in init_game");
          type = 'send_init_game',
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            // 'chat_id': websocket_obj.chat_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        case 'send_ball_update':
          type = 'send_ball_update',
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            // 'chat_id': websocket_obj.chat_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        case 'block_user':
          type = 'block_user',
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'user_to_block': websocket_obj.chat_name
          }
          break
        case 'unblock_user':
          type = 'unblock_user'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'user_to_unblock': websocket_obj.chat_name
          }
          break
        case 'get_blocked_by_user':
          type = 'get_blocked_by_user'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_blocked_user':
          type = 'get_blocked_user'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_all_user':
          type = 'get_all_user'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_avatar':
          type = 'get_avatar'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'request_invites':
          console.log('request_invites')
          type = 'send_request_invites'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,

          }
          break
        case 'join_tournament':
          console.log('join_tournamentttttttt')
          console.log(websocket_obj.user_id)
          type = 'send_join_tournament'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'invited_id': websocket_obj.invited_id,
            'game_id': 0,
          }
          break
        case 'request_tourns':
          console.log('request_tournssss')
          console.log(websocket_obj.user_id)
          type = 'send_request_tourns'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'request_tourn_history':
          console.log('request_tourn_his')
          console.log(websocket_obj.user_id)
          type = 'request_tourn_his'
          logicType = 'game'
          data = {
              'user_id': websocket_obj.user_id,
              'game_id': 0,
          }
          break
        // case 'new_profile_picture':
        //   type = 'new_profile_picture',
        //   data = {
        //     'profile_picture': websocket_obj.profile_picture,
        //     'file_data': websocket_obj.file_data,
        //   }
        //   break
        case 'request_stats':
          type = 'send_stats'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'request_history':
          type = 'send_history'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'messages_in_chat_read':
          type = 'messages_in_chat_read'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'messages_in_chat_unread':
          type = 'messages_in_chat_unread'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'inform_chatbot':
          type = 'new_tournament_chatbot'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'invited_user_name': websocket_obj.invited_id,
            'current_user_name': websocket_obj.username
          }
          break
        case 'save_chatbot_message':
          type = 'save_chatbot_message'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'other_user_name': websocket_obj.other_user_name,
            'current_user_name': websocket_obj.username,
          }
          break
        case 'user_left_game':
          type = 'user_left_game',
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': websocket_obj.game.game_id,
          }
          websocket_obj.game.active_state = false

          websocket_obj.game.host_score = 0
          websocket_obj.game.guest_score = 0
          websocket_obj.game.game_id = 0
          break
        case 'request_score':
          type = 'request_score'
          logicType = 'game'
          console.log('request_score')
          console.log(websocket_obj.game.active_state)
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        case 'reset_stable_id':
          type = 'reset_stable_id'
          logicType = 'game'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'inform_chatbot_new_game':
          type = 'inform_chatbot_new_game'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'game_type': websocket_obj.chatbot.game_type,
            'user_one_name': websocket_obj.chatbot.user_one_name,
            'user_one_id': websocket_obj.chatbot.user_one_id,
            'user_two_name': websocket_obj.chatbot.user_two_name,
            'user_two_id': websocket_obj.chatbot.user_two_id,
            'user_three_name': websocket_obj.chatbot.user_three_name,
            'user_three_id': websocket_obj.chatbot.user_three_id,
            'user_four_name': websocket_obj.chatbot.user_four_name,
            'user_four_id': websocket_obj.chatbot.user_four_id,          }
          break
        case 'send_chatbot_message_new_game':
          type = 'send_chatbot_message_new_game'
          logicType = 'chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'game_type': websocket_obj.chatbot.game_type,
            'user_one_name': websocket_obj.chatbot.user_one_name,
            'user_one_id': websocket_obj.chatbot.user_one_id,
            'user_two_name': websocket_obj.chatbot.user_two_name,
            'user_two_id': websocket_obj.chatbot.user_two_id,
            'user_three_name': websocket_obj.chatbot.user_three_name,
            'user_three_id': websocket_obj.chatbot.user_three_id,
            'user_four_name': websocket_obj.chatbot.user_four_name,
            'user_four_id': websocket_obj.chatbot.user_four_id,
          }
          break
        default:
          console.log('SOMETHING ELSE [something wrong in onmessage type]')
      }

      websocket_obj.websocket.send(JSON.stringify({
        'status': 'ok',
        'type': type,
        'logicType': logicType,
        'data': data
      }));
      websocket_obj.websocket.addEventListener('error', sendError);
      resolve() // WITHOUT this we don't return to prev functions!!
    }
    else {
      console.error("WebSocket connection is not open.");
      reject(new Error("WebSocket connection is not open."));
    }
  });
}


async function user_got_invited(data) {
  if (websocket_obj.user_id == data.user_one_id || websocket_obj.user_id == data.user_two_id) {
    return true
  }
  if (data.game_type == 'semi_final') {
    if (websocket_obj.user_id == data.user_three_id || websocket_obj.user_id == data.user_four_id) {
      return true
    }
  }
  return false
}