#!/usr/bin/env python3
"""Remet les quatre fichiers du live dans leur etat de depart (avant une repetition,
et le jour J). Les versions completes *_complet.py ne sont pas touchees."""
import os, shutil
ICI = os.path.dirname(os.path.abspath(__file__))
for nom in ('ouverture', 'live1', 'live2', 'live3'):
    shutil.copy(os.path.join(ICI, 'trames', f'{nom}.py'), os.path.join(ICI, f'{nom}.py'))
    print(f'  live/{nom}.py remis a zero')
