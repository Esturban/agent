"""Three-node voice pipeline: transcribe → respond → speak.

Audio in  ──► Whisper ──► transcript ──► LLM ──► text response ──► TTS ──► audio out

The graph makes the latency structure explicit: STT, LLM, and TTS are each a
distinct node. In production the TTS node can stream sentence-by-sentence
(TTFA optimisation) rather than waiting for the full LLM response.
"""

import tempfile
from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from .tools import MODEL_LLM, speech_to_text, text_to_speech


class VoiceState(TypedDict):
    audio_in: str    # path to input mp3
    transcript: str  # Whisper output
    response: str    # LLM text answer
    audio_out: str   # path to TTS output mp3


def transcribe(state: VoiceState) -> dict:
    text = speech_to_text(state["audio_in"])
    print(f"  [STT] {text}")
    return {"transcript": text}


def respond(state: VoiceState) -> dict:
    llm = ChatOpenAI(model=MODEL_LLM)
    answer = llm.invoke([HumanMessage(content=state["transcript"])]).content
    return {"response": answer}


def speak(state: VoiceState) -> dict:
    out = tempfile.mktemp(suffix=".mp3")
    text_to_speech(state["response"], out)
    return {"audio_out": out}


def create_workflow():
    g = StateGraph(VoiceState)
    g.add_node("transcribe", transcribe)
    g.add_node("respond", respond)
    g.add_node("speak", speak)
    g.add_edge(START, "transcribe")
    g.add_edge("transcribe", "respond")
    g.add_edge("respond", "speak")
    g.add_edge("speak", END)
    return g.compile()
