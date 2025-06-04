# services/menu_service.py
"""Service layer for managing menu and dishes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SectionDTO:
    """Menu section with dishes."""

    name: str
    dishes: List[dict]


_DISHES: Dict[int, dict] = {
    1: {"name": "Doner", "price": 10.0, "visible": True},
    2: {"name": "Burger", "price": 8.0, "visible": True},
}


async def toggle_visible(dish_id: int) -> None:
    """Toggle visibility for a dish."""
    dish = _DISHES.get(dish_id)
    if dish:
        dish["visible"] = not dish.get("visible", True)


async def get_visible_menu(lang: str = "kk") -> List[SectionDTO]:
    """Return visible dishes grouped into a single section."""
    visible = [
        {"id": did, "name": data["name"], "price": data["price"]}
        for did, data in _DISHES.items()
        if data.get("visible", True)
    ]
    return [SectionDTO(name="main", dishes=visible)]
