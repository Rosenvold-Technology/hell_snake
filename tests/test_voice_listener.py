import builtins
from unittest.mock import MagicMock
from src.voice_listener import VoiceCommandListener
from src.stratagem import Stratagem


def test_voice_command_triggers_macro():
    strat = Stratagem("Resupply", "Mission", [0], "icon")
    controller = MagicMock()
    controller.get_stratagems.return_value = {"0": strat}
    listener = VoiceCommandListener(controller)
    listener._handle_command("resupply")
    controller.trigger_macro.assert_called_once_with(strat)

