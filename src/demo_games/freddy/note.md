
for door, the problem is,
that the door is considered as open during movement
but it uses power (solved)

for office :
self.left\_door\_event = ...
if pressed door button when left\_door\_event is opening
end it as unfinished
and create a new one : closing

calculate power :
if closed in state vector: as closed
for character: open if closing / opening
or open in state vector
the last two dim of vector as left opening / right opening
for door duration event:

for office obs:
	whether send to character
	depends on whether door open

for office update on action

    # TODO: the order of turning on monitor and sending
                 observation event
                 may be we should let office to do this
                 office knows whether each camera is on or off
                
                 if player action in obs_list, door up/close, monitor up/close
                 or light off event
                 or power used up
                 FIXME
                 TODO: if press monitor button, switch current view and
                 current obs, if current door open, send to hall

