player : set monitor up (press button)
office : get event, trigger monitor up event
env: print("monitor up..") # hint event, like door opening
monitor up ends -> [
	select cam event, and return obs to player
	set office state
	for office: hook "set state" to event
	hint event: monitor up:done
]


if monitor down when setting monitor up:
	end monitor up with "not finitshed"
	# end video play
	# for all events, let it send "end" to audio server
	start a new event : monitor down

same for "door up/down"

monitor up/down event:
	.to_end(finitshed=True/False)
	.end() -> branch

hooks:
for those who starts an event
	let them know the event ends
	for example,
		open door/ monitor for office
		kill player for env (if it ends, set game = end)
		light on (light on for office when it starts, and off when it ends)
	each event hook video play

the event manager has default event factory
but let it hook another event factory provided by interface:
	hook audio start and end 


