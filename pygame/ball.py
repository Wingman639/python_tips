import cStringIO, base64
import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        ball_file = cStringIO.StringIO(base64.decodestring(
"""iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ
bWFnZVJlYWR5ccllPAAABBJJREFUeNqsVj2PG1UUvfPp8XictXfHa+9mlyJCNEQRWiToqACJAgGC
LqJNlQZR0IFEj8RPSJkGGooUpEWJkGhR0tAAElI2tsfjjxnPjIdz7oyDF2wSUK72yN43793z7rkf
Y8N2HFmbbVliGIYiyzIpy1Isy3oHeMswzLOyXJ2tVit9VhTFAxz5Cfge+A7IZIcZmySObQudwIE0
veanraB1w/O8l5x6D9eXy6UkSaJYLBa6BvsNuAV8uY3sCQlvX4LANM0Xw/Dgdhj2Xm02m+K6LqPR
PXmeS5qmMp/PZTabyXQ6lclkosS1/QJcB+5vkthrAkoAuc4uHx//0B8MvCAIxG/5jEg0kpIkmcwX
icTxBIhlHWEURXoedgW4B3wIfHuBJM9yMQ3j5PTk5N7g6MjtdrrS3e9Ku90GUUvc2hkdMYJx5Ivn
NRC19UReRlRLR/sGeB34UUkMJBcJlcHg6K4SdDvS7/el1+tJp7MnQdCWRqMhDGWZLmWCCFog9rBm
GBYc50rOKON4uqkSC+IQSC3moeX7N09PX/i4AwLkAoQDxeFhHziU8CCUzt6e+EFLc2QaJi4mFQHy
kQLZMpME+WJF1sabdYA7Nq4jQbv9OZPs+75cgkSMYH9/X6PhJ9dpTLjruFLkBRyjACBd1BoLzzY8
T3O0IRntJvCZDXsTTnq262CzrzmgRHu4+QEIQhAxNzRWU1mTxfjOwvBIAOlIYNnWtja5bqM33mN/
sBEdx9bNPOQ1PWlqZJdAFKoMrEI6R+9gj6t7cUl1zjKnjFvsfaybr1Uqlv94ypXSKCud+aefpezs
7O3LL9s4c5U65gCrhGDDpUkqyWIuU1STweNlJRe7nAlmA+ZaVbnmiD4KFNEWC+3VqjB5YImDdMA+
YKONx2OVgxefojRL8CzmCxkOhxLhWYy+mGIvz6RKmv096X91PErP4Byazapbs3vZB45bVQqTzBzQ
kjQBQSTnjx7JcDTCRSLkKNY9SbKACsttHKZdrIqHILnGCNhoDU0qG83U5mNUVTOKShRPYo3m8fAc
nT/S/3mWFy2KrXKNOFbuI+Rr1FvLsB731Ho2m2pU7I1Sx8pSHTLaESIZjob6nfso2w77mSR3IMsN
zh4mmLOIBAkO6fjAgESdV1MYiV4kiUZHRDjD3E0Qza580D+rjsUdAQEj4fRl8wUkqBttPeo5RlJI
uB71jIASc8D+i4W8IoX8CviC5cuI+JlgpLsgcF1ng6RQyaoX1oWX1i67DTxe9w+9/EHW9VOrngCW
ZfNFpmvVWOfUzZ/mfG0HwHBz4ZV1kz8nvLuL+YPnRPDJ00J8A/j9fzrnW+sjeUbjbP8amDyj86z+
tXL5PwzOC4njj4K3gavA8cazczYacLd+p/+6y8mfAgwAsRuLfp/zVLMAAAAASUVORK5CYII="""))
        self.image = pygame.image.load(ball_file, 'file').convert_alpha()
        self.rect = self.image.fill(color, None, BLEND_ADD)
        self.rect.topleft = initial_position

pygame.init()
screen = pygame.display.set_mode([350, 350])

ball = Ball((255, 0, 0), (100, 100))
screen.blit(ball.image, ball.rect)
pygame.display.update()
while pygame.event.poll().type != KEYDOWN:
    pygame.time.delay(10)