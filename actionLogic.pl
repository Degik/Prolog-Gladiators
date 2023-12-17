:- dynamic apple/2.
:- dynamic agent/2.

action(move_north) :- agent(X,_), apple(X2,_), X > X2.
action(move_south) :- agent(X,_), apple(X2,_), X < X2.
action(move_est) :- agent(_,Y), apple(_, Y2), Y < Y2.
action(move_ovest) :- agent(_,Y), apple(_, Y2), Y > Y2.

action(take) :- agent(X,Y), apple(X,Y).
