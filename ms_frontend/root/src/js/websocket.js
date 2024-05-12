websocket_obj = {
  // profile_picture: null,
  // file_data: null,

  active_game: null,

  username: null,
  password: null,
  avatar: '../../backend/media/avatars/Abitur_Jaderberg.JPG',
  // avatar: null,
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

  user_id: -1
  // game_alias: 
  // mail
}

async function establishWebsocketConnection() {
  websocket_obj.websocket = new WebSocket(`wss://${window.location.hostname}/ws/init/${websocket_obj.user_id}/`);
  console.log('what is in web: ', websocket_obj.websocket);
  websocket_obj.websocket.onopen = function () {
    // renderProfile()
    sendDataToBackend('get_all_user') // NEW since 03.02 | this should also happen on refresh!
    sendDataToBackend('get_avatar')// NEW since 07.02
  };

  websocket_obj.websocket.onmessage = async function (event) {
    const data = JSON.parse(event.data);
    // console.log('ONMESSAGE DATA: ', data)
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
        // var canvas = document.getElementById("pongCanvas");
        // websocket_obj.game.left_pedal = canvas.height * data.new_pedal_pos / 2
        websocket_obj.game.left_pedal = data.new_pedal_pos
        console.log("new left_pedal: ", websocket_obj.game.left_pedal);
        await update();
        // await renderGame()
        break
      case 'render_right':
        console.log("RENDER_RIGHT");
        // var canvas = document.getElementById("pongCanvas");
        websocket_obj.game.right_pedal = data.new_pedal_pos
        // websocket_obj.game.right_pedal = data.new_pedal_pos
        console.log("new right_pedal: ", websocket_obj.game.right_pedal);
        await update();
        // await renderGame()
        break
      case 'init_game':
        console.log(data);
        websocket_obj.game.active_state = true
        joinedGameSuccessfully(websocket_obj.game.game_id)
        document.getElementById("waitingScreen").style.display = "block";
        if (data.is_host === 'True')
        {
          document.getElementById('playerOne').textContent = websocket_obj.username;
          document.getElementById('playerTwo').textContent = data.guest_id;
          websocket_obj.game.is_host = true
          console.log("game.is_host = true");
          console.log(websocket_obj.game.is_host);
        }
        else  {
          document.getElementById('playerOne').textContent = data.host_id;
          document.getElementById('playerTwo').textContent = websocket_obj.username;
          websocket_obj.game.is_host = false
        }
        // websocket_obj.game.game_joined = true;
        break
      case 'game_start':
        
        console.log("GAME START");
        document.getElementById("waitingScreen").style.display = "none";
        launchGame();
        sendDataToBackend('request_score')
        startCountdownAnimation();
        break
      case 'ball_update':
        // console.log("BALL_UPDATE");
        // websocket_obj.game.ball_x = data.ball_x
        const canvas = document.getElementById("pongCanvas");
        websocket_obj.game.ball_x = data.ball_x * canvas.width / 4;
        // console.log("ball_x: ", websocket_obj.game.ball_x)
        // console.log("data.ball_x: ", data.ball_x)
        // console.log("data.ball_y: ", data.ball_y)
        // // websocket_obj.game.ball_y = data.ball_y
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
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('pongCanvas').classList.add('hidden');
        document.getElementById('winningScreen').classList.remove('hidden');
        
        console.log("before fireworks")
        console.log(websocket_obj.game.game_id)
        console.log(data.game_id)
        document.getElementById('fireworkCanvas').style.zIndex = 1;
        if (websocket_obj.game.game_id === data.game_id)
            activateFireworks();
        
        console.log("GAME_OVER");
        // document.getElementById("waitingScreen").style.display = "block";

        websocket_obj.game.hostname
        websocket_obj.game.active_state = false

        websocket_obj.game.host_score = 0
        websocket_obj.game.guest_score = 0
        websocket_obj.game.game_id = 0
        await updateScore();
        break
      case 'opponent_disconnected':
        console.log("YOUR APPONENT LEFT THE GAME");
        websocket_obj.game.host_score = 0
        websocket_obj.game.guest_score = 0
        websocket_obj.game.game_id = 0
        await updateScore();
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
        } else {
          // default avatar
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
        // websocket_obj.game.invites = data.matches
        console.log('DATA: ', websocket_obj.game.invites)
        // console.log('DATA: ', websocket_obj.game.invites[0])
        // console.log('DATA: ', websocket_obj.game.invites[0][1])
        // console.log('DATA: ', websocket_obj.game.invites[0][0])
        generateFrontendRepresentation(websocket_obj.game.invites)
        // console.log('DATA: ', websocket_obj.game.invites[1][1])
        break
      case 'recieve_stats':
        console.log('recieve_stats')
        console.log(data)
        break
      case 'recieve_history':
        console.log('recieve_history')
        console.log(data)
        break
      case 'already_in_game':
        console.log('already_in_game')
        requestInvites()
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

      switch (request_type) {
        case 'send_chat_message':
          type = 'save_message_in_db'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'sender': websocket_obj.sender,
            'message': websocket_obj.message,
          }
          break
        case 'get_chat_messages':
          type = 'send_chat_messages'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_online_stats':
          type = 'send_online_stats'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_user_in_current_chat':
          type = 'send_user_in_current_chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_current_users_chats':
          console.log('HERE: ', websocket_obj.user_id)
          type = 'send_current_users_chats'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'set_user_left_chat':
          type = 'send_user_left_chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'set_new_chat':
          type = 'send_created_new_chat'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'chat_name': document.getElementById('new_chat_name').value,
            'isPrivate': false,
          }
          break
        case 'set_new_private_chat':
          type = 'send_created_new_private_chat'
            data = {
              'user_id': websocket_obj.user_id,
              'chat_id': websocket_obj.chat_id,
              'chat_name': websocket_obj.new_private_chat_name
            }
          break
        case 'set_invited_user_to_chat':
          type = 'set_invited_user_to_chat'
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
          console.log("pedal_pos: ", pedal_pos);
          type = 'send_game_scene'
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
          type = 'send_init_game'
          data = {
            'user_id': websocket_obj.user_id,
            // 'chat_id': websocket_obj.chat_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        case 'send_ball_update':
          type = 'send_ball_update'
          data = {
            'user_id': websocket_obj.user_id,
            // 'chat_id': websocket_obj.chat_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        case 'block_user':
          type = 'block_user'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'user_to_block': websocket_obj.chat_name
          }
          break
        case 'unblock_user':
          type = 'unblock_user'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
            'user_to_unblock': websocket_obj.chat_name
          }
          break
        case 'get_blocked_by_user':
          type = 'get_blocked_by_user'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_blocked_user':
          type = 'get_blocked_user'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_all_user':
          type = 'get_all_user'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'get_avatar':
          type = 'get_avatar'
          data = {
            'user_id': websocket_obj.user_id,
            'chat_id': websocket_obj.chat_id,
          }
          break
        case 'request_invites':
          console.log('request_invites')
          type = 'send_request_invites'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,

          }
          break
        case 'join_tournament':
          console.log('join_tournamentttttttt')
          console.log(websocket_obj.user_id)
          type = 'send_join_tournament'
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
          data = {
            'user_id': websocket_obj.user_id,
          //   'invited_id': websocket_obj.invited_id,
            'game_id': 0,
          }
          break
        // case 'new_profile_picture':
        //   type = 'new_profile_picture'
        //   data = {
        //     'profile_picture': websocket_obj.profile_picture,
        //     'file_data': websocket_obj.file_data,
        //   }
        //   break
        case 'request_stats':
          type = 'send_stats'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'request_history':
          type = 'send_history'
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': 0,
          }
          break
        case 'user_left_game':
          type = 'user_left_game'
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
          data = {
            'user_id': websocket_obj.user_id,
            'game_id': websocket_obj.game.game_id,
          }
          break
        default:
          console.log('SOMETHING ELSE [something wrong in onmessage type]')
      }

      websocket_obj.websocket.send(JSON.stringify({
        'status': 'ok',
        'type': type,
        'data': data
      }));

      // websocket_obj.websocket.addEventListener('message', onMessage);
      websocket_obj.websocket.addEventListener('error', sendError);
      resolve() // WITHOUT this we don't return to prev functions!!

    } else {
      console.error("WebSocket connection is not open.");
      reject(new Error("WebSocket connection is not open."));
    }
  });
}
