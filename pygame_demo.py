#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import pygame
from pygame.mixer import Sound

def init_pygame():
    pygame.mixer.pre_init(44100, -16, 2, 512)  # smaller buffer
    #pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
    pygame.init()
    pygame.display.set_mode()


def get_mappings():
    sounds = {
       'kick':  Sound("samples/Bass-Drum-1.wav"),
       'snare':  Sound("samples/Snare 16.wav"),
       'drumloop':  Sound("samples/drum-loop-paper-bird-ricardo-espino.wav"),
       'guitar_e': Sound('samples/130625_130657-[2].wav'),
       'guitar_am': Sound('samples/130625_131130-[6].wav'),
       'guitar_c7': Sound('samples/130625_131722-[4].wav'),
       'guitar_d': Sound('samples/130625_132027-[5].wav')
    }
    mappings = {
        pygame.K_k: 'kick',
        pygame.K_s: 'snare',
        pygame.K_d: 'drumloop',
        pygame.K_1: 'guitar_e',
        pygame.K_2: 'guitar_am',
        pygame.K_3: 'guitar_c7',
        pygame.K_4: 'guitar_d',
    }
    return sounds, mappings


def verify_sounds_and_mappings(sounds, mappings):
    for key, name in mappings.items():
        assert name in sounds, '{} (key {}) not in sounds'.format(name, key)

    
init_pygame()
sounds, mappings = get_mappings()
verify_sounds_and_mappings(sounds, mappings)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            # Go through mappings
            if event.key in mappings:
                name = mappings[event.key]
                sound = sounds[name]
                print 'Playing', name
                sound.play()
            elif event.key == pygame.K_SPACE:
                pygame.mixer.stop()
                print 'Clear sounds'
            else:
                print 'Unrecognized key {}'.format(event.key)
                continue
