# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
  # This function runs every in-game tick (every time the game updates anything)
  def run(self):
    # self.print_debug()
    if self.intent is not None:
      # self.debug_intent()
      return
      # Check if the ball is close enough to dribble
    if self.is_ball_nearby_for_dribble():
        # Dribble the ball towards the opponent's goal
        self.dribble_towards_goal()
    else:
        # Go to the ball to get into a dribbling position
        self.set_intent(goto(self.ball.location))

    d1 = abs(self.ball.location.y - self.foe_goal.location.y)
    d2 = abs(self.me.location.y - self.foe_goal.location.y)
    is_in_front_of_ball = d1 > d2
    # if we're in front of the ball, retreat
    if is_in_front_of_ball:
        self.set_intent(goto(self.friend_goal.location))
        return


    if self.kickoff_flag:
      # self.clear_debug_lines()
      self.set_intent(self.kickoff())
      # self.add_debug_line('me_to_kickoff', self.me.location, self.ball.location, [0, 0, 255])
      # self.add_debug_line('kickoff_to_goal', self.ball.location, self.foe_goal.location, [0, 0, 255])
      return
    # self.clear_debug_lines()
    if self.is_in_front_of_ball():
      retreat_location = self.friend_goal.location
      self.set_intent(goto(retreat_location))
      # self.debug_text = 'retreating'
      # self.add_debug_line('retreating', self.me.location, retreat_location, [255, 0, 0])
      return

    if self.me.boost > 99:
      shot_location = self.foe_goal.location
      self.set_intent(short_shot(shot_location))
      # self.debug_text = 'shooting'
      # self.add_debug_line('me_to_ball', self.me.location, self.ball.location, [0, 0, 255])
      # self.add_debug_line('ball_to_net', self.ball.location, shot_location, [0, 0, 255])
      return

    closest_boost = self.get_closest_large_boost()
    if closest_boost is not None:
      boost_location = closest_boost.location
      self.set_intent(goto(closest_boost.location))
      # self.debug_text = 'getting boost'
      # self.add_debug_line('getting boost', self.me.location, boost_location, [0, 255, 0])     
      return




    def is_ball_nearby_for_dribble(self):
        # Implement your condition to check if the ball is close enough for dribbling
        # For example, check if the ball is within a certain distance from the car
        return self.me.location.distance(self.ball.location) < dribble_distance_threshold

    def dribble_towards_goal(self):
        # Calculate the direction from the ball to the opponent's goal
        goal_direction = self.foe_goal.location - self.ball.location
        goal_direction = goal_direction.normalize()

        # Calculate the target position to dribble towards (in front of the ball)
        dribble_target = self.ball.location + (goal_direction * dribble_distance)

        # Set the intent to go to the dribble target
        self.set_intent(goto(dribble_target))

        # Keep the ball close to the car
        ball_local = self.ball.location - self.me.location
        ball_local = self.me.orientation.dot(ball_local)
        self.controller.steer = ball_local.x * dribble_steer_gain

        # Use the handbrake to keep the ball on top of the car
        self.controller.handbrake = True

        # Apply throttle to move towards the dribble target
        self.controller.throttle = 1.0

        # Optional: Control other car inputs like boost, jump, etc., based on your dribbling strategy

        # Optional: Use the renderer to draw debug lines to visualize the dribbling path

# Constants for dribbling behavior
dribble_distance_threshold = 300
dribble_distance = 50
dribble_steer_gain = 1.0
