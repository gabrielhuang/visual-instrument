#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.mixer import Sound

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900

# draw rectangles
# https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/


def init_pygame():
    pygame.mixer.pre_init(44100, -16, 2, 512)  # smaller buffer
    #pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return screen



def get_mappings():
    sounds = {
       'kick':  Sound("samples/Bass-Drum-1.wav"),
       'snare':  Sound("samples/Snare 16.wav"),
       'drumloop':  Sound("samples/drum-loop-paper-bird-ricardo-espino.wav"),
       'guitar_e': Sound('samples/130625_130657-[2].wav'),
       'guitar_am': Sound('samples/130625_131130-[6].wav'),
       'guitar_c7': Sound('samples/130625_131722-[4].wav'),
       'guitar_d': Sound('samples/130625_132027-[5].wav'),
       'hat': Sound('samples/Hat 6.wav')
    }
    mappings = {
        pygame.K_k: 'kick',
        pygame.K_s: 'snare',
        pygame.K_a: 'hat',
        pygame.K_d: 'drumloop',
        pygame.K_1: 'guitar_e',
        pygame.K_2: 'guitar_am',
        pygame.K_3: 'guitar_c7',
        pygame.K_4: 'guitar_d',
    }
    return sounds, mappings

def get_mappings_house():
    sounds = {
       'kick':  (Sound("samples/house-Kick.wav"), 0),
       'snare':  (Sound("samples/Snare 16.wav"), 0),
       'drumloop_1':  (Sound("samples/House_Kit_01-Full_Drums-125-E.wav"), 1),
       'drumloop_2':  (Sound("samples/House_Kit_01-Kickless_Drums-125-E.wav"), 1),
       'bass_e': (Sound('samples/Bass E.wav'), 0),
       'bass_f': (Sound('samples/Bass F.wav'), 0),
       'chord_c': (Sound('samples/house-Chord C.wav'), 0),
       'chord_g': (Sound('samples/house-Chord G.wav'), 0),
       'hat': (Sound('samples/Hat 6.wav'), 0)
    }
    mappings = {
        pygame.K_k: 'kick',
        pygame.K_s: 'snare',
        pygame.K_a: 'hat',
        pygame.K_d: 'drumloop_1',
        pygame.K_f: 'drumloop_2',
        pygame.K_1: 'bass_e',
        pygame.K_2: 'bass_f',
        pygame.K_3: 'chord_c',
        pygame.K_4: 'chord_g',
    }
    return sounds, mappings



def verify_sounds_and_mappings(sounds, mappings):
    for key, name in mappings.items():
        assert name in sounds, '{} (key {}) not in sounds'.format(name, key)


def float_to_rgb(x, darken=1.):
    r,g,b,a = plt.cm.jet(x, bytes=True)
    if darken != 1.:
        darken = np.clip(darken, 0, 1)
        r = int(darken*r)
        g = int(darken*g)
        b = int(darken*b)
    return (r,g,b)

    
screen = init_pygame()
#sounds, mappings = get_mappings()
sounds, mappings = get_mappings_house()
verify_sounds_and_mappings(sounds, mappings)
sounds_idx = {name: idx for idx, name in enumerate(sounds)}
sounds_colors = {name: float_to_rgb(float(idx)/len(sounds_idx)) for name, idx in sounds_idx.items()}

music_events = []
FLIGHT_TIME = 3.  # seconds
FPS = 30.
REFRESH_TIME = 1. / FPS
TOLERANCE = 1.5
BLOCK_WIDTH = SCREEN_WIDTH / max(1, len(sounds))
BLOCK_HEIGHT = SCREEN_HEIGHT / 50
CURRENT_KEY_LAG = 0.3
TIGHTEST_SLEEP = 0.001

last_refresh = None
while True:
    # afford tiny sleep
    time.sleep(TIGHTEST_SLEEP)    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            # Go through mappings
            if event.key in mappings:
                name = mappings[event.key]
                sound, loop = sounds[name]
                print 'Playing', name
                sound.play(loops=-1 if loop else 0)
                music_events.append({
                    'time': time.time(),
                    'name': name
                })

                #print music_events
            elif event.key == pygame.K_SPACE:
                pygame.mixer.stop()
                music_events = []  # clear music events
                print 'Clear sounds'
            else:
                print 'Unrecognized key {}'.format(event.key)
                continue
    # pretty print
    now = time.time()
    if last_refresh is None or now - last_refresh > REFRESH_TIME:
        screen.fill((0,0,0))  # clear screen
        last_refresh = now
        pygame.display.update()
        # remove all events older than FLIGHT_TIME*TOLERANCE
        idx = 0
        new_events = []
        for idx, m_event in enumerate(music_events):
            name = m_event['name']
            loop = sounds[name][1]
            if now - m_event['time'] <= TOLERANCE * FLIGHT_TIME or loop:
                new_events.append(m_event)
        music_events = new_events
        # draw events
        for m_event in music_events:
            # x position is instrument
            name = m_event['name']
            x = sounds_idx[name] * BLOCK_WIDTH
            # y position proportional to time elapsed
            dt = now-m_event['time']
            y = int(dt * SCREEN_HEIGHT / float(FLIGHT_TIME))
            # color
            color_indicator = sounds_idx[name] / float(len(sounds_idx))
            # draw falling rectangle
            # if loop just fill whole screen
            loop = sounds[name][1]
            if loop:
                dt_indicator = 0.5+0.25*(1+np.sin(3*now))
                color = float_to_rgb(sounds_idx[name] / float(len(sounds_idx)), dt_indicator)
                pygame.draw.rect(screen, color, (x, 0, BLOCK_WIDTH, SCREEN_HEIGHT), 0)
            else:
                dt_indicator = np.clip((1-dt/FLIGHT_TIME)**2., 0, 1)
                color = float_to_rgb(sounds_idx[name] / float(len(sounds_idx)), dt_indicator)
                pygame.draw.rect(screen, color, (x, y, BLOCK_WIDTH, BLOCK_HEIGHT), 0)
            # also draw current instrument
            if dt < CURRENT_KEY_LAG:
                pygame.draw.rect(screen, color, (x, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 0)
        # update
        pygame.display.update()
