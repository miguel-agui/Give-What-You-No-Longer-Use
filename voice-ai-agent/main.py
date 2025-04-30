import os
import yaml

def load_prompt(filename):
  """Load a prompt from a YAML file."""
  prompt_path = os.path.join(filename)

  try:
    with open(prompt_path, 'r') as file:
        prompt_data = yaml.safe_load(file)
        return prompt_data.get('instructions', '')
  except (FileNotFoundError, yaml.YAMLError) as e:
    print(f"Error loading prompt file {filename}: {e}")
    return ""


import logging
import aiohttp
from typing import Annotated
from pathlib import Path
from dotenv import load_dotenv
from livekit import api
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.llm import function_tool
from livekit.agents.voice import Agent, AgentSession, RunContext
from livekit.plugins import (
    # google,
    deepgram,
    silero,
    turn_detector,
    noise_cancellation
    )
from livekit.agents import RoomInputOptions
from livekit.plugins.turn_detector.english import EnglishModel
from livekit.plugins.turn_detector.multilingual import MultilingualModel

import sys

from livekit.plugins.google.beta.realtime.realtime_api import RealtimeModel

from datetime import datetime
import random
import string

logger = logging.getLogger("function-calling")
logger.setLevel(logging.INFO)

load_dotenv()

class FunctionAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=load_prompt('voice-ai-agent/prompts/support-agent.yaml'),
            llm=RealtimeModel(
            model= "gemini-2.0-flash-exp",
            voice="Puck",
            temperature=0.8,
            ),
        )
    @function_tool
    async def identify_user(self, context: RunContext,name: str):
      """
      Called in order to identify a user

      Args:
          name: The name of the user.
      """
      # making the call to search for user in DB
      pass

    @function_tool
    async def post_donation(self, context: RunContext, title: str, category: str, images: list[str]):
      """
      Called when uploading new products or servces

      Args:
          title: The title of the product or service.
          category: The category of the product or service.
          images: The images of the product or service
      """
      # making the API call to POST donation
      pass
    
    @function_tool
    async def get_recommended_items(self, context: RunContext, category: str):
      """
      Describe suggested items based on interest or category

      Args:
          category: The category of the product or service.
      """
      # Making the API call to get recommended items
      pass

    @function_tool
    async def search_items(self, context: RunContext, keyword: str):
      """
      Help find listings by keyword or category

      Args:
          keyword: The keyword or category of the product or service.
      """
      # Making the call to search items
      pass

      


    async def on_enter(self):
        self.session.generate_reply(
            # instructions="Greet the user and offer your assistance."
            instructions=""" Greet the user and introduce yourself as the assistant for 'Donate What You No Longer Use'.
            Be conversational and knowledgeable
            """
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession()

    await session.start(
        agent=FunctionAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        )
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
