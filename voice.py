from maix import audio, time, app

p = audio.Player("/root/red.wav")
p.volume(80)
p.play()

while not app.need_exit():
    time.sleep_ms(10)
print("play finish!")
