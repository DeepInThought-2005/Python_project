# Entry point for pygbag (browser build); desktop can run chessL.py directly.
import asyncio

import pygame

from chessL import main

asyncio.run(main())
