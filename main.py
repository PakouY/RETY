# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
  # This function runs every in-game tick (every time the game updates anything)
  def run(self):
    if self.intent is not None:
      return

    # d1 = abs(self.ball.location.y - self.foe_goal.location.y)
    # d2 = abs(self.me.location.y - self.foe_goal.location.y)
    # is_in_front_of_ball = d1 > d2
    # # if we're in front of the ball, retreat
    # if is_in_front_of_ball:
    #     self.set_intent(goto(self.friend_goal.location))
    #     return


    if self.kickoff_flag:
      self.set_intent(self.kickoff())
      return
    if self.is_in_front_of_ball():
      retreat_location = self.friend_goal.location
      self.set_intent(goto(retreat_location))
      return

    if self.me.boost > 99:
      shot_location = self.foe_goal.location
      self.set_intent(short_shot(shot_location))
      return

    closest_boost = self.get_closest_large_boost()
    if closest_boost is not None:
      boost_location = closest_boost.location
      self.set_intent(goto(closest_boost.location))
      return


