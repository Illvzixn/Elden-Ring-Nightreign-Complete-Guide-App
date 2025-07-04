from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Dict, Optional
import os
import uuid
from datetime import datetime
import re

app = FastAPI(title="Elden Ring Nightreign Boss Guide API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
MONGO_URL = os.environ.get('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.nightreign_guide

# Collections
bosses_collection = db.bosses
characters_collection = db.characters
builds_collection = db.builds
achievements_collection = db.achievements
walkthroughs_collection = db.walkthroughs
user_ratings_collection = db.user_ratings
custom_builds_collection = db.custom_builds

# Sample data initialization
def initialize_data():
    # Initialize all 8 Nightlords
    bosses = [
        {
            "id": str(uuid.uuid4()),
            "name": "Gladius, Beast of Night",
            "expedition_name": "Tricephalos",
            "description": "The initial Nightlord that players encounter. Defeating Gladius unlocks access to subsequent bosses.",
            "weaknesses": ["Holy"],
            "damage_types": ["Physical", "Dark"],
            "difficulty_rating": 3,
            "min_level": 1,
            "max_level": 5,
            "recommended_strategies": [
                "Use holy damage attacks to exploit weaknesses",
                "Focus on dodging its charging attacks",
                "Attack after it completes its combo sequences"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Wylder", "Guardian", "Ironeye"],
            "recommended_builds": ["Wylder Versatile", "Guardian Tank", "Ironeye Marksman"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Maris, Fathom of Night",
            "expedition_name": "Augur",
            "description": "A water-based Nightlord with aquatic abilities and devastating area attacks.",
            "weaknesses": ["Lightning"],
            "damage_types": ["Water", "Dark"],
            "difficulty_rating": 5,
            "min_level": 6,
            "max_level": 8,
            "recommended_strategies": [
                "Utilize lightning attacks to exploit weaknesses",
                "Stay mobile to avoid water-based area attacks",
                "Use ranged attacks when possible"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Ironeye", "Recluse", "Duchess"],
            "recommended_builds": ["Ironeye Marksman", "Recluse Spellcaster", "Duchess Shadow"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gnoster, Wisdom of Night",
            "expedition_name": "Sentient Pest",
            "description": "A cunning Nightlord that uses intelligence and fire-based attacks.",
            "weaknesses": ["Fire"],
            "damage_types": ["Intelligence", "Fire"],
            "difficulty_rating": 6,
            "min_level": 9,
            "max_level": 11,
            "recommended_strategies": [
                "Use fire attacks to counter its abilities",
                "Interrupt its casting with quick attacks",
                "Focus on maintaining distance"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Executor", "Wylder"],
            "recommended_builds": ["Recluse Spellcaster", "Executor Duelist", "Wylder Versatile"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Adel, Baron of Night",
            "expedition_name": "Gaping Jaw",
            "description": "A formidable poison-based Nightlord with powerful jaw attacks.",
            "weaknesses": ["Poison"],
            "damage_types": ["Poison", "Physical"],
            "difficulty_rating": 7,
            "min_level": 12,
            "max_level": 14,
            "recommended_strategies": [
                "Use poison-resistant equipment",
                "Attack from the sides to avoid jaw attacks",
                "Focus on hit-and-run tactics"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Duchess", "Executor", "Guardian"],
            "recommended_builds": ["Duchess Shadow", "Executor Duelist", "Guardian Tank"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Caligo, Miasma of Night",
            "expedition_name": "Fissure in the Fog",
            "description": "A fog-based Nightlord that creates confusion and uses fire attacks.",
            "weaknesses": ["Fire"],
            "damage_types": ["Fog", "Fire"],
            "difficulty_rating": 8,
            "min_level": 15,
            "max_level": 15,
            "recommended_strategies": [
                "Use fire attacks to clear fog",
                "Stay grouped to avoid getting separated",
                "Use area-of-effect abilities"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Raider", "Revenant"],
            "recommended_builds": ["Recluse Spellcaster", "Raider Berserker", "Revenant Support"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Libra, Creature of Night",
            "expedition_name": "Equilibrious Beast",
            "description": "A unique Nightlord that can make pacts and alter battle conditions.",
            "weaknesses": ["Madness", "Fire"],
            "damage_types": ["Psychic", "Dark"],
            "difficulty_rating": 7,
            "min_level": 16,
            "max_level": 18,
            "recommended_strategies": [
                "Use madness-inducing attacks",
                "Consider making pacts for advantages",
                "Interrupt its meditation phases"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Revenant", "Wylder"],
            "recommended_builds": ["Recluse Spellcaster", "Revenant Support", "Wylder Versatile"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fulghor, Champion of Nightglow",
            "expedition_name": "Darkdrift Knight",
            "description": "One of the most challenging Nightlords with rapid movements and powerful attacks.",
            "weaknesses": ["Lightning"],
            "damage_types": ["Dark", "Physical"],
            "difficulty_rating": 9,
            "min_level": 19,
            "max_level": 21,
            "recommended_strategies": [
                "Use lightning attacks for maximum damage",
                "Focus on precise dodging and timing",
                "Use defensive abilities to survive combos"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Guardian", "Ironeye", "Executor"],
            "recommended_builds": ["Guardian Tank", "Ironeye Marksman", "Executor Duelist"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Heolstor, the Nightlord",
            "expedition_name": "Night Aspect",
            "description": "The final boss with a two-phase battle. The ultimate challenge in Nightreign.",
            "weaknesses": ["Holy"],
            "damage_types": ["Dark", "All Elements"],
            "difficulty_rating": 10,
            "min_level": 22,
            "max_level": 25,
            "recommended_strategies": [
                "Use holy damage for maximum effectiveness",
                "Master all mechanics from previous bosses",
                "Coordinate team attacks carefully",
                "Prepare for phase transitions"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils", "Nightlord Crown"],
            "recommended_team": ["All characters viable", "Team composition crucial"],
            "recommended_builds": ["All builds viable", "Master level required"]
        }
    ]
    
    # Initialize characters with accurate abilities
    characters = [
        {
            "id": str(uuid.uuid4()),
            "name": "Wylder",
            "description": "A versatile knight with balanced stats and a grappling hook for agility.",
            "primary_stat": "Balanced",
            "weapon_type": "Sword",
            "abilities": ["Claw Shot (grappling hook)", "Onslaught Stake (explosive crossbow)"],
            "damage_types": ["Physical", "Explosive"],
            "recommended_builds": ["Wylder Versatile", "Wylder Hybrid"],
            "starting_equipment": ["Longsword", "Crossbow", "Chain Mail"],
            "playstyle": "Versatile",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Raider",
            "description": "A strength-focused bruiser excelling in melee combat with colossal weapons.",
            "primary_stat": "Strength",
            "weapon_type": "Colossal Weapon",
            "abilities": ["Retaliate (damage stance)", "Totem Stela (buff totem)"],
            "damage_types": ["Physical", "Crushing"],
            "recommended_builds": ["Raider Berserker", "Raider Tank"],
            "starting_equipment": ["Greataxe", "Heavy Armor"],
            "playstyle": "Berserker",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Executor",
            "description": "A high-risk, high-reward character adept with katanas and deflection.",
            "primary_stat": "Dexterity",
            "weapon_type": "Katana",
            "abilities": ["Cursed Sword (deflection)", "Aspects of the Crucible - Beast"],
            "damage_types": ["Slash", "Arcane"],
            "recommended_builds": ["Executor Duelist", "Executor Beast"],
            "starting_equipment": ["Katana", "Light Armor"],
            "playstyle": "Duelist",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Recluse",
            "description": "A spellcaster with HP draining abilities and elemental attacks.",
            "primary_stat": "Intelligence",
            "weapon_type": "Staff",
            "abilities": ["HP Drain", "Boss Marking (extra damage)"],
            "damage_types": ["Magic", "Elemental"],
            "recommended_builds": ["Recluse Spellcaster", "Recluse Drain"],
            "starting_equipment": ["Sorcerer's Staff", "Robes"],
            "playstyle": "Spellcaster",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Guardian",
            "description": "A tank class specializing in absorbing damage and protecting teammates.",
            "primary_stat": "Strength",
            "weapon_type": "Halberd",
            "abilities": ["Whirlwind", "Wings of Salvation (AoE support)"],
            "damage_types": ["Physical", "Holy"],
            "recommended_builds": ["Guardian Tank", "Guardian Support"],
            "starting_equipment": ["Halberd", "Greatshield", "Plate Armor"],
            "playstyle": "Tank",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Duchess",
            "description": "A rogue-type character excelling in speed and agility with damage amplification.",
            "primary_stat": "Dexterity",
            "weapon_type": "Daggers",
            "abilities": ["Quickstep Dodge", "Ally Damage Double"],
            "damage_types": ["Slash", "Poison"],
            "recommended_builds": ["Duchess Shadow", "Duchess Support"],
            "starting_equipment": ["Twin Daggers", "Thief Outfit"],
            "playstyle": "Rogue",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ironeye",
            "description": "A long-ranged archer with tactical marking abilities.",
            "primary_stat": "Dexterity",
            "weapon_type": "Bow",
            "abilities": ["Marking (team damage boost)", "Distance Revival"],
            "damage_types": ["Piercing", "Tactical"],
            "recommended_builds": ["Ironeye Marksman", "Ironeye Support"],
            "starting_equipment": ["Composite Bow", "Leather Armor"],
            "playstyle": "Marksman",
            "max_level": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Revenant",
            "description": "A support character capable of summoning allies and providing invincibility.",
            "primary_stat": "Faith",
            "weapon_type": "Catalyst",
            "abilities": ["Summon Allies", "Invincibility Grant"],
            "damage_types": ["Summon", "Support"],
            "recommended_builds": ["Revenant Support", "Revenant Summoner"],
            "starting_equipment": ["Sacred Catalyst", "Ritual Robes"],
            "playstyle": "Support",
            "max_level": 15
        }
    ]
    
    # Initialize character-specific builds
    builds = [
        # Wylder builds
        {
            "id": str(uuid.uuid4()),
            "name": "Wylder Versatile",
            "character": "Wylder",
            "type": "Hybrid",
            "description": "Balanced build utilizing both melee and ranged capabilities with mobility.",
            "primary_weapon": "Marais Executioner's Blade",
            "secondary_weapon": "Explosive Crossbow",
            "armor_set": "Knight's Chainmail",
            "talismans": ["Versatility Charm", "Mobility Ring", "Balanced Medallion"],
            "recommended_stats": {"Strength": 10, "Dexterity": 10, "Vigor": 12, "Mind": 8},
            "strategy": "Use grappling hook for positioning, mix melee and ranged attacks",
            "best_for": ["Wylder"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wylder Hybrid",
            "character": "Wylder",
            "type": "Adaptive",
            "description": "Adaptive build focusing on weapon switching and tactical positioning.",
            "primary_weapon": "Longsword",
            "secondary_weapon": "Crossbow",
            "armor_set": "Adaptive Gear",
            "talismans": ["Weapon Mastery", "Tactical Awareness", "Quick Switch"],
            "recommended_stats": {"Strength": 12, "Dexterity": 12, "Vigor": 11, "Mind": 10},
            "strategy": "Adapt to enemy weaknesses, use mobility for advantage",
            "best_for": ["Wylder"]
        },
        # Raider builds
        {
            "id": str(uuid.uuid4()),
            "name": "Raider Berserker",
            "character": "Raider",
            "type": "Strength",
            "description": "Maximum damage output with colossal weapons and berserker tactics.",
            "primary_weapon": "Axe of Godfrey",
            "secondary_weapon": "Great Hammer",
            "armor_set": "Berserker's Plate",
            "talismans": ["Berserker's Rage", "Colossal Weapon Mastery", "Retaliate Enhancer"],
            "recommended_stats": {"Strength": 15, "Vigor": 13, "Endurance": 12, "Mind": 5},
            "strategy": "Use Retaliate for massive damage, overwhelm with heavy attacks",
            "best_for": ["Raider"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Raider Tank",
            "character": "Raider",
            "type": "Defensive",
            "description": "Tanky build focusing on damage absorption and team protection.",
            "primary_weapon": "Defensive Greataxe",
            "secondary_weapon": "Tower Shield",
            "armor_set": "Fortress Plate",
            "talismans": ["Damage Reduction", "Taunt Mastery", "Totem Power"],
            "recommended_stats": {"Strength": 12, "Vigor": 15, "Endurance": 13, "Mind": 5},
            "strategy": "Draw enemy attacks, use Totem Stela for team buffs",
            "best_for": ["Raider"]
        },
        # Executor builds
        {
            "id": str(uuid.uuid4()),
            "name": "Executor Duelist",
            "character": "Executor",
            "type": "Dexterity",
            "description": "High-risk, high-reward build focusing on perfect timing and counters.",
            "primary_weapon": "Cursed Katana",
            "secondary_weapon": "Wakizashi",
            "armor_set": "Duelist's Garb",
            "talismans": ["Perfect Timing", "Counter Mastery", "Dexterity Boost"],
            "recommended_stats": {"Dexterity": 15, "Vigor": 10, "Endurance": 12, "Arcane": 8},
            "strategy": "Use Cursed Sword for deflections, time counters perfectly",
            "best_for": ["Executor"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Executor Beast",
            "character": "Executor",
            "type": "Transformation",
            "description": "Beast transformation build utilizing Aspects of the Crucible.",
            "primary_weapon": "Beast Claws",
            "secondary_weapon": "Katana",
            "armor_set": "Crucible Vestments",
            "talismans": ["Beast Mastery", "Transformation Duration", "Primal Fury"],
            "recommended_stats": {"Dexterity": 12, "Vigor": 12, "Endurance": 10, "Arcane": 11},
            "strategy": "Transform into beast for powerful attacks, use katana for precision",
            "best_for": ["Executor"]
        },
        # Recluse builds
        {
            "id": str(uuid.uuid4()),
            "name": "Recluse Spellcaster",
            "character": "Recluse",
            "type": "Intelligence",
            "description": "Pure spellcaster build with maximum magical damage and HP drain.",
            "primary_weapon": "Moonlight Staff",
            "secondary_weapon": "Drain Catalyst",
            "armor_set": "Witch's Robes",
            "talismans": ["Spell Power", "HP Drain Mastery", "Marking Boost"],
            "recommended_stats": {"Intelligence": 15, "Vigor": 8, "Mind": 15, "Endurance": 7},
            "strategy": "Mark bosses for extra damage, drain HP for sustainability",
            "best_for": ["Recluse"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Recluse Drain",
            "character": "Recluse",
            "type": "Sustain",
            "description": "Sustain-focused build emphasizing HP drain and elemental control.",
            "primary_weapon": "Drain Staff",
            "secondary_weapon": "Elemental Catalyst",
            "armor_set": "Draining Vestments",
            "talismans": ["Life Steal", "Elemental Mastery", "Mana Efficiency"],
            "recommended_stats": {"Intelligence": 12, "Vigor": 11, "Mind": 12, "Endurance": 10},
            "strategy": "Sustain through HP drain, control battlefield with elements",
            "best_for": ["Recluse"]
        },
        # Guardian builds
        {
            "id": str(uuid.uuid4()),
            "name": "Guardian Tank",
            "character": "Guardian",
            "type": "Defensive",
            "description": "Ultimate tank build for maximum damage absorption and team protection.",
            "primary_weapon": "Guardian's Halberd",
            "secondary_weapon": "Greatshield",
            "armor_set": "Fortress Plate",
            "talismans": ["Ultimate Defense", "Damage Reduction", "Team Protection"],
            "recommended_stats": {"Strength": 12, "Vigor": 15, "Endurance": 13, "Mind": 5},
            "strategy": "Absorb damage, use Wings of Salvation for team support",
            "best_for": ["Guardian"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Guardian Support",
            "character": "Guardian",
            "type": "Support",
            "description": "Support-focused build emphasizing team buffs and area control.",
            "primary_weapon": "Support Halberd",
            "secondary_weapon": "Blessing Shield",
            "armor_set": "Support Plate",
            "talismans": ["Team Buff", "Area Control", "Healing Boost"],
            "recommended_stats": {"Strength": 10, "Vigor": 12, "Endurance": 11, "Mind": 12},
            "strategy": "Use Whirlwind for crowd control, Wings of Salvation for healing",
            "best_for": ["Guardian"]
        },
        # Duchess builds
        {
            "id": str(uuid.uuid4()),
            "name": "Duchess Shadow",
            "character": "Duchess",
            "type": "Stealth",
            "description": "Stealth and speed build focusing on hit-and-run tactics.",
            "primary_weapon": "Shadow Daggers",
            "secondary_weapon": "Poison Blades",
            "armor_set": "Shadow Garb",
            "talismans": ["Stealth Mastery", "Speed Boost", "Poison Mastery"],
            "recommended_stats": {"Dexterity": 15, "Vigor": 10, "Endurance": 13, "Mind": 7},
            "strategy": "Use quickstep for positioning, amplify ally damage",
            "best_for": ["Duchess"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Duchess Support",
            "character": "Duchess",
            "type": "Support",
            "description": "Support build focusing on team damage amplification and mobility.",
            "primary_weapon": "Support Daggers",
            "secondary_weapon": "Utility Blades",
            "armor_set": "Support Leather",
            "talismans": ["Team Damage", "Mobility Master", "Quick Actions"],
            "recommended_stats": {"Dexterity": 12, "Vigor": 11, "Endurance": 12, "Mind": 10},
            "strategy": "Double ally damage, provide mobile support",
            "best_for": ["Duchess"]
        },
        # Ironeye builds
        {
            "id": str(uuid.uuid4()),
            "name": "Ironeye Marksman",
            "character": "Ironeye",
            "type": "Ranged",
            "description": "Pure marksman build with maximum ranged damage and marking abilities.",
            "primary_weapon": "Precision Bow",
            "secondary_weapon": "Tactical Crossbow",
            "armor_set": "Marksman's Leather",
            "talismans": ["Precision Shot", "Marking Mastery", "Range Boost"],
            "recommended_stats": {"Dexterity": 15, "Vigor": 10, "Endurance": 10, "Mind": 10},
            "strategy": "Mark enemies for team damage, maintain distance",
            "best_for": ["Ironeye"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ironeye Support",
            "character": "Ironeye",
            "type": "Support",
            "description": "Support build focusing on team buffs and revival abilities.",
            "primary_weapon": "Support Bow",
            "secondary_weapon": "Healing Crossbow",
            "armor_set": "Support Leather",
            "talismans": ["Team Support", "Revival Mastery", "Tactical Awareness"],
            "recommended_stats": {"Dexterity": 12, "Vigor": 11, "Endurance": 10, "Mind": 12},
            "strategy": "Support team with marking, revive at distance",
            "best_for": ["Ironeye"]
        },
        # Revenant builds
        {
            "id": str(uuid.uuid4()),
            "name": "Revenant Support",
            "character": "Revenant",
            "type": "Support",
            "description": "Ultimate support build with summoning and invincibility abilities.",
            "primary_weapon": "Support Catalyst",
            "secondary_weapon": "Blessing Focus",
            "armor_set": "Support Robes",
            "talismans": ["Summon Power", "Invincibility Duration", "Team Blessing"],
            "recommended_stats": {"Faith": 15, "Vigor": 10, "Mind": 15, "Endurance": 5},
            "strategy": "Summon allies, provide invincibility to team",
            "best_for": ["Revenant"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Revenant Summoner",
            "character": "Revenant",
            "type": "Summon",
            "description": "Summon-focused build with multiple ally types and enhanced duration.",
            "primary_weapon": "Summon Catalyst",
            "secondary_weapon": "Binding Staff",
            "armor_set": "Summoner's Robes",
            "talismans": ["Multiple Summons", "Duration Boost", "Ally Strength"],
            "recommended_stats": {"Faith": 13, "Vigor": 9, "Mind": 15, "Endurance": 8},
            "strategy": "Summon multiple allies, coordinate attacks",
            "best_for": ["Revenant"]
        }
    ]
    
    # Initialize achievements
    achievements = [
        {
            "id": str(uuid.uuid4()),
            "name": "Nightreign",
            "description": "Unlock all achievements",
            "category": "Master",
            "requirements": "Complete all other achievements",
            "reward": "Master Title",
            "difficulty": "Extreme",
            "percentage": 0.1
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Shrouded Roundtable Hold",
            "description": "Reach the Shrouded Roundtable Hold",
            "category": "Progress",
            "requirements": "Complete first expedition",
            "reward": "Hub Access",
            "difficulty": "Easy",
            "percentage": 95.2
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Nightlords",
            "description": "The Nightlords appear",
            "category": "Story",
            "requirements": "Encounter first Nightlord",
            "reward": "Lore Entry",
            "difficulty": "Easy",
            "percentage": 89.7
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Night Begins",
            "description": "The Night Aspect appears",
            "category": "Story",
            "requirements": "Reach final boss area",
            "reward": "Story Completion",
            "difficulty": "Hard",
            "percentage": 15.3
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dawn",
            "description": "Reach the ending",
            "category": "Completion",
            "requirements": "Defeat Heolstor",
            "reward": "Ending Unlocked",
            "difficulty": "Hard",
            "percentage": 12.8
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nightlord Conqueror",
            "description": "Defeat all Nightlords",
            "category": "Combat",
            "requirements": "Defeat all 8 Nightlords",
            "reward": "Conqueror Title",
            "difficulty": "Very Hard",
            "percentage": 8.4
        },
        {
            "id": str(uuid.uuid4()),
            "name": "A Champion's Path",
            "description": "Defeat the Nightlord using all characters",
            "category": "Challenge",
            "requirements": "Complete expedition with each character",
            "reward": "Champion Title",
            "difficulty": "Extreme",
            "percentage": 2.1
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Beast Slayer",
            "description": "Defeat Gladius, Beast of Night",
            "category": "Boss",
            "requirements": "Defeat Gladius",
            "reward": "Beast Slayer Title",
            "difficulty": "Medium",
            "percentage": 78.5
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fathom Conqueror",
            "description": "Defeat Maris, Fathom of Night",
            "category": "Boss",
            "requirements": "Defeat Maris",
            "reward": "Fathom Conqueror Title",
            "difficulty": "Medium",
            "percentage": 65.2
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wisdom Overcome",
            "description": "Defeat Gnoster, Wisdom of Night",
            "category": "Boss",
            "requirements": "Defeat Gnoster",
            "reward": "Wisdom Overcome Title",
            "difficulty": "Hard",
            "percentage": 52.8
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Baron Defeated",
            "description": "Defeat Adel, Baron of Night",
            "category": "Boss",
            "requirements": "Defeat Adel",
            "reward": "Baron Defeated Title",
            "difficulty": "Hard",
            "percentage": 41.7
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Miasma Cleared",
            "description": "Defeat Caligo, Miasma of Night",
            "category": "Boss",
            "requirements": "Defeat Caligo",
            "reward": "Miasma Cleared Title",
            "difficulty": "Very Hard",
            "percentage": 32.4
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Equilibrium Restored",
            "description": "Defeat Libra, Creature of Night",
            "category": "Boss",
            "requirements": "Defeat Libra",
            "reward": "Equilibrium Restored Title",
            "difficulty": "Very Hard",
            "percentage": 28.9
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Champion Fallen",
            "description": "Defeat Fulghor, Champion of Nightglow",
            "category": "Boss",
            "requirements": "Defeat Fulghor",
            "reward": "Champion Fallen Title",
            "difficulty": "Extreme",
            "percentage": 18.6
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nightlord Vanquished",
            "description": "Defeat Heolstor, the Nightlord",
            "category": "Boss",
            "requirements": "Defeat Heolstor",
            "reward": "Nightlord Vanquished Title",
            "difficulty": "Extreme",
            "percentage": 12.8
        }
    ]
    
    # Initialize walkthroughs
    walkthroughs = [
        {
            "id": str(uuid.uuid4()),
            "character": "Wylder",
            "title": "Wylder's Remembrance Quest",
            "description": "Complete walkthrough for Wylder's remembrance questline",
            "chapters": [
                {
                    "chapter": 3,
                    "title": "Slate Whetstone",
                    "objective": "Locate the Slate Whetstone in a designated mine in Limveld",
                    "steps": [
                        "Travel to the designated mine in Limveld",
                        "Navigate through the mine tunnels",
                        "Defeat the mine guardians",
                        "Locate the Slate Whetstone in the deepest chamber"
                    ],
                    "reward": "Slate Whetstone Relic"
                },
                {
                    "chapter": 5,
                    "title": "Wylder's Chalice",
                    "objective": "Collect three notes near the Visual Codex in Roundtable Hold",
                    "steps": [
                        "Find the first note near the Visual Codex",
                        "Locate the second note in the upper area",
                        "Discover the third note in the lower chambers",
                        "Speak with Iron Menial about the notes",
                        "Converse with Duchess to complete the quest"
                    ],
                    "reward": "Wylder's Chalice"
                },
                {
                    "chapter": 7,
                    "title": "Silver Tear",
                    "objective": "Defeat the Mimic Troll during the Nolkateo Shifting Earth event",
                    "steps": [
                        "Wait for the Nolkateo Shifting Earth event",
                        "Locate the Mimic Troll spawn area",
                        "Engage the Mimic Troll in combat",
                        "Use appropriate strategies to defeat it",
                        "Collect the Silver Tear upon victory"
                    ],
                    "reward": "Silver Tear Relic and Wylder's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Guardian",
            "title": "Guardian's Remembrance Quest",
            "description": "Complete walkthrough for Guardian's remembrance questline",
            "chapters": [
                {
                    "chapter": 4,
                    "title": "Stone Stake",
                    "objective": "Defeat the Cracked Golem in Limveld",
                    "steps": [
                        "Locate the Cracked Golem in Limveld",
                        "Prepare for a challenging battle",
                        "Target the golem's weak points",
                        "Defeat the golem to obtain the Stone Stake"
                    ],
                    "reward": "Stone Stake Relic"
                },
                {
                    "chapter": 6,
                    "title": "Guardian's Chalice",
                    "objective": "Engage with the spectral merchant in Roundtable Hold",
                    "steps": [
                        "Find the spectral merchant in Roundtable Hold",
                        "Initiate conversation with the merchant",
                        "Watch the cutscene",
                        "Defeat the merchant after the cutscene",
                        "Collect the Guardian's Chalice"
                    ],
                    "reward": "Guardian's Chalice"
                },
                {
                    "chapter": 7,
                    "title": "Third Volume",
                    "objective": "Purchase the tome from the Scale-Bearing Merchant",
                    "steps": [
                        "Accumulate 10,000 Runes",
                        "Find the Scale-Bearing Merchant in Limveld",
                        "Purchase the tome for 10,000 Runes",
                        "Obtain the Third Volume"
                    ],
                    "reward": "Third Volume Relic"
                },
                {
                    "chapter": 9,
                    "title": "Witch's Brooch",
                    "objective": "Forgive Recluse in Roundtable Hold",
                    "steps": [
                        "Find Recluse in Roundtable Hold",
                        "Listen to her confession",
                        "Choose to forgive her",
                        "Receive the Witch's Brooch"
                    ],
                    "reward": "Witch's Brooch Relic and Guardian's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Ironeye",
            "title": "Ironeye's Remembrance Quest",
            "description": "Complete walkthrough for Ironeye's remembrance questline",
            "chapters": [
                {
                    "chapter": 4,
                    "title": "Cracked Sealing Wax",
                    "objective": "Defeat the Night Huntsman and deliver the letter",
                    "steps": [
                        "Locate and defeat the Night Huntsman",
                        "Obtain the Traitor's Letter",
                        "Find the Priestess in Roundtable Hold",
                        "Deliver the letter to the Priestess"
                    ],
                    "reward": "Cracked Sealing Wax Relic and Ironeye's Chalice"
                },
                {
                    "chapter": 6,
                    "title": "Edge of Order",
                    "objective": "Defeat the Nightlord Darkdrift Knight",
                    "steps": [
                        "Prepare for the Fulghor boss fight",
                        "Use lightning-based attacks",
                        "Defeat Fulghor, Champion of Nightglow",
                        "Collect the Edge of Order"
                    ],
                    "reward": "Edge of Order Relic"
                },
                {
                    "chapter": 7,
                    "title": "Ironeye's Remembrance Skin",
                    "objective": "Defeat Heolstor and make the final choice",
                    "steps": [
                        "Defeat the final Nightlord, Heolstor",
                        "Return to Roundtable Hold",
                        "Choose to 'Clench dagger' when prompted",
                        "Obtain the remembrance skin"
                    ],
                    "reward": "Ironeye's Remembrance skin"
                }
            ]
        }
    ]
    
    # Clear existing data and insert new
    bosses_collection.delete_many({})
    characters_collection.delete_many({})
    builds_collection.delete_many({})
    achievements_collection.delete_many({})
    walkthroughs_collection.delete_many({})
    user_ratings_collection.delete_many({})
    custom_builds_collection.delete_many({})
    
    bosses_collection.insert_many(bosses)
    characters_collection.insert_many(characters)
    builds_collection.insert_many(builds)
    achievements_collection.insert_many(achievements)
    walkthroughs_collection.insert_many(walkthroughs)
    
    # Create text indices for search
    bosses_collection.create_index([("name", "text"), ("description", "text")])
    characters_collection.create_index([("name", "text"), ("description", "text")])
    builds_collection.create_index([("name", "text"), ("description", "text")])
    achievements_collection.create_index([("name", "text"), ("description", "text")])

# Initialize data on startup
initialize_data()

@app.get("/")
async def root():
    return {"message": "Elden Ring Nightreign Boss Guide API", "version": "2.0"}

@app.get("/api/bosses")
async def get_bosses():
    bosses = list(bosses_collection.find({}, {"_id": 0}))
    return {"bosses": bosses}

@app.get("/api/bosses/{boss_id}")
async def get_boss(boss_id: str):
    boss = bosses_collection.find_one({"id": boss_id}, {"_id": 0})
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")
    return boss

@app.get("/api/characters")
async def get_characters():
    characters = list(characters_collection.find({}, {"_id": 0}))
    return {"characters": characters}

@app.get("/api/characters/{character_id}")
async def get_character(character_id: str):
    character = characters_collection.find_one({"id": character_id}, {"_id": 0})
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.get("/api/builds")
async def get_builds():
    builds = list(builds_collection.find({}, {"_id": 0}))
    return {"builds": builds}

@app.get("/api/builds/{build_id}")
async def get_build(build_id: str):
    build = builds_collection.find_one({"id": build_id}, {"_id": 0})
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build

@app.get("/api/achievements")
async def get_achievements():
    achievements = list(achievements_collection.find({}, {"_id": 0}))
    return {"achievements": achievements}

@app.get("/api/walkthroughs")
async def get_walkthroughs():
    walkthroughs = list(walkthroughs_collection.find({}, {"_id": 0}))
    return {"walkthroughs": walkthroughs}

@app.get("/api/walkthroughs/{character_name}")
async def get_walkthrough(character_name: str):
    walkthrough = walkthroughs_collection.find_one({"character": character_name}, {"_id": 0})
    if not walkthrough:
        raise HTTPException(status_code=404, detail="Walkthrough not found")
    return walkthrough

@app.get("/api/search")
async def search(query: str):
    try:
        # Search across bosses, characters, builds, and achievements
        boss_results = list(bosses_collection.find(
            {"$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"weaknesses": {"$regex": query, "$options": "i"}},
                {"damage_types": {"$regex": query, "$options": "i"}}
            ]}, 
            {"_id": 0}
        ))
        
        character_results = list(characters_collection.find(
            {"$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"abilities": {"$regex": query, "$options": "i"}},
                {"playstyle": {"$regex": query, "$options": "i"}}
            ]}, 
            {"_id": 0}
        ))
        
        build_results = list(builds_collection.find(
            {"$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"character": {"$regex": query, "$options": "i"}},
                {"type": {"$regex": query, "$options": "i"}}
            ]}, 
            {"_id": 0}
        ))
        
        achievement_results = list(achievements_collection.find(
            {"$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]}, 
            {"_id": 0}
        ))
        
        return {
            "query": query,
            "bosses": boss_results,
            "characters": character_results,
            "builds": build_results,
            "achievements": achievement_results,
            "total_results": len(boss_results) + len(character_results) + len(build_results) + len(achievement_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/boss-recommendations/{boss_id}")
async def get_boss_recommendations(boss_id: str):
    boss = bosses_collection.find_one({"id": boss_id}, {"_id": 0})
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")
    
    # Get recommended characters
    recommended_characters = list(characters_collection.find(
        {"name": {"$in": boss["recommended_team"]}},
        {"_id": 0}
    ))
    
    # Get recommended builds
    recommended_builds = list(builds_collection.find(
        {"name": {"$in": boss["recommended_builds"]}},
        {"_id": 0}
    ))
    
    return {
        "boss": boss,
        "recommended_characters": recommended_characters,
        "recommended_builds": recommended_builds
    }

@app.post("/api/rate-boss")
async def rate_boss(boss_id: str, rating: int, user_id: str = "anonymous"):
    if rating < 1 or rating > 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    
    # Check if boss exists
    boss = bosses_collection.find_one({"id": boss_id}, {"_id": 0})
    if not boss:
        raise HTTPException(status_code=404, detail="Boss not found")
    
    # Insert or update rating
    user_ratings_collection.update_one(
        {"user_id": user_id, "boss_id": boss_id},
        {"$set": {"rating": rating, "timestamp": datetime.now()}},
        upsert=True
    )
    
    # Calculate average rating
    ratings = list(user_ratings_collection.find({"boss_id": boss_id}))
    avg_rating = sum(r["rating"] for r in ratings) / len(ratings)
    
    return {
        "message": "Rating submitted successfully",
        "average_rating": round(avg_rating, 1),
        "total_ratings": len(ratings)
    }

@app.post("/api/custom-build")
async def create_custom_build(build_data: dict):
    build_data["id"] = str(uuid.uuid4())
    build_data["created_at"] = datetime.now()
    build_data["user_id"] = build_data.get("user_id", "anonymous")
    
    custom_builds_collection.insert_one(build_data)
    
    return {"message": "Custom build created successfully", "build_id": build_data["id"]}

@app.get("/api/custom-builds")
async def get_custom_builds():
    builds = list(custom_builds_collection.find({}, {"_id": 0}))
    return {"custom_builds": builds}

@app.get("/api/filter-bosses")
async def filter_bosses(
    difficulty: Optional[str] = None,
    weakness: Optional[str] = None,
    min_level: Optional[int] = None,
    max_level: Optional[int] = None
):
    filter_criteria = {}
    
    if difficulty:
        if difficulty == "easy":
            filter_criteria["difficulty_rating"] = {"$lte": 4}
        elif difficulty == "medium":
            filter_criteria["difficulty_rating"] = {"$gte": 5, "$lte": 6}
        elif difficulty == "hard":
            filter_criteria["difficulty_rating"] = {"$gte": 7, "$lte": 8}
        elif difficulty == "extreme":
            filter_criteria["difficulty_rating"] = {"$gte": 9}
    
    if weakness:
        filter_criteria["weaknesses"] = {"$in": [weakness]}
    
    if min_level is not None:
        filter_criteria["min_level"] = {"$gte": min_level}
    
    if max_level is not None:
        filter_criteria["max_level"] = {"$lte": max_level}
    
    bosses = list(bosses_collection.find(filter_criteria, {"_id": 0}))
    return {"bosses": bosses, "filters_applied": filter_criteria}

@app.get("/api/filter-characters")
async def filter_characters(
    playstyle: Optional[str] = None,
    primary_stat: Optional[str] = None
):
    filter_criteria = {}
    
    if playstyle:
        filter_criteria["playstyle"] = {"$regex": playstyle, "$options": "i"}
    
    if primary_stat:
        filter_criteria["primary_stat"] = {"$regex": primary_stat, "$options": "i"}
    
    characters = list(characters_collection.find(filter_criteria, {"_id": 0}))
    return {"characters": characters, "filters_applied": filter_criteria}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)