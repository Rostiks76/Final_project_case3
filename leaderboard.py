"""
Модуль для отображения таблицы лидеров.
"""

from typing import List
from datetime import datetime

from models import LeaderboardEntry


def display_leaderboard(entries: List[LeaderboardEntry]) -> None:
    """
    Выводит таблицу лидеров в красивом форматированном виде.
    
    Args:
        entries: Список записей таблицы лидеров
    """
    print("\n" + "=" * 60)
    print("🏆 ТАБЛИЦА ЛИДЕРОВ")
    print("=" * 60)
    
    if not entries:
        print("\n   Пока нет результатов. Станьте первым!")
        print("=" * 60)
        return
    
    print(f"\n{'№':<4} {'Имя игрока':<25} {'Баллы':<8} {'Дата':<20}")
    print("-" * 60)
    
    for idx, entry in enumerate(entries, 1):
        # Форматируем дату
        if isinstance(entry.date_played, str):
            date_str = entry.date_played[:16]  # Обрезаем до YYYY-MM-DD HH:MM
        else:
            date_str = entry.date_played.strftime("%Y-%m-%d %H:%M")
        
        print(f"{idx:<4} {entry.player_name:<25} {entry.score:<8} {date_str:<20}")
    
    print("=" * 60)