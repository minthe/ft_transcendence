import json
import asyncio
from channels.db import database_sync_to_async
from backend_app.models import MyUser, Chat, Message, Game, Tournament
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import random





class _Game:
# ---------- HANDLE FUNCTIONS ---------------------------------------
# ---------- SEND FUNCTIONS ---------------------------------------
# ---------- DATABASE REQUEST FUNCTIONS -----------------------------
# ---------- UTILS FUNCTIONS ----------------------------------------


    # Update these methods
    async def assign_left_pedal(cls, val):
        game_state = cls.game_states.get(cls.game_id, {})
        game_state['left_pedal'] = val


    async def assign_right_pedal(cls, val):
        game_state = cls.game_states.get(cls.game_id, {})
        game_state['right_pedal'] = val


    async def increment_joined_players(cls):
        game_state = cls.game_states.get(cls.game_id, {})
        game_state['joined_players'] += 1


    async def reset_joined_players(cls):
        game_state = cls.game_states.get(cls.game_id, {})
        game_state['joined_players'] = 0


    async def calculate_ball_state(self):
        # Adjust the paddle height as needed
        print("left pedal")
        print(self.game_states.get(self.game_id, {}).get('left_pedal'))
        print("right pedal")
        print(self.game_states.get(self.game_id, {}).get('right_pedal'))

        paddle_height = 0.5
        canvas_width = 4
        canvas_height = 2

        self.game_states[self.game_id]['ball_x'] += self.game_states[self.game_id]['ball_dx']
        self.game_states[self.game_id]['ball_y'] += self.game_states[self.game_id]['ball_dy']

        # Handle ball-wall collisions
        if self.game_states[self.game_id]['ball_y'] - self.game_states[self.game_id]['ball_radius'] < 0 or \
                self.game_states[self.game_id]['ball_y'] + self.game_states[self.game_id]['ball_radius'] > canvas_height:
            self.game_states[self.game_id]['ball_dy'] *= -1

        # Handle ball-paddle collisions with left paddle
        if (
                self.game_states[self.game_id]['ball_x'] - self.game_states[self.game_id]['ball_radius'] < 0.1 and
                self.game_states[self.game_id]['left_pedal'] < self.game_states[self.game_id]['ball_y'] <
                self.game_states[self.game_id]['left_pedal'] + paddle_height
        ):
            self.game_states[self.game_id]['ball_dx'] = abs(
                self.game_states[self.game_id]['ball_dx'])  # Ensure the ball moves to the right

        # Handle ball-paddle collisions with right paddle
        if (
                self.game_states[self.game_id]['ball_x'] + self.game_states[self.game_id][
            'ball_radius'] > canvas_width - 0.1 and
                self.game_states[self.game_id]['right_pedal'] < self.game_states[self.game_id]['ball_y'] <
                self.game_states[self.game_id]['right_pedal'] + paddle_height
        ):
            self.game_states[self.game_id]['ball_dx'] = -abs(
                self.game_states[self.game_id]['ball_dx'])  # Ensure the ball moves to the left

        # Handle ball-wall collisions for left and right walls
        if self.game_states[self.game_id]['ball_x'] - self.game_states[self.game_id]['ball_radius'] < 0 + 0.025 or \
                self.game_states[self.game_id]['ball_x'] + self.game_states[self.game_id][
            'ball_radius'] - 0.025 > canvas_width:
            print("BALL HIT LEFT OR RIGHT WALL")
            if self.game_states[self.game_id]['ball_x'] - self.game_states[self.game_id]['ball_radius'] < 0 + 0.025:
                # Ball hit the left side

                self.game_states[self.game_id]['guest_score'] += 1



            elif self.game_states[self.game_id]['ball_x'] + self.game_states[self.game_id][
                'ball_radius'] - 0.025 > canvas_width:
                # Ball hit the right side

                self.game_states[self.game_id]['host_score'] += 1

            print("HOST SCORE")
            print(self.game_states[self.game_id]['host_score'])
            print("GUEST SCORE")
            print(self.game_states[self.game_id]['guest_score'])

            # Reset ball position to the center
            self.game_states[self.game_id]['ball_x'] = canvas_width // 2
            self.game_states[self.game_id]['ball_y'] = canvas_height // 2

            if (self.game_states[self.game_id]['guest_score'] == self.game_states[self.game_id]['score_limit'] or
                    self.game_states[self.game_id]['host_score'] == self.game_states[self.game_id]['score_limit']):
                self.game_states[self.game_id]['game_active'] = False
                print("GAME OVER")

            print("GAME ACTIVE state = ")
            print(self.game_states[self.game_id]['game_active'])
            await self.handle_send_score_update()


    async def game_loop(self):
        # game_status = self.game_states.get(self.game_id, {}).get('game_active')
        while True:
            # print("game_status")
            # print(game_status)
            try:
                print("CALCULATING BALL STATE")
                await self.calculate_ball_state()
                # await self.handle_send_ball_update()

                # Use channel_layer to send a message to the group directly
                await self.channel_layer.group_send(
                    self.game_group_id,
                    {
                        'type': 'send.ball.update',
                        'data': {
                            'ball_x': self.game_states[self.game_id]['ball_x'],
                            'ball_y': self.game_states[self.game_id]['ball_y'],
                        },
                    }
                )
                await asyncio.sleep(1 / 60)
                # game_status = self.game_states.get(self.game_id, {}).get('game_active')


            except Exception as e:
                print(f"Error in game_loop: {e}")
                break
            if self.game_states.get(self.game_id, {}).get('game_active') == False:
                print("in game_active = false")
                self.game_states.pop(self.game_id, None)
                print("111111")

                await self.channel_layer.group_send(
                    self.game_group_id,
                    {
                        'type': 'send.game.over',
                        'data': {

                        },
                    }
                )
                try:
                    await self.remove_ended_match(self.user['user_id'], self.game_id)
                except Exception as e:
                    print(f"Error in game_over: {e}")

                print("after remove")

                break

        print("-----GAME LOOP OVER-----")


    async def send_game_scene(self, event):
        await self.send(text_data=json.dumps({
            'type': event['data']['response_type'],
            'new_pedal_pos': event['data']['new_pedal_pos']
        }))


    async def send_init_game(self, event):
        game_instance = await self.get_game_instance(self.game_id)
        await self.send(text_data=json.dumps({
            'type': 'init_game',
            'is_host': event['data']['is_host'],
            'guest_id': game_instance.guestId,
            'host_id': game_instance.hostId#julien edited

        }))

    async def send_game_start(self, event):
        # game_info = Game.objects.get(id=self.guestId)
        await self.send(text_data=json.dumps({
            'type': 'game_start',
            
        }))


    async def send_ball_update(self, event):
        print("IN SEND BALL UPDATE")
        await self.send(text_data=json.dumps({
            'type': 'ball_update',
            'ball_x': event['data']['ball_x'],
            'ball_y': event['data']['ball_y'],

        }))


    async def send_score_update(self, event):
        print("IN SEND SCORE UPDATE")
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'host_score': event['data']['host_score'],
            'guest_score': event['data']['guest_score'],

        }))


    async def send_game_over(self, event):
        print("IN SEND BALL UPDATE")
        await self.send(text_data=json.dumps({
            'type': 'game_over',

        }))
        
    async def send_opponent_disconnected(self, event):
        print("in opponent disconnected")
        await self.send(text_data=json.dumps({
            'type': 'opponent_disconnected',

        }))

    async def send_request_invites(self, event):
        print("in send_request_invites")
        await self.send(text_data=json.dumps({
            'type': 'recieve_invites',
            'matches': event['data'],

        }))

    async def send_request_tourns(self, event):
        print("in send_request_tourns")
        await self.send(text_data=json.dumps({
            'type': 'recieve_tourns',
            'matches': event['data'],

        }))



    async def handle_send_game_scene(self):
        if self.key_code == 38:
            new_pedal_pos = self.prev_pos - 0.05
        elif self.key_code == 40:
            new_pedal_pos = self.prev_pos + 0.05
        else:
            new_pedal_pos = self.prev_pos

        if (self.is_host == True):
            response_type = 'render_left'
            await self.assign_left_pedal(new_pedal_pos)
        else:
            response_type = 'render_right'
            await self.assign_right_pedal(new_pedal_pos)

        print("RESPONSE TYPE")

        print(response_type)
        await self.channel_layer.group_send(
            self.game_group_id,
            {
                'type': 'send.game.scene',
                'data': {
                    # 'chat_id': chat_id,
                    'new_pedal_pos': new_pedal_pos,
                    'response_type': response_type

                },
            }
        )


    async def init_game_struct(self):
        if self.game_id not in self.game_states:
            self.game_states[self.game_id] = {
                'left_pedal': 0.75,
                'right_pedal': 0.75,
                'ball_x': 2,  # Initial ball position
                'ball_y': 1,  # Initial ball position
                'ball_radius': 0.05,
                'ball_speed': 0.015,
                'ball_dx': 0.025,
                'ball_dy': 0.025,
                'joined_players': 0,
                'host_score': 0,
                'guest_score': 0,
                'score_limit': 3,
                'game_active': True,
            }


    async def handle_send_init_game(self):
        await self.init_game_struct()
        return_val = await self.get_host(self.game_id, self.user['user_id'])
        print("is host status:")
        print(return_val)

        await self.increment_joined_players()
        # self.game_states.get(self.game_id, {}).get('joined_players')
        print("self.joined_players")
        print(self.game_states.get(self.game_id, {}).get('joined_players'))

        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send.init.game',
                'data': {
                    'is_host': return_val,
                    'joined_players': self.game_states.get(self.game_id, {}).get('joined_players')
                },
            }
        )
        if (self.game_states.get(self.game_id, {}).get('joined_players') == 2):
            print("TWO PLAYERS\n")
            await self.reset_joined_players()
            await self.channel_layer.group_send(
                self.game_group_id,
                {
                    'type': 'send.game.start',
                    'data': {
                        'ball_x': self.game_states.get(self.game_id, {}).get('ball_x'),
                        'ball_y': self.game_states.get(self.game_id, {}).get('ball_y')
                    },
                }
            )
            print("after TWO PLAYERS\n")

            # await self.game_loop()
            asyncio.create_task(self.game_loop())


    async def handle_send_ball_update(self):
        await self.calculate_ball_state()
        print("BALL_UPDATEEEE")
        await self.channel_layer.group_send(
            self.game_group_id,
            {
                'type': 'send.ball.update',
                'data': {
                    'ball_x': self.ball_x,
                    'ball_y': self.ball_y

                },
            }
        )
        print("sent")


    async def handle_send_score_update(self):
        print('IN HANDLE SEND SCORE UPDATE')

        try:
            await self.channel_layer.group_send(
                self.game_group_id,
                {
                    'type': 'send.score.update',
                    'data': {
                        'host_score': self.game_states[self.game_id]['host_score'],
                        'guest_score': self.game_states[self.game_id]['guest_score'],
                    },
                }
            )
        except Exception as e:
            print(f"Error in handle_send_score: {e}")

    async def handle_send_tourns(self):
        return_data = await self.get_tourns(self.user['user_id'])
        await self.channel_layer.send(
        self.channel_name,
        {
            'type': 'send.request.tourns',
            'data': return_data,
        })

    async def handle_send_invites(self):
        return_data = await self.get_matches(self.user['user_id'])
        await self.channel_layer.send(
        self.channel_name,
        {
            'type': 'send.request.invites',
            'data': return_data,
        })

    async def handle_send_join_tournament(self):
        print("in handle_send_join_tournament")
        tourn_id = await self.add_to_tourn(self.user['user_id'], self.invited_id)
        if tourn_id != None:
            await self.semiFull(tourn_id)



    # ---------------------------- DATABASE FUNCTIONS ----------------------------


    @database_sync_to_async
    def matchResults(self, game_struct):
        game_instance = Game.objects.get(id=self.game_id)
        if game_struct['host_score'] == game_struct['score_limit']:
            game_instance.winner = game_instance.hostId
            game_instance.loser = game_instance.guestId
        elif game_struct['guest_score'] == game_struct['score_limit']:
            game_instance.winner = game_instance.guestId
            game_instance.loser = game_instance.hostId
        if game_instance.tournId != 0:
            tourn_instance = Tournament.objects.get(id=game_instance.tournId)
            tourn_instance.active_matches.remove(game_instance)
            return tourn_instance.id
            tourn_instance.finalMatch.append(MyUser.objects.get(name=game_instance.winnerId))
            tourn_instance.save()
            if len(tourn_instance.finalMatch) == 2:
                game_instance = Game.objects.create()
                game_instance.hostId = tourn_instance.finalMatch[0]
                game_instance.guestId = tourn_instance.finalMatch[1]
                tourn_instance.active_matches.add(game_instance)
                game_instance.tournId = tourn_instance.id
                game_instance.save()
                tourn_instance.save()

    @database_sync_to_async
    def semiFull(self, invited_id):
        print("in semiFull")

        tourn_instance = Tournament.objects.get(id=invited_id)
        if len(tourn_instance.semiMatch) == 4:
            # print("semiMatch is full")
            # print("semiMatch")
            # print(tourn_instance.semiMatch)
            print("creating gamerooms")

            semi_match = tourn_instance.semiMatch
            random.shuffle(semi_match)
            tourn_instance.semiMatch = semi_match
            tourn_instance.save()

            print("tourn_instance.semiMatch SHUFFLED")
            print(tourn_instance.semiMatch)


            for i in range(0, 4, 2):
                print("i")
                print(i)
                game_instance = Game.objects.create()
                game_instance.hostId = tourn_instance.semiMatch[i]
                game_instance.guestId = tourn_instance.semiMatch[i + 1]
                tourn_instance.active_matches.add(game_instance)
                game_instance.tournId = tourn_instance.id
                game_instance.save()
            tourn_instance.save()
            print("tourn_instance.active_matches")
            print(tourn_instance.active_matches)
            print("tourn_instance.active_matches")
            print(tourn_instance.active_matches.all())
        else:
            print("semiMatch is not full")

    @database_sync_to_async
    def add_to_tourn(self, user_id, invited_id):
        # user_id = 3
        print("user_id!!!!! tournament")
        print(user_id)
        print("invited_id")
        print(invited_id)
        host_instance = MyUser.objects.get(user_id=user_id)
        invited_instance = MyUser.objects.get(name=invited_id)

        print("invited_name!!!!! tournament")
        print(invited_instance)

        print("host_instance")
        print(host_instance)

        tourn_sessions = host_instance.tourns.all()
        exists = False
        if len(tourn_sessions) != 0:
            for tourn_session in tourn_sessions:
                print("tourn_session.hostId")
                print(tourn_session.hostId)
                if tourn_session.hostId == user_id:
                    print("---MATCH FOUND---")
                    already_inv = False
                    if len(tourn_session.semiMatch) < 4:
                        for id in tourn_session.semiMatch:
                            # print("id")
                            # print(type(id))
                            # print("invited_instance.id")
                            # print(type(invited_instance.id))
                            if int(id) == invited_instance.user_id:
                                print("[X] User is already in semiMatch")
                                already_inv = True
                                break
                        if already_inv == False:
                            print("adding to EXISTING tourn")
                            tourn_session.semiMatch.append(invited_instance.user_id)
                            invited_instance.tourns.add(tourn_session)

                            tourn_session.save()
                            print("USERS in SEMI:")
                            for value in tourn_session.semiMatch:
                                print(value)
                            if len(tourn_session.semiMatch) == 4:
                                print("semiMatch is FULL")
                                return tourn_session.id
                                # self.semiFull(tourn_session.id)
                                # try:
                                #     await self.semiFull(tourn_session.id)
                                # except Exception as e:
                                #     print(f"An exception occurred: {e}")
                    else:
                        print("DENIED invitation: finish your tournament first")
                    exists = True
        if not exists:
            print("creating a NEW tourn")
            tourn_instance = Tournament.objects.create()
            tourn_instance.semiMatch.append(user_id)
            tourn_instance.semiMatch.append(invited_instance.user_id)
            host_instance.tourns.add(tourn_instance)
            host_instance.save()

            invited_instance.tourns.add(tourn_instance)
            invited_instance.save()

            tourn_instance.hostId = user_id
            tourn_instance.save()

            print("USERS in SEMI:")

            for value in tourn_instance.semiMatch:
                print(value)


    @database_sync_to_async
    def get_host(self, game_id, user_id):
        game_instance = Game.objects.get(id=game_id)
        user_instance = MyUser.objects.get(user_id=user_id)  # changed id to user_id
        if user_instance.name == game_instance.hostId:
            self.is_host = True
            check_host = 'True'
        else:
            self.is_host = False
            check_host = 'False'
        return check_host

    @database_sync_to_async
    def get_tourns(self, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)  # changed id to user_id
        tourn_instances = user_instance.tourns.all()

        match_data = []
        for tourns in tourn_instances:
            game_sessions = tourn_instances.active_matches.all()
            tourn_host = tourns.hostId
            for game_session in game_sessions:
                player_one = game_session.hostId
                player_two = game_session.guestId
                game_id = game_session.id
                
                # Append data to the match_data list
                match_data.append({
                    'player_one': player_one,
                    'player_two': player_two,
                    'game_id': game_id,
                    'tourn_host': tourn_host
                })
        json_data = json.dumps(match_data)
        return json_data

    @database_sync_to_async
    def get_matches(self, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)  # changed id to user_id
        game_sessions = user_instance.new_matches.all()

        match_data = []

        # Iterate through game_sessions
        for game_session in game_sessions:
            # Extract opponent name and game id
            opponent_name = game_session.hostId
            game_id = game_session.id
            
            # Append data to the match_data list
            match_data.append({
                'opponent_name': opponent_name,
                'game_id': game_id
            })
        json_data = json.dumps(match_data)
        return json_data

        if user_instance.name == game_instance.hostId:
            self.is_host = True
            check_host = 'True'
        else:
            self.is_host = False
            check_host = 'False'
        return check_host

    @database_sync_to_async
    def remove_ended_match(self, user_id, game_id):
        print("in remove_ended_match")
        try:
            print("user_id")

            print(user_id)
            user1 = MyUser.objects.get(user_id=user_id)  # changed id to user_id
            game_instance = Game.objects.get(id=game_id)
            user1.new_matches.remove(game_instance)
            game_instance.delete()
        except MyUser.DoesNotExist:
            return None

    @database_sync_to_async#julien edited
    def get_game_instance(self, game_id):
        try:
            game_instance = Game.objects.get(id=game_id)
            return game_instance
        except Game.DoesNotExist:
            return None