# https://stackoverflow.com/a/55788901 -> on macos: pyaudio fails to be installed due to the missing header file portaudio.h. installing portaudio with brew resolves this issue
import pyaudio
import numpy as np
from scipy import signal

import Config as C

'''
example output for a sound device with pyaudio get_device_info_by_index
{'index': 2, 'structVersion': 2, 'name': 'Anua Mic CM 900', 'hostApi': 0, 'maxInputChannels': 1, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.0057083333333333335, 'defaultLowOutputLatency': 0.01, 'defaultHighInputLatency': 0.015041666666666667, 'defaultHighOutputLatency': 0.1, 'defaultSampleRate': 48000.0}
'''

class AudioDevice:
    def __init__(self, index: int, name: str, max_input_channels: int=1, sample_rate: float=48000) -> None:
        self.index = index
        self.name = name
        self.max_input_channels = max_input_channels
        self.sample_rate = sample_rate

    def to_string(self) -> str:
        return f"id: {self.index}; name: {self.name}"

class AudioInput:
  CHUNK_SIZE = C.Audio.CHUNK_SIZE #eq to sample rate
  FORMAT = C.Audio.FORMAT
  CHANNELS = C.Audio.CHANNELS
  RATE = C.Audio.RATE

  def __init__(self) -> None:
    self.py_audio = pyaudio.PyAudio()

    self.kernel = signal.gaussian(C.Frequency.KERNEL_SIZE, C.Frequency.KERNEL_SIG)
    self.kernel /= np.sum(self.kernel)

    self.devices_length = self.py_audio.get_device_count()
    #contains all devices on the machine that support the configuration on top of def __init__
    self.supported_devices: list[AudioDevice] = []
    self.selected_device = None
    
    self.stream = None
    #whistle input list
    self.frequencies = []

  def _check_input_devices(self) -> None:
    for i in range(self.devices_length):
      device = self.py_audio.get_device_info_by_index(device_index=i)

      try:
        #before presenting a list of devices to the user, check if the configuration works for the device. is_format_supported raises an exception if the device does not support the config.
        if self.py_audio.is_format_supported(
          rate=self.RATE,
          input_channels=self.CHANNELS,
          input_device=device.get("index"),
          input_format=self.FORMAT,
        ):
          self.supported_devices.append(
            AudioDevice(index=device.get("index"), name=device.get("name"))
          )
      except:
          pass

  def _get_device_by_id(self, index: int) -> AudioDevice:
    if isinstance(index, int):
      for device in self.supported_devices:
        if device.index == index:
          return device

    return None

  def _get_valid_index(self) -> None:
    '''
      reads input from terminal that checks for correct data type and does retries
    '''
    count = 0
    while True:
      try:
        selected_index = int(input())
        if selected_device := self._get_device_by_id(selected_index):
          print(
            f"\nYou selected input device {selected_device.name} with id {selected_device.index}"
          )
          self.selected_device = selected_device

          break
        else:
          count += 1
          if count > 2:
            raise Exception("too many tries...")
          print(
              "The device id must be from the list above. Please try again."
          )

      except ValueError:
        count += 1
        if count > 2:
          raise Exception("too many tries...")
        print("The device id must be an integer. Please try again.")

  def request_input_device_index(self) -> None:
    self._check_input_devices()
    devices_length = len(self.supported_devices)

    if devices_length:
      print(f"We found {devices_length} devices on your machine:")
      for device in self.supported_devices:
          print(device.to_string())

      print("\nPlease enter the device id to select it!")
      self._get_valid_index()

    else:
      print(
        f"We found no supported devices on your machine. Please plugin a device that supports {self.CHANNELS} input channel, {self.RATE}Hz sampling rate, {self.FORMAT}-bit audio. Then try again."
      )

  def open_stream(self) -> None:
    self.stream = self.py_audio.open(
      format=self.FORMAT,
      channels=self.CHANNELS,
      rate=self.RATE,
      input=True,
      frames_per_buffer=self.CHUNK_SIZE,
      input_device_index=self.selected_device.index,
    )

  def _read_stream(self) -> float:
    buffer = self.stream.read(AudioInput.CHUNK_SIZE, exception_on_overflow=False)
    data = np.frombuffer(buffer, dtype=np.int16)
    #added a kernel in this version to reduce background noise
    data = np.convolve(data, self.kernel, "same")

    fft = np.fft.fft(data)
    freq = np.fft.fftfreq(AudioInput.CHUNK_SIZE, 1/AudioInput.RATE)

    return np.abs(freq[np.argmax(fft)])

  def stop_stream(self) -> None:
    if self.stream:
      self.stream.stop_stream()

  def end_stream(self) -> None:
    if self.stream:
      self.stream.close()
    self.py_audio.terminate()

  def get_direction(self) -> int:
    '''
      :return: -1 -> down; 1 -> up; 0 -> no change
    '''
    data = self._read_stream()

    #clear frequencies list if there is input that is off the boundries because this means that the user is currently not/no longer whistling
    if data < C.Frequency.LOWER or data > C.Frequency.UPPER:
      self.frequencies = []
      
      return 0
    else:
      self.frequencies.append(data)

    print(self.frequencies)

    # self.frequencies must have a min length so that we analyse the trend of frequencies
    if len(self.frequencies) > C.Frequency.MIN_LENGTH:
      trend_count = {"up": 0, "down": 0, "straigth": 0}

      trend_list = np.diff(self.frequencies)
      for trend_item in trend_list:
        if trend_item > 0:
          trend_count["up"] += 1
        elif trend_item < 0:
          trend_count["down"] += 1
        else:
          trend_count["straigth"] += 1

      self.frequencies = []

      #introducing whistle threshold: there must be a distinct trend direction for direction change up/down
      #trend_direction == "up" and
      if np.sum([trend_count["down"] * - 1, trend_count["up"]]) >= C.Frequency.WHISTLE_UP_THRESHOLD:
        return 1
      
      #trend_direction == "down"
      elif np.sum([trend_count["down"] * - 1, trend_count["up"]]) <= C.Frequency.WHISTLE_DOWN_THRESHOLD:
        return -1
      
      else:
        return 0

    return 0