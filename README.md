# pagerduty-auto-ack

Sometimes in life you can not acknowledge an incident manually, but you also can't respond to it.
These are (and should be when you are on-call) usually short moments, usually taking about 15-20 minutes.
A good example here is taking a bath.

This script monitors the incidents that are assigned to you and acks them if needed.
At the end of execution (when stopped with C^c) it displays the incidents that it acknowledged.

## How to run it

Fast and easy way is to use `pipx`:

```
pipx pagerduty-auto-ack
```
