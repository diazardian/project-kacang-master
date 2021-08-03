from gtts import gTTS

data = 'halo, saya adalah asisten virtual dari server kacang'
tts = gTTS(f'{data}', lang='id')
tts.save(f'audio/{data}.mp3')