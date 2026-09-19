"""Interactive Whisper ASR demo with a Praat-based acoustic visualisation.

Run with: uv run python asr_demo.py
"""

from __future__ import annotations

import os
from pathlib import Path

import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import parselmouth
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).with_name("secret.env"))
client = OpenAI()


def praat_figure(audio_path: str):
    """Build a waveform, spectrogram, pitch, and formant plot using Praat."""
    sound = parselmouth.Sound(audio_path)
    waveform = sound.values[0]
    times = sound.xs()

    pitch = sound.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    pitch_times = pitch.xs()
    frequencies = pitch.selected_array["frequency"]
    frequencies[frequencies == 0] = np.nan

    spectrogram = sound.to_spectrogram(
        window_length=0.03, maximum_frequency=8000
    )
    spec_db = 10 * np.log10(np.maximum(spectrogram.values, 1e-12))

    fig, (wave_ax, spec_ax) = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True, height_ratios=(1, 2)
    )
    wave_ax.plot(times, waveform, color="black", linewidth=0.7)
    wave_ax.set(title="Waveform", ylabel="Amplitude")
    wave_ax.grid(alpha=0.2)

    spec_ax.pcolormesh(
        spectrogram.x_grid(),
        spectrogram.y_grid(),
        spec_db,
        shading="auto",
        cmap="magma",
    )
    spec_ax.set(title="Praat spectrogram with pitch and formants", xlabel="Time (s)", ylabel="Frequency (Hz)")
    spec_ax.set_ylim(0, 8000)

    try:
        formants = sound.to_formant_burg(maximum_formant=5500)
        formant_times = formants.xs()
        for index, colour, label in ((1, "#36d65d", "F1"), (2, "#68b7ff", "F2")):
            values = np.array(
                [formants.get_value_at_time(index, time) for time in formant_times]
            )
            spec_ax.plot(formant_times, values, color=colour, linewidth=1.4, label=label)
    except Exception:
        pass

    pitch_ax = spec_ax.twinx()
    pitch_ax.plot(pitch_times, frequencies, color="cyan", linewidth=1.5, label="F0 / pitch")
    pitch_ax.set_ylabel("Pitch (Hz)", color="cyan")
    pitch_ax.tick_params(axis="y", labelcolor="cyan")
    pitch_ax.set_ylim(75, 500)

    handles, labels = spec_ax.get_legend_handles_labels()
    pitch_handles, pitch_labels = pitch_ax.get_legend_handles_labels()
    if handles or pitch_handles:
        spec_ax.legend(handles + pitch_handles, labels + pitch_labels, loc="upper right")

    fig.tight_layout()
    return fig


def transcribe_and_visualise(audio_path: str | None):
    if not audio_path:
        raise gr.Error("Upload a WAV file or record an audio clip first.")

    if not os.environ.get("OPENAI_API_KEY"):
        raise gr.Error("Set OPENAI_API_KEY in secret.env, then restart the app.")

    try:
        with Path(audio_path).open("rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment", "word"],
            )
        figure = praat_figure(audio_path)
        return transcription.text, figure
    except Exception as exc:
        raise gr.Error(f"Could not process this recording: {exc}") from exc


demo = gr.Interface(
    fn=transcribe_and_visualise,
    inputs=gr.Audio(
        sources=["upload", "microphone"],
        type="filepath",
        label="Upload a WAV file or record your voice",
    ),
    outputs=[
        gr.Textbox(label="Whisper transcription", lines=5),
        gr.Plot(label="Praat acoustic visualisation"),
    ],
    title="Automatic Speech Recognition Demo",
    description="Record speech or upload audio, then inspect its transcription, waveform, spectrogram, pitch (F0), and formants.",
)


if __name__ == "__main__":
    demo.launch()
