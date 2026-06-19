"""
4 attacks × 3 defenses comparison matrix.

Runs every (attack, defense) combination and returns a results grid.
Each cell records whether the canary leaked and the response snippet.

This is the core of the example: the matrix makes the paper's findings
concrete and visually clear.
"""

from prompts.system_prompt import VARIANTS
from prompts.attack_variants import ATTACKS
from prompts.defenses import DEFENSES
from .attacker import run_attack
from .monitor import scan


def build_matrix() -> list[dict]:
    """
    Returns a list of result dicts, one per (attack, defense, system_prompt) combination.
    Each dict: {attack_name, defense_name, system_name, leaked, canaries, response_snippet, patterns}
    """
    results = []
    for sys_name, base_system in VARIANTS:
        for def_name, defense_text, _ in DEFENSES:
            full_system = (defense_text + "\n\n" + base_system).strip() if defense_text else base_system
            for atk_name, attack_prompt, _ in ATTACKS:
                _turn1, turn2 = run_attack(full_system, attack_prompt)
                scan_result = scan(turn2, attack_prompt)
                results.append({
                    "system":   sys_name,
                    "defense":  def_name,
                    "attack":   atk_name,
                    "leaked":   scan_result["canary_leaked"],
                    "canaries": scan_result["canaries_found"],
                    "response": turn2[:200],
                })
    return results
