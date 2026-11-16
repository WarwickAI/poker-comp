from __future__ import annotations

import multiprocessing
import queue
import sys


# Every table is shown in one window, which is run by a process of its own so that it carries on drawing while the AIs think.
# The AIs and the tournament stay in the main process, which sends the window the hands played at each table as they are needed.
#
# The window sends the main process (generation, table, message), where the message is one of
#   "need"     the table has shown everything it was sent, and is ready for its next hand
#   "restart"  R was pressed, which isn't about one table, so the table is 0
#   "closed"   the window has closed, because ESC was pressed or it was closed, and the table is 0
# The generation goes up every time the tournament restarts, so that messages sent before a restart can be told apart.
#
# The main process sends the window one of
#   ("hand", table, hand)                               a hand to show at a table
#   ("finish", table, title, lines, hints, close_after) a table has no more hands to come, so show this once its last one is over
#   ("reset", generation, tables)                       the tournament has started again, with these players at each table
#   ("quit",)                                           close the window


def show_tables(tables: dict[int, list[str]], total_hands: int, fullscreen: bool, generation: int, commands: multiprocessing.Queue, events: multiprocessing.Queue):
    try:
        run_window(tables, total_hands, fullscreen, generation, commands, events)
    except KeyboardInterrupt:
        pass  # Ctrl+C in the terminal reaches the window as well as the main process, which deals with it


def run_window(tables: dict[int, list[str]], total_hands: int, fullscreen: bool, generation: int, commands: multiprocessing.Queue, events: multiprocessing.Queue):
    from .render import PokerWindow

    window = PokerWindow(tables=tables, total_hands=total_hands, fullscreen=fullscreen)
    asked: set[int] = set()  # The tables which have asked for their next hand and not been sent it yet

    try:
        while window.is_window_open():
            try:
                while True:
                    command = commands.get_nowait()

                    if command[0] == "hand":
                        if command[1] in window.tables:
                            window.tables[command[1]].push(command[2])

                        asked.discard(command[1])

                    elif command[0] == "finish":
                        if command[1] in window.tables:
                            window.tables[command[1]].finish(*command[2:])

                    elif command[0] == "reset":
                        generation = command[1]
                        window.reset(command[2])
                        asked = set()

                    elif command[0] == "quit":
                        return

            except queue.Empty:
                pass

            if window.should_restart():
                events.put((generation, 0, "restart"))

            for number, table in window.tables.items():
                if number not in asked and table.needs_hand():
                    events.put((generation, number, "need"))
                    asked.add(number)

            window.update()

    finally:
        window.close()
        events.put((generation, 0, "closed"))


class Window:
    # The window, from the main process's side
    def __init__(self, *, total_hands: int, fullscreen: bool, sys_path: list[str] | None = None):
        # The window's process is started with sys_path as its module search path. The bots' folders are added to it as they are
        # loaded, and a team's snapshot holds its own copy of the poker folder, which the window must never import in place of this one.
        self.sys_path = list(sys_path) if sys_path is not None else list(sys.path)
        self.context = multiprocessing.get_context("spawn")  # The same on every system, and nothing from the main process is copied into the window
        self.events = self.context.Queue()
        self.commands = self.context.Queue()
        self.total_hands = total_hands
        self.fullscreen = fullscreen
        self.process: multiprocessing.Process | None = None
        self.open = False
        self.generation = 0

    def start(self, tables: dict[int, list[str]]):
        # Opens the window with every table in it, or starts again in it if it is already open
        self.generation += 1

        if self.open:
            self.send("reset", self.generation, tables)
            return

        self.process = self.context.Process(target=show_tables, args=(tables, self.total_hands, self.fullscreen, self.generation, self.commands, self.events), daemon=True)
        searched = sys.path[:]
        sys.path[:] = self.sys_path  # A spawned process is given the search path in place when it starts

        try:
            self.process.start()
        finally:
            sys.path[:] = searched

        self.open = True

    def send(self, *command):
        if self.open:
            self.commands.put(command)

    def next_event(self) -> tuple[int, str] | None:
        # Waits for the window to say something. Anything sent before the latest restart is dropped, apart from the window closing.
        while True:
            try:
                generation, number, message = self.events.get(timeout=0.5)
                break

            except queue.Empty:
                # A window which crashed before it could say so, such as when raylib can't open it, counts as closed
                if not self.process.is_alive():
                    self.open = False
                    return 0, "closed"

        if message == "closed":
            self.open = False
            return number, message

        if generation != self.generation:
            return None

        return number, message

    def close(self):
        self.send("quit")

        if self.process is not None:
            self.process.join(timeout=2)

            if self.process.is_alive():
                self.process.terminate()

        # Anything still waiting to be sent to the window is thrown away, rather than holding up the exit
        self.commands.cancel_join_thread()
        self.commands.close()
