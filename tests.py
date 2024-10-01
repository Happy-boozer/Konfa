
from commands import echo
def test_echo():
    result = echo("kl", "rt")
    result == ["kl","rt"]
    result = echo(1, 2, 10)
    result == [1, 2, 10]
    result = echo(1, "love", (3, 2, 1))
    result == [1, "love", (3, 2, 1)]

test_echo()
print("OK")
