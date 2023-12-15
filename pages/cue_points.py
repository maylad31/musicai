
import streamlit as st
import librosa
import numpy as np
import librosa
import numpy as np
from scipy.signal import find_peaks

def find_energy_segments(audio_file, num_segments=30, top_n=5):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Calculate segment length in samples
    segment_length = len(y) // num_segments

    high_energy_segments = []
    low_energy_segments = []

    # Iterate through segments to calculate RMS energy
    for i in range(num_segments):
        segment_start = i * segment_length
        segment_end = min(segment_start + segment_length, len(y))

        segment = y[segment_start:segment_end]

        # Calculate RMS energy for the segment
        energy = np.sqrt(np.mean(segment ** 2))

        # Store the segment and its energy
        if len(high_energy_segments) < top_n or energy > np.min([seg[2] for seg in high_energy_segments]):
            high_energy_segments.append((segment_start, segment_end, energy))
            high_energy_segments = sorted(high_energy_segments, key=lambda x: x[2], reverse=True)[:top_n]

        if len(low_energy_segments) < top_n or energy < np.max([seg[2] for seg in low_energy_segments]):
            low_energy_segments.append((segment_start, segment_end, energy))
            low_energy_segments = sorted(low_energy_segments, key=lambda x: x[2])[:top_n]

    # Extract start and end times for the selected high and low energy segments
    high_energy_times = [(start / sr, end / sr) for start, end, _ in high_energy_segments]
    low_energy_times = [(start / sr, end / sr) for start, end, _ in low_energy_segments]

    return high_energy_times, low_energy_times

st.subheader('Upload a track')
prev = st.file_uploader('Choose mp3 file(prev track)', type='mp3')
out_path=False
if prev is not None:
    with open('previous.wav', 'wb') as f:
        a=prev.read()
        f.write(a)
    st.audio(a, format='audio/wav')
    out_path=True


if out_path:
    cue_points =find_energy_segments("previous.wav")
    
        
        
    st.write("high energy: "+str(cue_points[0]))
    st.write("low energy: "+str(cue_points[1]))
   
    
