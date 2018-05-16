"""
Music structure
"""
from time import sleep
from typing import List
from pydub import AudioSegment
import pyaudio
# from pyaudio import Stream
import threading
from pydub.utils import get_player_name, make_chunks


class MUSIC:
    POSITION = 0
    KILLERS = []
    AUDIO = pyaudio.PyAudio()
    BITE_SIZE_MS = 1
    _REQUESTED_VOICES = 0
    SECTION = 0

    @staticmethod
    def kill():
        # print("Stoppers: ", MUSIC.KILLERS)
        all_killers = MUSIC.KILLERS.copy()
        for stop in all_killers:
            MUSIC.KILLERS.remove(stop)
            stop()

    @staticmethod
    def position():
        return MUSIC.POSITION

    @staticmethod
    def can_play():
        return True if MUSIC._REQUESTED_VOICES and MUSIC._REQUESTED_VOICES > 0 else False

    @staticmethod
    def set_voices(value):
        """Bottom off at 0"""
        if value < 0:
            return
        MUSIC._REQUESTED_VOICES = value

    @staticmethod
    def lower_voices():
        MUSIC.set_voices(MUSIC._REQUESTED_VOICES - 1)

    @staticmethod
    def raise_voices():
        MUSIC.set_voices(MUSIC._REQUESTED_VOICES + 1)

    @staticmethod
    def get_voices():
        return MUSIC._REQUESTED_VOICES


class Player(threading.Thread):
    PLAYER = get_player_name()

    def __init__(self, clip: AudioSegment, start_pos: int, loop_time: int, callback: classmethod):
        # print({
        #     "clip length (ms)": len(clip),
        #     "start pos (ms)": start_pos,
        #     "loop time (ms)": loop_time,
        #     "result play length (ms)": len(clip[start_pos:])
        # })
        self.clip = clip[start_pos:]
        self.stream = None
        """:type : Stream"""

        self.local_pos = start_pos
        self.loop_time = loop_time

        self.playing = False
        self.time_callback = callback

        super().__init__(target=self.play)

    def __play_with_pyaudio(self, seg: AudioSegment):
        self.stream = MUSIC.AUDIO.open(
            format=MUSIC.AUDIO.get_format_from_width(seg.sample_width),
            channels=seg.channels,
            rate=seg.frame_rate,
            output=True
        )
        self.playing = True
        # PLAYBACK LOOP
        for chunk in make_chunks(seg, MUSIC.BITE_SIZE_MS):
            if not self.playing:
                return
            if self.local_pos <= self.loop_time:
                self.time_callback()
            self.stream.write(chunk._data)

        # Done
        self.stop()

    def play(self):
        MUSIC.KILLERS.append(self.stop)
        self.__play_with_pyaudio(self.clip)

    def stop(self):
        if self.playing:
            self.playing = False


class LoopPlayer(threading.Thread):

    def __init__(self, full_clip: AudioSegment, loop_time: float):
        self.players = []
        """:type : List[Player]"""
        self.full_clip = full_clip
        self.loop_time = loop_time * 1000
        self.stopped = False
        super().__init__(target=self.loop)
        self.position = MUSIC.position()

    def loop(self):
        while not self.stopped:
            self.play(self.position)
            # loop_range = self.loop_time - self.position if self.position < self.loop_time else
            if MUSIC.position() > self.loop_time:
                while MUSIC.position() > self.loop_time:
                    MUSIC.POSITION -= self.loop_time
            self.position = MUSIC.position()
            loop_range = self.loop_time - self.position

            sleep(loop_range / 1000.0)
            self.position = MUSIC.POSITION = 0

    def update_time(self):
        self.position += MUSIC.BITE_SIZE_MS

    def play(self, position: int):
        p = Player(
            clip=self.full_clip,
            start_pos=position,
            loop_time=round(self.loop_time),
            callback=self.update_time
        )
        p.start()
        self.players.append(p)

    def stop(self):
        MUSIC.POSITION = self.position
        self.stopped = True
        MUSIC.kill()


class Voice(object):
    """
    The instrument used to play a track
    This is basically just an audio clip wrapper
    """
    def __init__(self, clip_file: str, beats: int=None):
        self.clip = AudioSegment.from_mp3(clip_file)
        self.filename = clip_file

        self.beats = beats


class Timing(object):
    """
    Container for tempo and rhythm properties of a Song Section
    """

    @property
    def signature(self):
        return "{}/{}".format(self.sig_n, self.sig_d)

    def __init__(self, tempo: int or float, sig_n: int = 4, sig_d: int = 4):
        self.tempo = tempo
        self.seconds_per_bar = sig_n / tempo * 60

        self.sig_n = sig_n
        self.sig_d = sig_d

    def get_loop_seconds_from_voice(self, voice: Voice):
        return self.seconds_per_bar * voice.beats


class Loop(object):
    """
    A set of voices within a section
    """

    def __init__(self, voices: List[Voice]):
        self.__timing = None
        self.__time = None
        self.__bars = None
        self.looper = None
        """: type : LoopPlayer"""

        self.all_voices = voices

    @property
    def num_voices(self):
        return len(self.all_voices)

    @property
    def timing(self) -> Timing:
        return self.__timing

    @timing.setter
    def timing(self, value: Timing):
        self.__timing = value

    @property
    def first_voice(self) -> Voice:
        return self.all_voices[0]

    @property
    def longest_voice(self) -> Voice:
        return next(v for v in self.all_voices if v.beats == max(v.beats for v in self.all_voices))

    @property
    def time(self):
        if not self.__time:
            self.__time = self.timing.get_loop_seconds_from_voice(self.longest_voice)
        return self.__time

    @property
    def bars(self):
        """
        This part is good
        :return:
        """
        if not self.__bars:
            self.__bars = self.longest_voice.beats
        return self.__bars

    @property
    def bar_length(self):
        return self.time / self.bars

    def active_mix(self, req_voices: int):
        top_voices = int(min(req_voices, self.num_voices))
        active_voices = [self.all_voices[n] for n in range(0, top_voices)]
        return self.mix(active_voices)

    def mix(self, voices: List[Voice]):
        """
        Mix the requested voices together and return the audio clip
        :param voices:
        :return:
        """
        mix = voices[0].clip
        for v in range(1, len(voices)):
            voice = voices[v]
            clip_bars = voice.beats
            for rep in range(round(self.bars/clip_bars)):
                pos = rep*self.bar_length*clip_bars*1000
                mix = mix.overlay(voice.clip, position=pos)
        return mix

    def start(self):
        # print("Playing up to {0} voices".format(self.num_active))
        if MUSIC.can_play():
            self.looper = LoopPlayer(
                full_clip=self.active_mix(req_voices=MUSIC.get_voices()),
                loop_time=self.time
            )
            # print("Created a loop, now trying to start it")
            self.looper.start()

    def stop(self):
        """
        Please kill the music
        :return:
        """
        if self.looper:
            self.looper.stop()
        self.looper = None

    def restart(self):
        self.stop()
        self.start()

    def change_voices(self):
        req_voices = MUSIC.get_voices()
        if req_voices <= 0:
            self.stop()
        if req_voices <= self.num_voices:
            self.restart()


class Section(object):
    """
    A set of bars of a song, with a unifying tempo
    """
    def __init__(self, name: str, timing: Timing, loops: List[Loop]):
        self.loops = loops
        for b in self.loops:
            b.timing = timing
        self.name = name
        self.timing = timing

    def get_loop(self, ix: int):
        try:
            return self.loops[ix]
        except IndexError:
            print("Loop not found: {0}".format(ix))
            return None


class Song(object):
    """
    A complete song, comprised of sections * tracks
    """

    def __init__(self, name: str, sections: List[Section]):
        self.sections = sections
        self.name = name
