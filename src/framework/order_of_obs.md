last iteration i.e. t0:
all instances updated to s0
and sent e0 to others
(1)if do observate at t0,
get observation at t1 with obs0
  obs event sent at t0
  environment handles this event
  (event must be handled by environment)
  environment send message to observed instances, (t0)
  instances return corresponding features(t0)
  environment get returning features and fill into obs buffer
  and character get the result at t1 before updating
  character and observed object update at same time
(2) if do observate at t0
get obs at t2 with obs1
send obs event at t0
  env -> message -> observed, but not to return anything
  observed update at t1 and send obs1 back
  get obs1 at t2
i.e.
  t0 update : observer send message to obs (b)
              observed return obs-1 (a)
  t1 update : observer update with obs -1 (a)
              observed update
              observer send message
              observed send message, observed return with obs 0 (b)
each instance update with (update, send message)
