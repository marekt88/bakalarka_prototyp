import asyncio
import os

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()

async def create_classic_assistant(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful and professional assistant. You provide clear, concise answers "
            "and maintain a formal, business-like tone. You excel at organizing information "
            "and presenting it in a structured manner."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(voice="alloy"),  # Using a more formal voice
        chat_ctx=initial_ctx
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hello, I'm your professional assistant. How may I help you today?", allow_interruptions=True)

async def create_friendly_assistant(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a friendly, casual, and engaging assistant with a warm personality. "
            "You use a conversational tone and occasionally add light humor to make interactions "
            "more enjoyable. While maintaining helpfulness, you keep the conversation natural "
            "and relatable, as if chatting with a friend."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(voice="nova"),  # Using a warmer, more casual voice
        chat_ctx=initial_ctx
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hey there! 👋 I'm your friendly AI assistant. What's on your mind?", allow_interruptions=True)

async def entrypoint(ctx: JobContext):
    # Get the assistant version from the room name
    room_name = ctx.room.name if ctx.room and ctx.room.name else ""
    
    if "v3" in room_name.lower():
        await create_friendly_assistant(ctx)
    else:
        await create_classic_assistant(ctx)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
