
function chatDom() {
  // document.getElementById('sendMessageButton').addEventListener('click', async function () {
  //   const isBlocked = websocket_obj.blocked_by && websocket_obj.blocked_by.includes(websocket_obj.chat_name);
  //   if (isBlocked) {
  //     $('#userBlockedYouWarning').modal('show');
  //     return
  //   }
  //   websocket_obj.message = document.getElementById('messageInput').value
  //   websocket_obj.sender = websocket_obj.username
  //   document.getElementById('messageInput').value = ''
  //   await sendDataToBackend('send_chat_message')
  //   await sendDataToBackend('get_online_stats')
  //   await sendDataToBackend('get_chat_messages')
  // });

  // document.getElementById('invite_user_button').addEventListener('click', async function () {
  //   const invited_user_name = document.getElementById('invite_user').value
  //   document.getElementById('invite_user').value = ''
  //   await inviteUser(invited_user_name)
  // })

  // document.getElementById('logoutButton').addEventListener('click', async function () {
  //   await logoutUser()
  // })

  // document.getElementById('create_public_chat_button').addEventListener('click', async function() {
  //   await createPublicChat()
  // })

  // document.getElementById('create_private_chat_button').addEventListener('click', async function() {
  //   await createPrivateChat()
  // })

  // document.getElementById('close_button_clicked_user').addEventListener('click', async function() {
  //   const public_chat_backdrop = document.getElementById('publicChatModal')
  //   public_chat_backdrop.style.opacity = 1;
  // })

  // document.getElementById('goToChatButton').addEventListener('click', async function(){
  //   console.log('secondChat show button');


  //   const clicked_user = document.getElementById('backdropClickedUserLabel')
  //   let chatNameToFind = clicked_user.textContent;
  //   let foundChat = websocket_obj.chat_data.find(chat=> chat.chat_name === chatNameToFind);
  //   if (foundChat) {
  //     await handleClickedOnChatElement(foundChat);
  //     document.getElementById('publicChatModal').style.opacity = 1
  //     $('#staticBackdropProfile').modal('hide');
  //     $('#backdropClickedUser').modal('hide');
  //   } else {
  //     websocket_obj.new_private_chat_name = chatNameToFind
  //     await sendDataToBackend('set_new_private_chat')
  //     await sendDataToBackend('get_current_users_chats')
  //     document.getElementById('goToChatButton').textContent = 'Go to Chat'
  //     hideDiv('create_chat_alert')
  //   }
  // })

  // document.getElementById('blockUserButton').addEventListener('click', async function() {
  //   await sendDataToBackend('block_user')
  //   $('#backdropPrivateProfile').modal('hide');
  // })

  // document.getElementById('unblockUserButton').addEventListener('click',  async function () {
  //   await sendDataToBackend('unblock_user')
  //   $('#backdropPrivateProfile').modal('hide');
  // })

  // document.getElementById('right-heading-name').addEventListener('click', async function() {
  //   const state = document.getElementById('right-heading-name').dataset.state
  //   console.log('STATE: ', state)

  //   if (state === 'private') {
  //     await showPrivateChatModal()
  //   } else {
  //     await showPublicChatModal()
  //   }
  // })


//   document.getElementById('challengeUserToGame').addEventListener('click', async function() {
    
//     console.log('In inviting through chat')
//     // const username = websocket_obj.username;
//     sendDataToBackend('get_user_in_current_chat')
//     console.log('get_user_in_current_chat ', websocket_obj.userInCurrentChat)

//     function findOtherUserName(users, username) {
//       for (let i = 0; i < users.length; i++) {
//           if (users[i].user_name !== username) {
//               return users[i].user_name;
//           }
//       }
//       return null; // Return null if the username is not found
//   }
//     const invited_username = findOtherUserName(websocket_obj.userInCurrentChat, websocket_obj.username);
//     console.log('invited_username ', invited_username)
//     // const invited_username = 'test'
//     websocket_obj.invited_id = invited_username
    
//     try {
//       const response = await fetch(`${window.location.origin}/user/game/create/${websocket_obj.username}/${websocket_obj.invited_id}`);
//       const data = await response.json();
  
  
  
//       console.log('DATA ', data);
//       // websocket_obj.active_game = data.id;
  
//       if (response.ok) {
//       displayError(null);
//       websocket_obj.active_game = data.id;
//       // console.log(data.id); // Check the console for the result
  
//       // Perform actions on successful login, e.g., set isLoggedIn and userData
//           console.log(data);
//       } else {
//       displayError(data.error);
//       }
//     } catch (error) {
//       console.error('Error fetching user data:', error);
//       displayError('Error fetching user data');
//     }
//   })
// }



  // document.getElementById('challengeUserToGame').addEventListener('click', async function() {
    
  //   console.log('In inviting through chat')
  //   // const username = websocket_obj.username;
  //   sendDataToBackend('get_user_in_current_chat')
  //   console.log('get_user_in_current_chat ', websocket_obj.userInCurrentChat)

  //   function findOtherUserName(users, username) {
  //     for (let i = 0; i < users.length; i++) {
  //         if (users[i].user_name !== username) {
  //             return users[i].user_name;
  //         }
  //     }
  //     return null; // Return null if the username is not found
  // }
  //   const invited_username = findOtherUserName(websocket_obj.userInCurrentChat, websocket_obj.username);
  //   console.log('invited_username ', invited_username)
  //   // const invited_username = 'test'
  //   websocket_obj.invited_id = invited_username
    
  //   try {
  //     const response = await fetch(`${window.location.origin}/user/game/create/${websocket_obj.username}/${websocket_obj.invited_id}`);
  //     const data = await response.json();
  
  
  
  //     console.log('DATA ', data);
  //     // websocket_obj.active_game = data.id;
  
  //     if (response.ok) {
  //     displayError(null);
  //     websocket_obj.active_game = data.id;
  //     // console.log(data.id); // Check the console for the result
  
  //     // Perform actions on successful login, e.g., set isLoggedIn and userData
  //         console.log(data);
  //     } else {
  //     displayError(data.error);
  //     }
  //   } catch (error) {
  //     console.error('Error fetching user data:', error);
  //     displayError('Error fetching user data');
  //   }
  

  // //   try {
  

  // //     const response = await fetch(`${window.location.origin}/user/game/render/invites/${username}/`);
  // //     const htmlContent = await response.text();
  
  // //     const container = document.getElementById('game-session-container');
  // //     container.innerHTML = htmlContent;
  
  // // } catch (error) {
  // //     console.error('There was a problem with the fetch operation:', error);
  // // }
  

  //   // await sendDataToBackend('new_invite')

    

  // })



}


async function showPrivateChatModal() {
  if (websocket_obj.blocked_user && websocket_obj.blocked_user.includes(websocket_obj.chat_name)) {
    showDiv('unblockUserButton')
    hideDiv('blockUserButton')
  } else {
    showDiv('blockUserButton')
    hideDiv('unblockUserButton')
  }
  $('#backdropPrivateProfile').modal('show');
}

async function showPublicChatModal() {
  const dropdownMenu = document.getElementById('dynamicContactsDropdown');
  dropdownMenu.innerHTML = ''
  const all_private_chats = websocket_obj.chat_data
    .filter(chat => chat.isPrivate)
    .map(chat => chat.chat_name);

  const user_not_in_chat = websocket_obj.all_user
    .filter(user => user.name && !all_private_chats.includes(user.name))
    .filter(user => !websocket_obj.userInCurrentChat.some(currentChatUser => currentChatUser.user_name === user.name));
  user_not_in_chat.forEach(user => {
    const listItem = document.createElement('li');
    const button = document.createElement('button');
    button.className = 'dropdown-item';
    button.type = 'button';
    button.textContent = user.name;
    button.addEventListener('click', async () => {
      await inviteUser(user.name);
    });
    listItem.appendChild(button);
    dropdownMenu.appendChild(listItem);
  });
  $('#staticBackdropProfile').modal('show');
}


async function logoutUser() {
  let websocket_obj = null
  showDiv('userIsNotAuth')
  hideDiv('userIsAuth')
}

async function inviteUser(invited_user_name){
  websocket_obj.invited_user_name = invited_user_name
  await sendDataToBackend('set_invited_user_to_chat')
  await sendDataToBackend('get_current_users_chats')
}

async function leaveChat() {
  await sendDataToBackend('set_user_left_chat')
  await sendDataToBackend('get_current_users_chats')
}

async function createPublicChat() {
  let chat_name = document.getElementById('new_chat_name').value
  if (chat_name.trim() === '') {
    setErrorWithTimout('info_create_chat', 'Chat name cannot be empty',  5000)
    return;
  }
  
  await sendDataToBackend('set_new_chat')
  let chatNameLabel = document.getElementById('new_chat_name');
  chatNameLabel.value = '';
  chatNameLabel.textContent = '';
}

async function createPrivateChat() {
  let chat_name = document.getElementById('new_private_chat_name').value
  if (chat_name.trim() === '') {
    setErrorWithTimout('info_create_private_chat', 'Username cannot be empty',  5000)
    return;
  }
  websocket_obj.new_private_chat_name = chat_name
  await sendDataToBackend('set_new_private_chat')
  await sendDataToBackend('get_current_users_chats')
  let chatNameLabel = document.getElementById('new_private_chat_name');
  chatNameLabel.value = '';
  chatNameLabel.textContent = '';
}

async function renderProfile() {
  document.getElementById('displayUserName').textContent = 'Hey '+websocket_obj.username+' 🫠';
}

async function handleClickedOnChatElement(chat_obj) {
  const chat_avatar = document.getElementById('chat_avatar');

  console.log('which chat is it: ', chat_obj.chat_name);
  if (!state.chatOpen || state.chatObj.chat_name !== chat_obj.chat_name) {
    showDiv('messageSide')

    // const chat_avatar = document.getElementById('chat_avatar')
    if (!chat_obj.isPrivate) {
      // avatar for group picture
      chat_avatar.src = 'https://www.shareicon.net/data/512x512/2016/01/09/700702_network_512x512.png'
    } else if (chat_obj.avatar) {
      chat_avatar.src = chat_obj.avatar
    } else {
      // default avatar
      chat_avatar.src = 'https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png'
    }
    document.getElementById('right-heading-name').textContent = chat_obj.chat_name
    if (chat_obj.isPrivate) {
      document.getElementById('backdropPrivateProfileLabel').textContent = chat_obj.chat_name
      document.getElementById('right-heading-name').dataset.state = 'private'
    } else {
      document.getElementById('backdropPublicProfileLabel').textContent = chat_obj.chat_name
      document.getElementById('right-heading-name').dataset.state = 'public'
    }
    websocket_obj.chat_id = chat_obj.chat_id;
    websocket_obj.chat_name = chat_obj.chat_name;

    // console.log('chat obj### : ', chat_obj.chat_id);
    // console.log('chat name### : ', chat_obj.chat_name);

    await sendDataToBackend('get_online_stats')
    await sendDataToBackend('get_user_in_current_chat')
    await sendDataToBackend('get_chat_messages')

    
    state.chatOpen = true;
  }
  else if (state.chatOpen) {
    console.log('goes back to default and closes');
    hideDiv('messageSide');
    document.getElementById('right-heading-name').textContent = "";
    chat_avatar.src = "../img/ballWithEye.jpg";
    state.chatOpen = false;
    window.history.back();
  }
  if (state.currPage !== 'group_chat' || state.chatObj.chat_name !== chat_obj.chat_name) {
    state.currPage = 'group_chat';
    state.chatObj = chat_obj;
    handleButtonClick("");
  }
}








async function renderMessages() {
  let myArray = websocket_obj.messages.message_data;
  renderUserInChatList()
  let mainContainer = document.getElementById('messageContainer');
  mainContainer.innerHTML = '';
  if (!myArray) { return }
  let tmpDiv = [];
  for (let i = 0; i < myArray.length; i++) {
    let messageDiv = document.createElement('div');
    let contentDiv = document.createElement('div');
    let titleElement = document.createElement('div');
    let timestampElement = document.createElement('div');
    let textDiv = document.createElement('div');
    textDiv.classList.add('text-break');
    textDiv.textContent = myArray[i].text;
    timestampElement.textContent = myArray[i].timestamp;
    if (websocket_obj.username === myArray[i].sender) {
      titleElement.classList.add('sender-title')
      titleElement.textContent = 'You';
      messageDiv.style.textAlign = 'right';
      contentDiv.classList.add('sender-message-content');
      timestampElement.classList.add('sender-timestamp');
    }
    else {
      titleElement.classList.add('receiver-title')
      contentDiv.classList.add('receiver-message-content');
      timestampElement.classList.add('receiver-timestamp');
      const currentUserId = myArray[i].sender_id
      function hasMatchingUserId(user) {
        return user.user_id === currentUserId;
      }
      if (websocket_obj.onlineStats.some(hasMatchingUserId)) {
        titleElement.textContent = myArray[i].sender + ' 🟢';
      } else {
        titleElement.textContent = myArray[i].sender + ' 🔴';
      }
    }
    contentDiv.appendChild(titleElement);
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timestampElement);
    messageDiv.appendChild(contentDiv);
    tmpDiv.push(messageDiv);
  }
  for (let i = 0; i < myArray.length; i++) {
    mainContainer.appendChild(tmpDiv[i]);
    if (i < tmpDiv.length - 1) {
      mainContainer.appendChild(document.createElement('br'));
    }
  }
  // THIS scrolls to the bottom of messageDiv by default (user sees last messages first)
  mainContainer.scrollTo(0, mainContainer.scrollHeight);
}

function renderUserInChatList() {
  let mainContainer = document.getElementById('userInChatList');
  mainContainer.innerHTML = '';
  let myArray = websocket_obj.userInCurrentChat
  let title = document.createElement('h2');
  title.textContent = 'User in Chat:'
  mainContainer.appendChild(title);
  // own user always first in the list
  const own_user = document.createElement('div');
  own_user.classList.add('row', 'own-user-in-chat-profile');
  own_user.textContent = 'You';
  mainContainer.appendChild(own_user)
  for (let i = 0; i < myArray.length; i++) {
    if (myArray[i].user_name !== websocket_obj.username) {
      const chat_element = document.createElement('div');
      chat_element.classList.add('row', 'contacts-in-chat-profile');
      chat_element.textContent = myArray[i].user_name;
      chat_element.addEventListener('click', async function () {
        await handleClickedElementInPublicChatModal(myArray[i].user_name);
      });
      mainContainer.appendChild(chat_element)
    }
  }
}

async function handleClickedElementInPublicChatModal(clickedUser) {
  const modal = new bootstrap.Modal(document.getElementById('backdropClickedUser'));
  document.getElementById('publicChatModal').style.opacity = 0.5;
  document.getElementById('backdropClickedUserLabel').textContent = clickedUser
  const chat_exist = websocket_obj.chat_data.some(chat => chat.chat_name === clickedUser);
  if (!chat_exist) {
    document.getElementById('goToChatButton').textContent = 'Create Chat'
    showDiv('create_chat_alert')
  }
  modal.show();
}

async function renderChat() {
  const chats_container = document.getElementById('chatsLeftSide')
  chats_container.innerHTML = ''
  let myArray = sortChats(websocket_obj.chat_data)
  myArray.forEach(chat => {
    const chat_element = document.createElement('div');
    chat_element.classList.add('row', 'sideBar-body');
    const avatarCol = document.createElement('div');
    avatarCol.classList.add('col-sm-3', 'col-xs-3', 'sideBar-avatar');
    const avatarIcon = document.createElement('div');
    avatarIcon.classList.add('avatar-icon');
    const avatarImg = document.createElement('img');

    if (!chat.isPrivate) {
      // avatar for group picture
      avatarImg.src = 'https://www.shareicon.net/data/512x512/2016/01/09/700702_network_512x512.png'
    } else if (chat.avatar) {
      avatarImg.src = chat.avatar
    } else {
      // default avatar
      avatarImg.src = 'https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png'
    }
    avatarIcon.appendChild(avatarImg);
    avatarCol.appendChild(avatarIcon);
    const mainCol = document.createElement('div');
    mainCol.classList.add('col-sm-9', 'col-xs-9', 'sideBar-main');
    const rowDiv = document.createElement('div');
    rowDiv.classList.add('row');
    const nameCol = document.createElement('div');
    nameCol.classList.add('col-sm-8', 'col-xs-8', 'sideBar-name');
    let chatName = document.createElement('div');
    chatName.textContent = chat.chat_name;
    chat_element.addEventListener('click', async function () {
      await handleClickedOnChatElement(chat);
    });
    nameCol.appendChild(chatName);
    const timeCol = document.createElement('div');
    timeCol.classList.add('col-sm-4', 'col-xs-4', 'pull-right', 'sideBar-time');
    const timeSpan = document.createElement('span');
    timeSpan.classList.add('time-meta', 'pull-right');
    timeSpan.textContent = getTimestamp(chat)
    timeCol.appendChild(timeSpan);
    rowDiv.appendChild(nameCol);
    rowDiv.appendChild(timeCol);
    mainCol.appendChild(rowDiv);
    chat_element.appendChild(avatarCol);
    chat_element.appendChild(mainCol);
    chats_container.appendChild(chat_element);
  });
}

function getTimestamp(chat) {
  const dateString = chat.last_message["time"]
  if (dateString === '0') { return '' }
  let dateParts = dateString.split(' ');
  const timePart = dateParts[0];
  const datePart = dateParts[1];
  const currentDate = new Date();
  dateParts = datePart.split('.');
  const day = parseInt(dateParts[0], 10);
  const month = parseInt(dateParts[1], 10);
  const year = parseInt(dateParts[2], 10);
  const date = new Date(year, month - 1, day);
  const yesterday = new Date(currentDate);
  yesterday.setDate(currentDate.getDate() - 1);
  const isYesterday =
    date.getDate() === yesterday.getDate() &&
    date.getMonth() === yesterday.getMonth() &&
    date.getFullYear() === yesterday.getFullYear();
  if (isYesterday) {
    return 'yesterday'
  } else if (date < yesterday) {
    return datePart
  } else {
    return timePart
  }
}

function sortChats(chats){
  chats.sort(compareChats);
  return chats
}

function compareChats(chat1, chat2) {
  var time1 = parseTimeString(chat1.last_message["time"]);
  var time2 = parseTimeString(chat2.last_message["time"]);
  // Handle the case where one of the timestamps is '0'
  if (time1 === '0') { return 1 }
  if (time2 === '0') { return -1 }
  if (time1.getFullYear() !== time2.getFullYear()) {
    return time2.getFullYear() - time1.getFullYear();
  }
  if (time1.getMonth() !== time2.getMonth()) {
    return time2.getMonth() - time1.getMonth();
  }
  if (time1.getDate() !== time2.getDate()) {
    return time2.getDate() - time1.getDate();
  }
  return time2.getHours() * 60 + time2.getMinutes() - (time1.getHours() * 60 + time1.getMinutes());
}

function parseTimeString(timeString) {
  if (timeString === '0') {
    return new Date(0); // Set to the epoch for '0' timestamp
  }
  var [hours, minutes, day, month, year] = timeString.match(/\d+/g);
  return new Date(year, month - 1, day, hours, minutes);
}


function findOtherUserName(users, username) {
	for (let i = 0; i < users.length; i++) {
		if (users[i].user_name !== username) {
			return users[i].user_name;
		}
	}
	return null; // Return null if the username is not found
}


















async function chatSiteClicked() {
  await sendDataToBackend('get_current_users_chats')
  await sendDataToBackend('get_blocked_by_user')
  await sendDataToBackend('get_blocked_user') // NEW since 02.02
  showSiteHideOthers('chat')
  hideDiv('messageSide');
  document.getElementById('right-heading-name').textContent = "";
  chat_avatar.src = "../img/ballWithEye.jpg";
  
  state.chatOpen = false;
}

function invSiteClicked() {
  state.currPage = 'invites';
  handleButtonClick("");
}

async function sendMessage() {
  const isBlocked = websocket_obj.blocked_by && websocket_obj.blocked_by.includes(websocket_obj.chat_name);
    if (isBlocked) {
      $('#userBlockedYouWarning').modal('show');
      return
    }
    websocket_obj.message = document.getElementById('messageInput').value
    websocket_obj.sender = websocket_obj.username
    document.getElementById('messageInput').value = ''
    await sendDataToBackend('send_chat_message')
    await sendDataToBackend('get_online_stats')
    await sendDataToBackend('get_chat_messages')
}

async function openChat() {
  const clicked_user = document.getElementById('backdropClickedUserLabel')
  let chatNameToFind = clicked_user.textContent;
  let foundChat = websocket_obj.chat_data.find(chat=> chat.chat_name === chatNameToFind);
  if (foundChat) {
    await handleClickedOnChatElement(foundChat);
    document.getElementById('publicChatModal').style.opacity = 1
    $('#staticBackdropProfile').modal('hide');
    $('#backdropClickedUser').modal('hide');
  } else {
    websocket_obj.new_private_chat_name = chatNameToFind
    await sendDataToBackend('set_new_private_chat')
    await sendDataToBackend('get_current_users_chats')
    document.getElementById('goToChatButton').textContent = 'Go to Chat'
    hideDiv('create_chat_alert')
  }
}

async function challengeUserClicked() {
  console.log('In inviting through chat')
  // const username = websocket_obj.username;
  sendDataToBackend('get_user_in_current_chat')
  console.log('get_user_in_current_chat ', websocket_obj.userInCurrentChat)

  const invited_username = findOtherUserName(websocket_obj.userInCurrentChat, websocket_obj.username);
  console.log('invited_username ', invited_username)
  // const invited_username = 'test'
  websocket_obj.invited_id = invited_username 
  try {
    const response = await fetch(`${window.location.origin}/user/game/create/${websocket_obj.username}/${websocket_obj.invited_id}`);
    const data = await response.json();
    console.log('DATA ', data);
    // websocket_obj.active_game = data.id;

    if (response.ok) {
    displayError(null);
    websocket_obj.active_game = data.id;
    // console.log(data.id); // Check the console for the result

    // Perform actions on successful login, e.g., set isLoggedIn and userData
        console.log(data);
    } else {
    displayError(data.error);
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    displayError('Error fetching user data');
  }
}

async function inviteUserClicked() {
  const invited_user_name = document.getElementById('invite_user').value
  document.getElementById('invite_user').value = ''
  await inviteUser(invited_user_name)
}

async function closeButtonClicked() {
  const public_chat_backdrop = document.getElementById('publicChatModal')
  public_chat_backdrop.style.opacity = 1;
}

async function blockUserClicked() {
  await sendDataToBackend('block_user')
  $('#backdropPrivateProfile').modal('hide');
}

async function unblockUserClicked() {
  await sendDataToBackend('unblock_user')
  $('#backdropPrivateProfile').modal('hide');
}

async function rightHeadingClicked() {
  const state = document.getElementById('right-heading-name').dataset.state
  console.log('STATE: ', state)

  if (state === 'private')
    await showPrivateChatModal()
  else
    await showPublicChatModal()
}