"""
UNIT 1: Bowling:

You will write the function bowling(balls), which returns an integer indicating
the score of a ten-pin bowling game.  balls is a list of integers indicating
how many pins are knocked down with each ball.  For example, a perfect game of
bowling would be described with:

    >>> bowling([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    300

The rules of bowling are as follows:

(1) A game consists of 10 frames. In each frame you roll one or two balls,
except for the tenth frame, where you roll one, two, or three.  Your total
score is the sum of your scores for the ten frames.
(2) If you knock down fewer than ten pins with your two balls in the frame,
you score the total knocked down.  For example, bowling([8, 1, 7, ...]) means
that you knocked down a total of 9 pins in the first frame.  You score 9 point
for the frame, and you used up two balls in the frame. The second frame will
start with the 7.
(3) If you knock down all ten pins on your second ball it is called a 'spare'
and you score 10 points plus a bonus: whatever you roll with your next ball.
The next ball will also count in the next frame, so the next ball counts twice
(except in the tenth frame, in which case the bonus ball counts only once).
For example, bowling([8, 2, 7, ...]) means you get a spare in the first frame.
You score 10 + 7 for the frame; the second frame starts with the 7.
(4) If you knock down all ten pins on your first ball it is called a 'strike'
and you score 10 points plus a bonus of your score on the next two balls.
(The next two balls also count in the next frame, except in the tenth frame.)
For example, bowling([10, 7, 3, ...]) means that you get a strike, you score
10 + 7 + 3 = 20 in the first frame; the second frame starts with the 7.
"""


def scoreboard(c, frame, board):

    if frame == 10: return board

    if frame == 9:
        if c[0] + c[1] >= 10:
            board[frame] = [c[0],c[1],c[2]]
        else:
            board[frame] = [c[0],c[1]]
    else:
        if balls[0] == 10:
            board[frame] = [10,0]
            balls.pop(0)

        elif balls[0] + balls[1] == 10:
            board[frame] = [balls[0],balls[1]]
            balls.pop(0)
            balls.pop(0)

        elif balls[0] + balls[1] < 10:
            board[frame] = [balls[0],balls[1]]
            balls.pop(0)
            balls.pop(0)

    return scoreboard(balls, frame+1, board)


def framescore(board, frame):
    score = 0
    if frame < 9:
        if board[frame][0] == 10: 
            if board[frame+1][0] == 10:
                if frame == 8:
                    return 20 + board[9][1]
                else:
                    return 20 + board[frame+2][0]
            else:
                if frame == 8:
                    return 10 + board[9][0] + board[9][1]
                else:
                    return 10 + sum(board[frame+1])
        elif sum(board[frame]) == 10:
            return 10 + board[frame+1][0]
        else:
            return sum(board[frame])
    else:
        return sum(board[9])


def score(board):
    s = 0
    for frame in xrange(10):
        s += framescore(board, frame)
    return s 

balls = []

def bowling(b):
    "Compute the total score for a player's game of bowling."
    board = {}
    global balls
    balls = b
    s = scoreboard(balls, 0, board)
    return score(s)


def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    print "tests pass"

test_bowling()

