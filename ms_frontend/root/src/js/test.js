<div id="right-heading-name" class="heading-name-meta" data-state="private">c</div>














<div id="chat" class="chat hidden"><div class="row app g-0">
  <div id="chat-area" class="col-sm-4">
    <div class="row left-heading">
      <div class="col-sm-3 col-xs-3 heading-avatar">
        <button class="btn btn-outline-dark profile-button" data-bs-toggle="modal" data-bs-target="#backdropSettings"></button>
        <div id="userChatsList"></div>
        <div class="modal fade" id="backdropSettings" data-bs-keyboard="false" tabindex="-1" aria-labelledby="backdropSettingsLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="backdropSettingsLabel">Settings</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="New public Chat..." aria-label="Chat Name" id="new_chat_name" aria-describedby="create_public_chat_button">
                  <button class="btn btn-outline-success" type="button" id="create_public_chat_button">Create</button>
                </div>
                <div id="info_create_chat"></div>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="New private Chat..." aria-label="Chat Name" id="new_private_chat_name" aria-describedby="create_private_chat_button">
                  <button class="btn btn-outline-success" type="button" id="create_private_chat_button">Create</button>
                </div>
                <div id="info_create_private_chat"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="chatsLeftSide" class="scroll-contacts"><div class="row sideBar-body"><div class="col-sm-3 col-xs-3 sideBar-avatar"><div class="avatar-icon"><img src="https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png"></div></div><div class="col-sm-9 col-xs-9 sideBar-main"><div class="row"><div class="col-sm-8 col-xs-8 sideBar-name"><div>ff</div></div><div class="col-sm-4 col-xs-4 pull-right sideBar-time"><span class="time-meta pull-right">16:29</span></div></div></div></div><div class="row sideBar-body"><div class="col-sm-3 col-xs-3 sideBar-avatar"><div class="avatar-icon"><img src="https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png"></div></div><div class="col-sm-9 col-xs-9 sideBar-main"><div class="row"><div class="col-sm-8 col-xs-8 sideBar-name"><div>b</div></div><div class="col-sm-4 col-xs-4 pull-right sideBar-time"><span class="time-meta pull-right">16:22</span></div></div></div></div><div class="row sideBar-body"><div class="col-sm-3 col-xs-3 sideBar-avatar"><div class="avatar-icon"><img src="https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png"></div></div><div class="col-sm-9 col-xs-9 sideBar-main"><div class="row"><div class="col-sm-8 col-xs-8 sideBar-name"><div>c</div></div><div class="col-sm-4 col-xs-4 pull-right sideBar-time"><span class="time-meta pull-right">25.03.2024</span></div></div></div></div><div class="row sideBar-body"><div class="col-sm-3 col-xs-3 sideBar-avatar"><div class="avatar-icon"><img src="https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png"></div></div><div class="col-sm-9 col-xs-9 sideBar-main"><div class="row"><div class="col-sm-8 col-xs-8 sideBar-name"><div>lol private shit backend CONSUMERS.py</div></div><div class="col-sm-4 col-xs-4 pull-right sideBar-time"><span class="time-meta pull-right">17.03.2024</span></div></div></div></div></div>
  </div>
  <div class="col-sm-8 conversation">
    <div class="row heading g-0">
      <div class="col-sm-2 col-md-1 col-xs-3 heading-avatar">
        <div class="heading-avatar-icon">
          <img id="chat_avatar" src="https://miro.medium.com/v2/resize:fit:720/1*W35QUSvGpcLuxPo3SRTH4w.png">
        </div>
      </div>
      <div class="col-sm-8 col-xs-7 heading-name">
        <div id="right-heading-name" class="heading-name-meta" data-state="private">b</div>
      </div>
      <div class="col">

        <!-- MODAL FOR PRIVATE CHATS-->
        <div class="modal fade" id="backdropPrivateProfile" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="backdropPrivateProfileLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title" id="backdropPrivateProfileLabel">b</h1>
              </div>
              <div class="modal-body">
                <button id="blockUserButton" class="btn btn-outline-danger hidden">block User</button>
                <button id="unblockUserButton" class="btn btn-outline-warning hidden">unblock User</button>
<!--?           TODO: KRISTINA:-->
                <button id="challengeUserToGame" class="btn btn-outline-success">challenge User [coming soon]</button>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" id="close_button" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>

        <!-- MODAL FOR PUBLIC CHATS-->
        <div id="publicChatModal">
        <div class="modal fade" id="staticBackdropProfile" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="backdropPublicProfileLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title" id="backdropPublicProfileLabel"></h1>
              </div>
              <div class="modal-body">
                <div id="userInChatList"><h2>User in Chat:</h2><div class="row own-user-in-chat-profile">You</div><div class="row contacts-in-chat-profile">b</div></div><br>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="Invite User..." aria-label="Recipient's username" id="invite_user" aria-describedby="invite_user_button">
                  <button class="btn btn-outline-success" type="button" id="invite_user_button">Invite</button>
                </div>
                <div class="dropdown">
                  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    All User
                  </button>
                  <ul id="dynamicContactsDropdown" class="dropdown-menu" style="max-height: 200px; overflow-y: auto;"></ul>
                </div>
                <div id="message_with_timeout"></div><br>
                <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#staticBackdrop2">Leave Chat
                </button><br><br>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" id="close_button" data-bs-dismiss="modal">Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

        <!-- MODAL FOR CLICKED USER-->
        <div class="modal fade" id="backdropClickedUser" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="backdropClickedUserLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-scrollable">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title" id="backdropClickedUserLabel"></h1>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col">
                    <button id="goToChatButton" class="btn btn-outline-dark">Go to Chat</button>
                  </div>
                  <div class="col">
                    <div id="create_chat_alert" class="alert alert-warning hidden" role="alert">
                      You don't have a Chat with this User yet
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" id="close_button_clicked_user" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>

        <!-- NESTED MODAL, LEAVE CHAT -->
        <div class="modal fade" id="staticBackdrop2" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel2" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="staticBackdropLabel2">Leave Chat</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                Are you sure you want to leave the Chat?
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal" onclick="leaveChat()">Yes, I
                  want to leave
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL FOR IF USER IS BLOCKED -->
    <div class="modal fade" id="userBlockedYouWarning" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content user-blocked-you-warning">
          <div class="modal-body">
            ❗️This User blocked you
          </div>
        </div>
      </div>
    </div>
    <div id="messageSide" class="row">
      <div id="messageContainer" class="scroll-messages"><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">hello</div><div class="sender-timestamp">11:02 18.03.2024</div></div></div><br><div><div class="receiver-message-content"><div class="receiver-title">b 🟢</div><div class="text-break">test</div><div class="receiver-timestamp">11:02 18.03.2024</div></div></div><br><div><div class="receiver-message-content"><div class="receiver-title">b 🟢</div><div class="text-break">who</div><div class="receiver-timestamp">17:44 24.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">test</div><div class="sender-timestamp">18:07 24.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">ertregb</div><div class="sender-timestamp">18:28 24.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">adsfsadf</div><div class="sender-timestamp">18:28 24.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">afdsf</div><div class="sender-timestamp">18:28 24.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">test</div><div class="sender-timestamp">16:04 25.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">test</div><div class="sender-timestamp">23:59 29.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break"></div><div class="sender-timestamp">23:59 29.03.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break">etraeg</div><div class="sender-timestamp">16:22 01.04.2024</div></div></div><br><div style="text-align: right;"><div class="sender-message-content"><div class="sender-title">You</div><div class="text-break"></div><div class="sender-timestamp">16:22 01.04.2024</div></div></div></div>
      <div class="input-group format-input-group">
        <input type="text" class="lel form-control" style="color: white; background-color: #212121; border: none" placeholder="Type your message..." id="messageInput">
        <button id="sendMessageButton" class="btn btn-dark">Send</button>
      </div>
    </div>
  </div>
</div>