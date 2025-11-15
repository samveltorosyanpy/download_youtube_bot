import sox
from pydub import AudioSegment


class Effector:

    @staticmethod
    def add_effects(input_path, final_path, reverberance=0, bass=0, pitch=0, speed=1):
        audio_transformer = sox.Transformer()
        audio_transformer.reverb(reverberance=int(reverberance))
        audio_transformer.bass(gain_db=int(bass))
        audio_transformer.pitch(n_semitones=int(pitch))
        audio_transformer.speed(factor=float(speed))

        audio_transformer.build(input_path, final_path)
        return final_path

    @staticmethod
    def pan_rotation(input_path, final_path, speed, output_format='mp3'):
        audio_file = AudioSegment.from_mp3(input_path)
        audio_start = audio_file[0]

        panning = 0
        panning_gain = 0.05

        for i in range(0, len(audio_file) - int(speed), int(speed)):
            if panning >= 0.89:
                panning_gain = -0.05
            elif panning <= -0.89:
                panning_gain = 0.05

            peice = audio_file[i:i + speed]
            panned = peice.pan(panning)
            audio_start = audio_start + panned

            panning += panning_gain

        audio_start.export(final_path, format=output_format)


