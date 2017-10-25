import smwc_hack_play
import smwc_music_preview
import smwc_sram_play

ALL_TYPES = ('music', 'smwhack', 'yihack', 'sram')
NEEDS_SECONDARY_ID = ('sram',)

def do_stuff(data):
    if data['type'] == 'music':
        smwc_music_preview.play_id(data['id'])
    elif data['type'] == 'smwhack':
        smwc_hack_play.play_id(data['id'], False)
    elif data['type'] == 'yihack':
        smwc_hack_play.play_id(data['id'], True)
    elif data['type'] == 'sram':
        smwc_sram_play.play_id(data['id'], data['secondary_id'])
