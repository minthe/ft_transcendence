import json
import asyncio
from channels.db import database_sync_to_async
from backend_app.models import MyUser, Chat, Message, Game, Tournament
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils import timezone
import random

class _Game:

    # Update these methods
    async def assign_left_pedal(cls, val):
        game_state = cls.game_states.get(cls.stable_game_id, {})
        game_state['left_pedal'] = val

    async def assign_right_pedal(cls, val):
        game_state = cls.game_states.get(cls.stable_game_id, {})
        game_state['right_pedal'] = val


    async def increment_joined_players(cls):
        game_state = cls.game_states.get(cls.stable_game_id, {})
        game_state['joined_players'] += 1

    async def decrement_joined_players(cls):
        game_state = cls.game_states.get(cls.stable_game_id, {})
        game_state['joined_players'] -= 1

    async def reset_joined_players(cls):
        game_state = cls.game_states.get(cls.stable_game_id, {})
        game_state['joined_players'] = 0


    async def calculate_ball_state(self):
        paddle_height = 0.5
        canvas_width = 4
        canvas_height = 2
        enhancer = 4.0

        self.game_states[self.stable_game_id]['ball_x'] += self.game_states[self.stable_game_id]['ball_dx'] * enhancer
        self.game_states[self.stable_game_id]['ball_y'] += self.game_states[self.stable_game_id]['ball_dy'] * enhancer

        # Handle ball-wall collisions
        if self.game_states[self.stable_game_id]['ball_y'] - self.game_states[self.stable_game_id]['ball_radius'] < 0 or \
                self.game_states[self.stable_game_id]['ball_y'] + self.game_states[self.stable_game_id]['ball_radius'] > canvas_height:
            self.game_states[self.stable_game_id]['ball_dy'] *= -1

        # Handle ball-paddle collisions with left paddle
        if (
                self.game_states[self.stable_game_id]['ball_x'] - self.game_states[self.stable_game_id]['ball_radius'] < 0.1 and
                self.game_states[self.stable_game_id]['left_pedal'] < self.game_states[self.stable_game_id]['ball_y'] <
                self.game_states[self.stable_game_id]['left_pedal'] + paddle_height
        ):
            self.game_states[self.stable_game_id]['ball_dx'] = abs(
                self.game_states[self.stable_game_id]['ball_dx'])  # Ensure the ball moves to the right

        # Handle ball-paddle collisions with right paddle
        if (
                self.game_states[self.stable_game_id]['ball_x'] + self.game_states[self.stable_game_id][
            'ball_radius'] > canvas_width - 0.1 and
                self.game_states[self.stable_game_id]['right_pedal'] < self.game_states[self.stable_game_id]['ball_y'] <
                self.game_states[self.stable_game_id]['right_pedal'] + paddle_height
        ):
            self.game_states[self.stable_game_id]['ball_dx'] = -abs(
                self.game_states[self.stable_game_id]['ball_dx'])  # Ensure the ball moves to the left

        # Handle ball-wall collisions for left and right walls
        if self.game_states[self.stable_game_id]['ball_x'] - self.game_states[self.stable_game_id]['ball_radius'] < 0 + 0.025 or \
                self.game_states[self.stable_game_id]['ball_x'] + self.game_states[self.stable_game_id][
            'ball_radius'] - 0.025 > canvas_width:
            if self.game_states[self.stable_game_id]['ball_x'] - self.game_states[self.stable_game_id]['ball_radius'] < 0 + 0.025:
                self.game_states[self.stable_game_id]['guest_score'] += 1

            elif self.game_states[self.stable_game_id]['ball_x'] + self.game_states[self.stable_game_id][
                'ball_radius'] - 0.025 > canvas_width:
                self.game_states[self.stable_game_id]['host_score'] += 1

            # Reset ball position to the center
            self.game_states[self.stable_game_id]['ball_x'] = canvas_width // 2
            self.game_states[self.stable_game_id]['ball_y'] = canvas_height // 2

            if (self.game_states[self.stable_game_id]['guest_score'] == self.game_states[self.stable_game_id]['score_limit'] or
                    self.game_states[self.stable_game_id]['host_score'] == self.game_states[self.stable_game_id]['score_limit']):
                self.game_states[self.stable_game_id]['game_active'] = False
            await self.handle_send_score_update()


    async def game_loop(self):
        while True:
            try:
                await self.calculate_ball_state()
                if self.game_states.get(self.stable_game_id, {}).get('group_id') is not None:
                    await self.channel_layer.group_send(
                        self.game_states.get(self.stable_game_id, {}).get('group_id'),
                        {
                            'type': 'send.ball.update',
                            'data': {
                                'ball_x': self.game_states[self.stable_game_id]['ball_x'],
                                'ball_y': self.game_states[self.stable_game_id]['ball_y'],
                            },
                        }
                    )
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error in game_loop: {e}")
                break
            if self.game_states.get(self.stable_game_id, {}).get('game_active') == False:
                if self.game_states[self.stable_game_id]['canceled'] == True:
                    break
                await self.setWinner(self.game_states[self.stable_game_id])
                return_data = await self.matchResults()
                if return_data:
                    await self.channel_layer.send(
                        self.channel_name,
                        {
                            'type': 'send.chatbot.trigger',
                            'data': return_data,
                        })
                if self.game_states.get(self.stable_game_id, {}).get('group_id') is not None:
                    await self.channel_layer.group_send(
                        self.game_states.get(self.stable_game_id, {}).get('group_id'),
                        {
                            'type': 'send.game.over',
                            'data': {
                                'game_id': self.stable_game_id,

                            },
                        }
                    )
                try:
                    await self.remove_ended_match(self.user['user_id'], self.stable_game_id)
                except Exception as e:
                    print(f"Error in game_over: {e}")
                break

        self.game_states[self.stable_game_id]['game_loop_task'] = None
        tmp_id = self.game_states.get(self.stable_game_id, {}).get('group_id')
        prefixed_value = f"b_{tmp_id}"
        self.game_states.pop(self.stable_game_id, None)
        await self.channel_layer.group_send(
                prefixed_value,
                {
                    'type': 'reset.stable.id'
                }
        )


    async def send_game_scene(self, event):
        await self.send(text_data=json.dumps({
            'type': event['data']['response_type'],
            'new_pedal_pos': event['data']['new_pedal_pos']
        }))


    async def send_init_game(self, event):
        game_instance = await self.get_game_instance(self.stable_game_id)
        await self.send(text_data=json.dumps({
            'type': 'init_game',
            'alias_one': event['data']['alias_one'],
            'alias_two': event['data']['alias_two'],
            'is_host': event['data']['is_host'],
            'guest_id': game_instance.guestId,
            'host_id': game_instance.hostId,
            'num_id_one': event['data']['num_id_one'],
            'num_id_two': event['data']['num_id_two'],
            'str_id_one': event['data']['str_id_one'],
            'str_id_two': event['data']['str_id_two'],
            'is_tourn': event['data']['is_tourn'],
        }))

    async def send_game_start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_start',
        }))


    async def send_ball_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ball_update',
            'ball_x': event['data']['ball_x'],
            'ball_y': event['data']['ball_y'],
        }))


    async def send_score_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'host_score': event['data']['host_score'],
            'guest_score': event['data']['guest_score'],
        }))


    async def send_game_over(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_over',
            'game_id': event['data']['game_id'],
        }))
        
    async def send_opponent_disconnected(self, event):
        if self.stable_game_id not in self.game_states:
            return None
        if self.game_states.get(self.stable_game_id, {}).get('player_one') == event['data']['user_id']:
            self.game_states[self.stable_game_id]['player_one'] = None
        elif self.game_states.get(self.stable_game_id, {}).get('player_two') == event['data']['user_id']:
            self.game_states[self.stable_game_id]['player_two'] = None

        if (self.game_states.get(self.stable_game_id, {}).get('player_one') == None and self.game_states.get(self.stable_game_id, {}).get('player_two') == None):
            self.game_states[self.stable_game_id]['canceled'] = True
            self.game_states[self.stable_game_id]['game_active'] = False


    async def send_request_invites(self, event):
        await self.send(text_data=json.dumps({
            'type': 'recieve_invites',
            'matches': event['data'],
        }))

    async def send_request_tourns(self, event):
        if event['real_type'] == 'send_request_tourns':
            type = 'recieve_tourns'
        elif event['real_type'] == 'request_tourn_his':
            type = 'recieve_tourn_history'
        await self.send(text_data=json.dumps({
            'type': type,
            'matches': event['data'],
        }))

    async def send_stats(self, event):
        await self.send(text_data=json.dumps({
            'type': 'recieve_stats',
            'stats': event['data'],
        }))

    async def send_history(self, event):
        await self.send(text_data=json.dumps({
            'type': 'recieve_history',
            'history': event['data'],
        }))
    async def send_already_in_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'already_in_game',
        }))

    async def send_chatbot_trigger(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chatbot_trigger',
            'data': event['data'],
        }))

    async def reset_stable_id(self, event):
        await self.send(text_data=json.dumps({
            'type': 'reset_stable_id',
        }))

    async def handle_user_left_game(self):
        if self.game_states.get(self.stable_game_id, {})['player_one'] == self.user['user_id']:
            self.game_states[self.stable_game_id]['player_one'] = None
        elif self.game_states.get(self.stable_game_id, {})['player_two'] == self.user['user_id']:
            self.game_states[self.stable_game_id]['player_two'] = None
        if (self.game_states.get(self.stable_game_id, {})['player_one'] == None and self.game_states.get(self.stable_game_id, {})['player_two'] == None):
            self.game_states[self.stable_game_id]['canceled'] = True
            self.game_states[self.stable_game_id]['game_active'] = False
            tmp_id = self.game_states.get(self.stable_game_id, {}).get('group_id')
            prefixed_value = f"b_{tmp_id}"

            if self.game_states.get(self.stable_game_id, {}).get('game_loop_task') is None:
                await self.channel_layer.group_send(
                    prefixed_value,
                    {
                        'type': 'reset.stable.id'
                    }
                )
        
        await self.channel_layer.group_discard(self.game_group_id, self.channel_name)

    async def update_stable_game_id_for_group(self, group_id, new_value):
        users_in_group = await self.get_users_in_group(group_id)
        for conn in self.connections:
            if conn['user_id'] in [user['user_id'] for user in users_in_group]:
                conn['stable_game_id'] = new_value

    async def get_users_in_group(self, group_id):
        return [conn for conn in self.connections if conn['user_id'] in (channel['user_id'] for channel in self.channels if channel['channel_name'] == group_id)]


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
        await self.channel_layer.group_send(
            self.game_group_id,
            {
                'type': 'send.game.scene',
                'data': {
                    'new_pedal_pos': new_pedal_pos,
                    'response_type': response_type
                },
            }
        )
    async def handle_request_score(self):
        if self.stable_game_id != 0 and self.stable_game_id in self.game_states:
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'send.score.update',
                    'data': {
                        'host_score': self.game_states[self.stable_game_id]['host_score'],
                        'guest_score': self.game_states[self.stable_game_id]['guest_score'],
                    },
                }
            )


    async def clear_game_struct(self):
        self.game_states[self.stable_game_id] = {
            'left_pedal': 0.75,
            'right_pedal': 0.75,
            'ball_x': 2,  # Initial ball position
            'ball_y': 1,  # Initial ball position
            'ball_radius': 0.05,
            'ball_dx': 0.025,
            'ball_dy': 0.025,
            'joined_players': 0,
            'host_score': 0,
            'guest_score': 0,
            'score_limit': 3,
            'game_active': True,
            'player_one': None,
            'player_two': None,
            'previous_join': 0,
            'canceled': False,
            'game_loop_task': None,
        }


    async def init_game_struct(self):
        if self.stable_game_id not in self.game_states:
            self.game_states[self.stable_game_id] = {
                'left_pedal': 0.75,
                'right_pedal': 0.75,
                'ball_x': 2,  # Initial ball position
                'ball_y': 1,  # Initial ball position
                'ball_radius': 0.05,
                'ball_dx': 0.025,
                'ball_dy': 0.025,
                'joined_players': 0,
                'host_score': 0,
                'guest_score': 0,
                'score_limit': 3,
                'game_active': True,
                'player_one': None,
                'player_two': None,
                'previous_join': 0,
                'canceled': False,
                'game_loop_task': None,
                'group_id': self.game_group_id,
            }


    async def handle_send_init_game(self):
        if int(self.stable_game_id) == 0:
            self.stable_game_id = int(self.game_id)
        elif int(self.stable_game_id) != int(self.game_id):
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'send.already.in.game',
                })
            return None
        active_game = await self.check_active_games(self.stable_game_id)
        if active_game:
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'send.already.in.game',
                })
            return None
        if self.game_states.get(self.stable_game_id, {}):
            if self.game_states.get(self.stable_game_id, {}).get('player_one') == self.user['user_id'] or self.game_states.get(self.stable_game_id, {}).get('player_two') == self.user['user_id']:
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        'type': 'send.already.in.game',
                    })
                return None
            elif self.game_states.get(self.stable_game_id, {}).get('player_one') == None:
                self.game_states[self.stable_game_id]['player_one'] = self.user['user_id']
            elif self.game_states.get(self.stable_game_id, {}).get('player_two') == None:
                self.game_states[self.stable_game_id]['player_two'] = self.user['user_id']
        else:
            await self.init_game_struct()
            self.game_states.get(self.stable_game_id, {})['player_one'] = self.user['user_id']
        return_val = await self.get_host(self.stable_game_id, self.user['user_id'])
        data = await self.get_players_id(self.stable_game_id)
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send.init.game',
                'data': {
                    'is_host': return_val,
                    'joined_players': self.game_states.get(self.stable_game_id, {}).get('joined_players'),
                    'num_id_one': data[0]['num_id_one'],
                    'num_id_two': data[0]['num_id_two'],
                    'str_id_one': data[0]['str_id_one'],
                    'str_id_two': data[0]['str_id_two'],
                    'is_tourn': data[0]['is_tourn'],
                    'alias_one': data[0]['alias_one'],
                    'alias_two': data[0]['alias_two']
                },
            }
        )

        if (self.game_states.get(self.stable_game_id, {}).get('player_one') != None and self.game_states.get(self.stable_game_id, {}).get('player_two') != None):
            await self.channel_layer.group_send(
                self.game_group_id,
                {
                    'type': 'send.game.start',
                    'data': {
                        'ball_x': self.game_states.get(self.stable_game_id, {}).get('ball_x'),
                        'ball_y': self.game_states.get(self.stable_game_id, {}).get('ball_y')
                    },
                }
            )

            if self.game_states.get(self.stable_game_id, {}).get('game_loop_task') is None:
                self.game_states[self.stable_game_id]['game_loop_task'] = asyncio.create_task(self.game_loop())


    async def handle_send_ball_update(self):
        await self.calculate_ball_state()
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


    async def handle_send_score_update(self):
        try:
            await self.channel_layer.group_send(
                self.game_group_id,
                {
                    'type': 'send.score.update',
                    'data': {
                        'host_score': self.game_states[self.stable_game_id]['host_score'],
                        'guest_score': self.game_states[self.stable_game_id]['guest_score'],
                    },
                }
            )
        except Exception as e:
            print(f"Error in handle_send_score: {e}")

    async def handle_send_tourns(self, type):
        if type == 'send_request_tourns':
            prop = 'active'
        elif type == 'request_tourn_his':
            prop = 'finished'
        return_data = await self.get_tourns(self.user['user_id'], prop)
        await self.channel_layer.send(
        self.channel_name,
        {
            'type': 'send.request.tourns',
            'real_type': type,
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
        tourn_id = await self.add_to_tourn(self.user['user_id'], self.invited_id)
        if tourn_id:
            return_data = await self.semiFull(tourn_id)
            if return_data:
                await self.channel_layer.send(
                    self.channel_name,
                    {
                        'type': 'send.chatbot.trigger',
                        'data': return_data,
                    })

    async def handle_send_stats(self):
        return_data = await self.get_stats(self.user['user_id'])
        await self.channel_layer.send(
        self.channel_name,
        {
            'type': 'send.stats',
            'data': return_data,
        })

    async def handle_send_history(self):
        return_data = await self.get_history(self.user['user_id'])
        await self.channel_layer.send(
        self.channel_name,
        {
            'type': 'send.history',
            'data': return_data,
        })


    # ---------------------------- DATABASE FUNCTIONS ----------------------------
    
    
    @database_sync_to_async
    def check_active_games(self, stable_game_id):
        user_instance = MyUser.objects.get(user_id=self.user['user_id'])
        active_games = user_instance.new_matches.all()
        for game in active_games:
            if str(game.id) in self.game_states:
                if self.game_states.get(str(game.id), {}).get('player_one') == self.user['user_id'] or self.game_states.get(str(game.id), {}).get('player_two') == self.user['user_id']:
                    print("")
                elif self.game_states.get(str(game.id), {}).get('game_active') == True and str(game.id) != str(self.stable_game_id):
                    return True
        game_isinstance = Game.objects.get(id=stable_game_id)
        if game_isinstance.winnerId != None:
            return True
        return False


    @database_sync_to_async
    def set_technical_winner(self, game_id, user_id):
        game_instance = Game.objects.get(id=game_id)
        if game_instance.hostId == user_id:
            game_instance.winnerId = game_instance.guestId
            game_instance.loserId = game_instance.hostId
        else:
            game_instance.winnerId = game_instance.hostId
            game_instance.loserId = game_instance.guestId
        game_instance.save()

    
    @database_sync_to_async
    def get_players_id(self, game_id):
        game_instance = Game.objects.get(id=game_id)
        return_data = []
        if game_instance.hostId.isdigit():
            str_id_one = MyUser.objects.get(user_id=int(game_instance.hostId)).name
            str_id_two = MyUser.objects.get(user_id=int(game_instance.guestId)).name
            num_id_one = int(game_instance.hostId)
            num_id_two = int(game_instance.guestId)
            alias_one = MyUser.objects.get(user_id=int(game_instance.hostId)).alias
            alias_two = MyUser.objects.get(user_id=int(game_instance.guestId)).alias
            is_tourn = 'True'
        else:
            str_id_one = game_instance.hostId
            str_id_two = game_instance.guestId
            num_id_one = int(MyUser.objects.get(name=game_instance.hostId).user_id)
            num_id_two = int(MyUser.objects.get(name=game_instance.guestId).user_id)
            alias_one = None
            alias_two = None
            is_tourn = 'False'

        return_data.append({
            'num_id_one': num_id_one,
            'num_id_two': num_id_two,
            'str_id_one': str_id_one,
            'str_id_two': str_id_two,
            'is_tourn': is_tourn,
            'alias_one': alias_one,
            'alias_two': alias_two
        })
        return return_data

    @database_sync_to_async
    def get_history(self, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)
        before_reverse = user_instance.old_matches.all()
        game_sessions = before_reverse.order_by('-id')
        match_data = []
        for game_session in game_sessions:
            game_entry = []
            game_id = game_session.id
            if game_session.hostId.isdigit():
                winner_id = MyUser.objects.get(user_id=int(game_session.hostId)).name
                loser_id = MyUser.objects.get(user_id=int(game_session.guestId)).name
            else:
                winner_id = game_session.winnerId
                loser_id = game_session.loserId
            date = game_session.date.strftime("%Y-%m-%d %H:%M:%S")
            game_entry.append({
                'winner_id': winner_id,
                'loser_id': loser_id,
                'game_id': game_id,
                'date': date
            })
            match_data.append(game_entry)
        return match_data

    @database_sync_to_async
    def get_stats(self, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)
        won_games = user_instance.old_matches.filter(winnerId=user_instance.name).count()
        won_tourn_games = user_instance.old_matches.filter(winnerId=user_id).count()
        lost_games = user_instance.old_matches.filter(loserId=user_instance.name).count()
        lost_tourn_games = user_instance.old_matches.filter(loserId=user_id).count()
        total_games = won_games + lost_games + won_tourn_games + lost_tourn_games
        won_tourns = user_instance.tourns.filter(winnerId=user_instance.user_id).count()
        all_tourns = user_instance.tourns.filter(status='finished').count()
        return { 'won_games': won_games + won_tourn_games, 'lost_games': lost_games + lost_tourn_games, 'total_games': total_games, 'won_tourns': won_tourns, 'all_tourns': all_tourns }

    @database_sync_to_async
    def setWinner(self, game_struct):
        game_instance = Game.objects.get(id=self.stable_game_id)
        if game_struct['host_score'] == game_struct['score_limit']:
            game_instance.winnerId = game_instance.hostId
            game_instance.loserId = game_instance.guestId
        elif game_struct['guest_score'] == game_struct['score_limit']:
            game_instance.winnerId = game_instance.guestId
            game_instance.loserId = game_instance.hostId
        game_instance.date = timezone.localtime(timezone.now())
        game_instance.save()

    @database_sync_to_async
    def matchResults(self):
        game_instance = Game.objects.get(id=self.stable_game_id)
        if game_instance.hostId.isdigit():
            user_one = MyUser.objects.get(user_id=game_instance.hostId)
        else:
            user_one = MyUser.objects.get(name=game_instance.hostId)
        if game_instance.guestId.isdigit():
            user_two = MyUser.objects.get(user_id=game_instance.guestId)
        else:
            user_two = MyUser.objects.get(name=game_instance.guestId)
        user_one.old_matches.add(game_instance)
        user_two.old_matches.add(game_instance)
        user_one.new_matches.remove(game_instance)
        user_two.new_matches.remove(game_instance)
        user_one.save()
        user_two.save()

        if game_instance.tournId is not None:
            return_data = []
            tourn_instance = Tournament.objects.get(id=game_instance.tournId)
            tourn_instance.active_matches.remove(game_instance)
            tourn_instance.passed_matches.add(game_instance)
            tourn_instance.save()

            # return tourn_instance.id
            if game_instance.stage == "semi":
                tourn_instance.finalMatch.append(game_instance.winnerId)
            tourn_instance.save()
            if len(tourn_instance.finalMatch) == 2:
                if game_instance.stage == "semi":
                    new_game = Game.objects.create()
                    new_game.hostId = tourn_instance.finalMatch[0]
                    new_game.guestId = tourn_instance.finalMatch[1]
                    tourn_instance.active_matches.add(new_game)
                    new_game.tournId = tourn_instance.id
                    new_game.stage = "final"
                    new_game.save()

                    user_one = MyUser.objects.get(user_id=tourn_instance.finalMatch[0])
                    user_two = MyUser.objects.get(user_id=tourn_instance.finalMatch[1])
                    user_one.new_matches.add(new_game)
                    user_two.new_matches.add(new_game)
                    user_one.save()
                    user_two.save()
                    game_entry = {
                        'user_one_str': user_one.name,
                        'user_two_str': user_two.name,
                        'user_one_num': user_one.user_id,
                        'user_two_num': user_two.user_id,
                        'user_one_alias': user_one.alias,
                        'user_two_alias': user_two.alias,
                        'game_id': new_game.id,
                        'tourn_instance_id': tourn_instance.id
                    }
                    tourn_instance.save()
                    return_data.append(game_entry)
                    return return_data
                else:
                    tourn_instance.winnerId = game_instance.winnerId
                    tourn_instance.status = "finished"
                    tourn_instance.save()

    @database_sync_to_async
    def semiFull(self, invited_id):
        return_data = []
        tourn_instance = Tournament.objects.get(id=invited_id)
        if len(tourn_instance.semiMatch) == 4:
            semi_match = tourn_instance.semiMatch
            random.shuffle(semi_match)
            tourn_instance.semiMatch = semi_match
            tourn_instance.save()

            for i in range(0, 4, 2):
                game_instance = Game.objects.create()
                game_instance.hostId = tourn_instance.semiMatch[i]
                game_instance.guestId = tourn_instance.semiMatch[i + 1]
                tourn_instance.active_matches.add(game_instance)
                game_instance.tournId = tourn_instance.id
                game_instance.stage = "semi"
                game_instance.save()

                user_one = MyUser.objects.get(user_id=tourn_instance.semiMatch[i])
                user_two = MyUser.objects.get(user_id=tourn_instance.semiMatch[i + 1])
                user_one.new_matches.add(game_instance)
                user_two.new_matches.add(game_instance)
                user_one.save()
                user_two.save()
                game_entry = {
                    'user_one_str': user_one.name,
                    'user_two_str': user_two.name,
                    'user_one_num': user_one.user_id,
                    'user_two_num': user_two.user_id,
                    'user_one_alias': user_one.alias,
                    'user_two_alias': user_two.alias,
                    'game_id': game_instance.id,
                    'tourn_instance_id': tourn_instance.id
                }
                return_data.append(game_entry)

            tourn_instance.save()
            return return_data

    @database_sync_to_async
    def add_to_tourn(self, user_id, invited_id):
        host_instance = MyUser.objects.get(user_id=user_id)
        invited_instance = MyUser.objects.get(name=invited_id)
        tourn_sessions = host_instance.tourns.all()
        exists = False
        if len(tourn_sessions) != 0:
            for tourn_session in tourn_sessions:
                if tourn_session.hostId == user_id and tourn_session.status == "active":
                    already_inv = False
                    if len(tourn_session.semiMatch) < 4:
                        for id in tourn_session.semiMatch:
                            if int(id) == invited_instance.user_id:
                                already_inv = True
                                break
                        if already_inv == False:
                            tourn_session.semiMatch.append(invited_instance.user_id)
                            invited_instance.tourns.add(tourn_session)
                            tourn_session.save()
                            if len(tourn_session.semiMatch) == 4:
                                return tourn_session.id
                    exists = True
        if not exists:
            tourn_instance = Tournament.objects.create()
            tourn_instance.semiMatch.append(user_id)
            tourn_instance.semiMatch.append(invited_instance.user_id)
            host_instance.tourns.add(tourn_instance)
            host_instance.save()
            invited_instance.tourns.add(tourn_instance)
            invited_instance.save()
            tourn_instance.hostId = user_id
            tourn_instance.save()


    @database_sync_to_async
    def get_host(self, game_id, user_id):
        game_instance = Game.objects.get(id=game_id)
        if game_instance.hostId.isdigit():
            to_compare = MyUser.objects.get(user_id=int(game_instance.hostId)).name
        else:
            to_compare = game_instance.hostId
        user_instance = MyUser.objects.get(user_id=user_id)
        if user_instance.name == to_compare:
            self.is_host = True
            check_host = 'True'
        else:
            self.is_host = False
            check_host = 'False'
        return check_host

    @database_sync_to_async
    def get_tourns(self, user_id, prop):
        user_instance = MyUser.objects.get(user_id=user_id)  # changed id to user_id
        tourn_instances = user_instance.tourns.filter(status=prop)

        match_data = []
        for tourns in tourn_instances:
            active_sessions = tourns.active_matches.all()
            passed_sessions = tourns.passed_matches.all()
            unsorted_game_sessions = active_sessions.union(passed_sessions)
            game_sessions = sorted(unsorted_game_sessions, key=lambda session: session.id)
            unit = []
            tourn_entry = []
            tourn_host = MyUser.objects.get(user_id=int(tourns.hostId)).alias
            if tourns.winnerId is not None:
                tourn_winner = MyUser.objects.get(user_id=int(tourns.winnerId)).alias
            else:
                tourn_winner = None
            tourn_id = tourns.id

            tourn_entry.append({
                'tourn_host': tourn_host,
                'tourn_winner': tourn_winner,
                'tourn_id': tourn_id
            })
            unit.append(tourn_entry)
            i = 0
            for game_session in game_sessions:
                game_entry = []
                player_one = game_session.hostId
                player_two = game_session.guestId
                game_id = game_session.id
                winner_id = game_session.winnerId
                loser_id = game_session.loserId
                stage = game_session.stage
                alias_one = MyUser.objects.get(user_id=player_one).alias
                alias_two = MyUser.objects.get(user_id=player_two).alias
                if stage == 'semi':
                    i = i + 1
                
                # Append data to the match_data list
                game_entry.append({
                    'player_one': player_one,
                    'player_two': player_two,
                    'game_id': game_id,
                    'winner_id': winner_id,
                    'loser_id': loser_id,
                    'stage': stage,
                    'alias_one': alias_one,
                    'alias_two': alias_two,
                    'counter_semi': i
                })
                unit.append(game_entry)
            match_data.append(unit)

        json_data = json.dumps(match_data)
        return json_data

    @database_sync_to_async
    def get_matches(self, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)  # changed id to user_id
        game_sessions = user_instance.new_matches.exclude(tournId__isnull=False)
        match_data = []

        # Iterate through game_sessions
        for game_session in game_sessions:
            # Extract opponent name and game id
            print(game_session.hostId)
            if type(game_session.hostId) == str:
                if game_session.hostId.isdigit():
                    host = int(game_session.hostId)
                else:
                    host = MyUser.objects.get(name=game_session.hostId).user_id
            else:
                host = game_session.hostId
            if type(game_session.guestId) == str:
                if game_session.guestId.isdigit():
                    guest = int(game_session.guestId)
                else:
                    guest = MyUser.objects.get(name=game_session.guestId).user_id
            else:
                guest = game_session.guestId
            if type(user_instance.user_id) == str:
                if user_instance.user_id.isdigit():
                    user_id = int(user_instance.user_id)
                else:
                    user_id = MyUser.objects.get(name=user_instance.name).user_id
            else:
                user_id = user_instance.user_id
            if int(user_id) == int(host):
                opponent = guest
            else:
                opponent = host
            game_id = game_session.id
            opponent_name = MyUser.objects.get(user_id=opponent)

            # Append data to the match_data list
            match_data.append({
                'opponent_name': opponent_name.name,
                'game_id': game_id
            })
        json_data = json.dumps(match_data)
        return json_data


    @database_sync_to_async
    def remove_ended_match(self, user_id, game_id):
        try:
            game_instance = Game.objects.get(id=game_id)
            user1 = MyUser.objects.get(name=game_instance.hostId)  # changed id to user_id
            user1.new_matches.remove(game_instance)
            user1.old_matches.add(game_instance)
            user1.save()
            user2 = MyUser.objects.get(name=game_instance.guestId)
            user2.new_matches.remove(game_instance)
            user2.old_matches.add(game_instance)
            user2.save()
        except MyUser.DoesNotExist:
            return None

    @database_sync_to_async
    def get_game_instance(self, game_id):
        try:
            game_instance = Game.objects.get(id=game_id)
            return game_instance
        except Game.DoesNotExist:
            return None