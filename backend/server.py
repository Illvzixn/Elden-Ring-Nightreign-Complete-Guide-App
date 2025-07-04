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
creatures_collection = db.creatures
secrets_collection = db.secrets
weapon_skills_collection = db.weapon_skills
weapon_passives_collection = db.weapon_passives

# Sample data initialization
def initialize_data():
    # Initialize all 8 Nightlords with corrected level ranges (max 15)
    bosses = [
        {
            "id": str(uuid.uuid4()),
            "name": "Gladius, Beast of Night",
            "expedition_name": "Tricephalos",
            "description": "The initial Nightlord that players encounter. A monstrous three-headed wolf resembling a cerberus.",
            "weaknesses": ["Holy"],
            "damage_types": ["Physical", "Fire"],
            "difficulty_rating": 3,
            "min_level": 1,
            "max_level": 5,
            "recommended_strategies": [
                "Use holy damage attacks to exploit weaknesses",
                "Focus on dodging its charging attacks",
                "Attack after it completes its combo sequences",
                "Watch for when it splits into three beasts"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Wylder", "Guardian", "Ironeye"],
            "recommended_builds": ["Wylder Versatile", "Guardian Tank", "Ironeye Marksman"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Maris, Fathom of Night",
            "expedition_name": "Augur",
            "description": "An enigmatic aquatic creature that fills the battlefield with explosive jellyfish and hostile hydras.",
            "weaknesses": ["Lightning"],
            "damage_types": ["Water", "Sleep"],
            "difficulty_rating": 5,
            "min_level": 3,
            "max_level": 7,
            "recommended_strategies": [
                "Utilize lightning attacks to exploit weaknesses",
                "Stay mobile to avoid water-based area attacks",
                "Watch for sleep-inducing attacks",
                "Clear jellyfish before focusing on boss"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Ironeye", "Recluse", "Duchess"],
            "recommended_builds": ["Ironeye Marksman", "Recluse Spellcaster", "Duchess Shadow"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gnoster, Wisdom of Night",
            "expedition_name": "Sentient Pest",
            "description": "Two gigantic insects acting as one entity - a massive moth and a colossal arachnid.",
            "weaknesses": ["Fire"],
            "damage_types": ["Magic", "Poison"],
            "difficulty_rating": 6,
            "min_level": 5,
            "max_level": 9,
            "recommended_strategies": [
                "Use fire attacks to counter its abilities",
                "Focus on one insect at a time",
                "Avoid poisonous clouds from the moth",
                "Watch for underground attacks from the arachnid"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Executor", "Wylder"],
            "recommended_builds": ["Recluse Spellcaster", "Executor Duelist", "Wylder Versatile"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Adel, Baron of Night",
            "expedition_name": "Gaping Jaw",
            "description": "A colossal draconic entity with a grotesquely twisted mouth that can seize and chew players.",
            "weaknesses": ["Poison"],
            "damage_types": ["Lightning", "Physical"],
            "difficulty_rating": 7,
            "min_level": 7,
            "max_level": 11,
            "recommended_strategies": [
                "Use poison attacks but beware of vomit purge",
                "Attack from the sides to avoid jaw attacks",
                "Dodge seismic shocks and lightning explosions",
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
            "min_level": 9,
            "max_level": 13,
            "recommended_strategies": [
                "Use fire attacks to clear fog",
                "Stay grouped to avoid getting separated",
                "Use area-of-effect abilities",
                "Coordinate team positioning"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Raider", "Revenant"],
            "recommended_builds": ["Recluse Spellcaster", "Raider Berserker", "Revenant Support"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Libra, Creature of Night",
            "expedition_name": "Equilibrious Beast",
            "description": "A demon with goat-like head that offers deals before combat and uses alchemy to produce false gold.",
            "weaknesses": ["Madness", "Fire"],
            "damage_types": ["Madness", "Alchemical"],
            "difficulty_rating": 7,
            "min_level": 10,
            "max_level": 14,
            "recommended_strategies": [
                "Consider the pre-combat deal carefully",
                "Use madness-inducing attacks",
                "Avoid false gold to prevent madness buildup",
                "Interrupt alchemical processes"
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
            "min_level": 12,
            "max_level": 15,
            "recommended_strategies": [
                "Use lightning attacks for maximum damage",
                "Master precise dodging and timing",
                "Use defensive abilities to survive combos",
                "Coordinate team attacks during openings"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils", "Edge of Order"],
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
            "min_level": 13,
            "max_level": 15,
            "recommended_strategies": [
                "Use holy damage for maximum effectiveness",
                "Master all mechanics from previous bosses",
                "Coordinate team attacks carefully",
                "Prepare for phase transitions and pattern changes"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils", "Nightlord Crown"],
            "recommended_team": ["All characters viable", "Team composition crucial"],
            "recommended_builds": ["All builds viable", "Master level required"]
        }
    ]
    
    # Initialize characters with corrected max level (15)
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
    
    # Initialize character-specific builds (removing test builds)
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
            "recommended_stats": {"Strength": 8, "Dexterity": 8, "Vigor": 10, "Mind": 6},
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
            "recommended_stats": {"Strength": 9, "Dexterity": 9, "Vigor": 9, "Mind": 8},
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
            "recommended_stats": {"Strength": 12, "Vigor": 10, "Endurance": 10, "Mind": 3},
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
            "recommended_stats": {"Strength": 10, "Vigor": 12, "Endurance": 10, "Mind": 3},
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
            "recommended_stats": {"Dexterity": 12, "Vigor": 8, "Endurance": 9, "Arcane": 6},
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
            "recommended_stats": {"Dexterity": 10, "Vigor": 9, "Endurance": 8, "Arcane": 8},
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
            "recommended_stats": {"Intelligence": 12, "Vigor": 6, "Mind": 12, "Endurance": 5},
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
            "recommended_stats": {"Intelligence": 10, "Vigor": 8, "Mind": 10, "Endurance": 7},
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
            "recommended_stats": {"Strength": 10, "Vigor": 12, "Endurance": 10, "Mind": 3},
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
            "recommended_stats": {"Strength": 8, "Vigor": 10, "Endurance": 9, "Mind": 8},
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
            "recommended_stats": {"Dexterity": 12, "Vigor": 8, "Endurance": 10, "Mind": 5},
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
            "recommended_stats": {"Dexterity": 10, "Vigor": 9, "Endurance": 9, "Mind": 7},
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
            "recommended_stats": {"Dexterity": 12, "Vigor": 8, "Endurance": 8, "Mind": 7},
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
            "recommended_stats": {"Dexterity": 10, "Vigor": 9, "Endurance": 8, "Mind": 8},
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
            "recommended_stats": {"Faith": 12, "Vigor": 8, "Mind": 12, "Endurance": 3},
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
            "recommended_stats": {"Faith": 10, "Vigor": 7, "Mind": 12, "Endurance": 6},
            "strategy": "Summon multiple allies, coordinate attacks",
            "best_for": ["Revenant"]
        }
    ]
    
    # Initialize all 37 achievements properly ranked
    achievements = [
        # Platinum/Master Achievement
        {
            "id": str(uuid.uuid4()),
            "name": "Nightreign",
            "description": "Unlock all achievements",
            "category": "Platinum",
            "requirements": "Complete all other achievements",
            "reward": "Platinum Trophy",
            "difficulty": "Platinum",
            "percentage": 0.1,
            "rank": 1
        },
        # Story Progression Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "The Shrouded Roundtable Hold",
            "description": "Reach the Shrouded Roundtable Hold",
            "category": "Progress",
            "requirements": "Complete first expedition",
            "reward": "Hub Access",
            "difficulty": "Easy",
            "percentage": 95.2,
            "rank": 37
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Night Begins",
            "description": "The Night Aspect appears",
            "category": "Story",
            "requirements": "Reach final boss area",
            "reward": "Story Completion",
            "difficulty": "Hard",
            "percentage": 15.3,
            "rank": 10
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dawn",
            "description": "Reach the ending",
            "category": "Completion",
            "requirements": "Defeat Heolstor",
            "reward": "Ending Unlocked",
            "difficulty": "Hard",
            "percentage": 12.8,
            "rank": 7
        },
        # Equipment and Power Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "Relic",
            "description": "Invoke the power of a relic for the first time",
            "category": "Equipment",
            "requirements": "Use any relic",
            "reward": "Relic Mastery",
            "difficulty": "Easy",
            "percentage": 89.5,
            "rank": 35
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dresser",
            "description": "Change garb via the dresser for the first time",
            "category": "Customization",
            "requirements": "Use dresser to change appearance",
            "reward": "Style Points",
            "difficulty": "Easy",
            "percentage": 85.7,
            "rank": 34
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Vessel",
            "description": "Acquire a new vessel and conduct a different relic rite for the first time",
            "category": "Equipment",
            "requirements": "Get new vessel and perform rite",
            "reward": "Vessel Mastery",
            "difficulty": "Easy",
            "percentage": 78.3,
            "rank": 33
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Replenished Sacred Flasks",
            "description": "Acquire a great number of flask charges",
            "category": "Progression",
            "requirements": "Maximize flask charges",
            "reward": "Flask Mastery",
            "difficulty": "Medium",
            "percentage": 45.8,
            "rank": 25
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Legendary Armament",
            "description": "Acquire a legendary armament for the first time",
            "category": "Equipment",
            "requirements": "Obtain legendary weapon",
            "reward": "Legendary Weapon",
            "difficulty": "Medium",
            "percentage": 42.1,
            "rank": 24
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Obtained Vessels",
            "description": "Acquire a great many vessels",
            "category": "Collection",
            "requirements": "Collect multiple vessels",
            "reward": "Vessel Collection",
            "difficulty": "Medium",
            "percentage": 38.6,
            "rank": 23
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mastery",
            "description": "Attain maximum level",
            "category": "Character",
            "requirements": "Reach level 15",
            "reward": "Master Title",
            "difficulty": "Hard",
            "percentage": 25.4,
            "rank": 14
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Set and Steadfast",
            "description": "Acquire many pieces of high-rarity equipment on a single expedition",
            "category": "Equipment",
            "requirements": "Get multiple rare items in one run",
            "reward": "Collector Title",
            "difficulty": "Hard",
            "percentage": 18.7,
            "rank": 12
        },
        # Character Unlock Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "The Duchess Joins the Fray",
            "description": "Unlock The Duchess as a playable character",
            "category": "Character",
            "requirements": "Complete Duchess unlock requirements",
            "reward": "Duchess Character",
            "difficulty": "Medium",
            "percentage": 67.4,
            "rank": 30
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Revenant Joins the Fray",
            "description": "Unlock The Revenant as a playable character",
            "category": "Character",
            "requirements": "Complete Revenant unlock requirements",
            "reward": "Revenant Character",
            "difficulty": "Medium",
            "percentage": 58.9,
            "rank": 28
        },
        # Boss Defeat Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "Tricephalos",
            "description": "Defeat Gladius, Beast of Night",
            "category": "Boss",
            "requirements": "Defeat Gladius",
            "reward": "Beast Slayer Title",
            "difficulty": "Easy",
            "percentage": 78.5,
            "rank": 32
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Augur",
            "description": "Defeat Maris, Fathom of Night",
            "category": "Boss",
            "requirements": "Defeat Maris",
            "reward": "Fathom Conqueror Title",
            "difficulty": "Medium",
            "percentage": 65.2,
            "rank": 29
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Sentient Pest",
            "description": "Defeat Gnoster, Wisdom of Night",
            "category": "Boss",
            "requirements": "Defeat Gnoster",
            "reward": "Wisdom Overcome Title",
            "difficulty": "Medium",
            "percentage": 52.8,
            "rank": 27
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gaping Jaw",
            "description": "Defeat Adel, Baron of Night",
            "category": "Boss",
            "requirements": "Defeat Adel",
            "reward": "Baron Defeated Title",
            "difficulty": "Hard",
            "percentage": 41.7,
            "rank": 22
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fissure in the Fog",
            "description": "Defeat Caligo, Miasma of Night",
            "category": "Boss",
            "requirements": "Defeat Caligo",
            "reward": "Miasma Cleared Title",
            "difficulty": "Hard",
            "percentage": 32.4,
            "rank": 19
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Equilibrious Beast",
            "description": "Defeat Libra, Creature of Night",
            "category": "Boss",
            "requirements": "Defeat Libra",
            "reward": "Equilibrium Restored Title",
            "difficulty": "Hard",
            "percentage": 28.9,
            "rank": 17
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Darkdrift Knight",
            "description": "Defeat Fulghor, Champion of Nightglow",
            "category": "Boss",
            "requirements": "Defeat Fulghor",
            "reward": "Champion Fallen Title",
            "difficulty": "Very Hard",
            "percentage": 18.6,
            "rank": 11
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Night Aspect",
            "description": "Defeat Heolstor, the Nightlord",
            "category": "Boss",
            "requirements": "Defeat Heolstor",
            "reward": "Nightlord Vanquished Title",
            "difficulty": "Very Hard",
            "percentage": 12.8,
            "rank": 6
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nightlord Conqueror",
            "description": "Defeat all Nightlords",
            "category": "Combat",
            "requirements": "Defeat all 8 Nightlords",
            "reward": "Conqueror Title",
            "difficulty": "Very Hard",
            "percentage": 8.4,
            "rank": 4
        },
        # Combat Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "Untold Power",
            "description": "Defeat 10 or more great enemies on one expedition",
            "category": "Combat",
            "requirements": "Kill 10+ great enemies in single run",
            "reward": "Power Title",
            "difficulty": "Medium",
            "percentage": 49.2,
            "rank": 26
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nightlord Slayer",
            "description": "Defeat three different Nightlords in a row",
            "category": "Combat",
            "requirements": "Beat 3 Nightlords consecutively",
            "reward": "Slayer Title",
            "difficulty": "Very Hard",
            "percentage": 15.7,
            "rank": 9
        },
        # Exploration Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "Mountaintop",
            "description": "Find the secret of the Mountaintop",
            "category": "Exploration",
            "requirements": "Discover Mountaintop secret",
            "reward": "Explorer Title",
            "difficulty": "Medium",
            "percentage": 36.8,
            "rank": 21
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Crater",
            "description": "Find the secret of the Crater",
            "category": "Exploration",
            "requirements": "Discover Crater secret",
            "reward": "Crater Explorer",
            "difficulty": "Medium",
            "percentage": 34.5,
            "rank": 20
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Rotted Woods",
            "description": "Find the secret of the Rotted Woods",
            "category": "Exploration",
            "requirements": "Discover Rotted Woods secret",
            "reward": "Woods Explorer",
            "difficulty": "Hard",
            "percentage": 29.7,
            "rank": 18
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Noklateo, the Shrouded City",
            "description": "Find the secret of Noklateo, the Shrouded City",
            "category": "Exploration",
            "requirements": "Discover Noklateo secret",
            "reward": "City Explorer",
            "difficulty": "Hard",
            "percentage": 26.3,
            "rank": 16
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Shifting Earth",
            "description": "Find the secrets of all Shifting Earth locations",
            "category": "Exploration",
            "requirements": "Discover all Shifting Earth secrets",
            "reward": "Earth Master",
            "difficulty": "Hard",
            "percentage": 22.1,
            "rank": 13
        },
        # Raid Achievements
        {
            "id": str(uuid.uuid4()),
            "name": "Fell Omen",
            "description": "Complete the Fell Omen raid",
            "category": "Raid",
            "requirements": "Complete Fell Omen raid",
            "reward": "Omen Conqueror",
            "difficulty": "Very Hard",
            "percentage": 16.8,
            "rank": 8
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Plague of Locusts",
            "description": "Complete the Sentient Pest raid",
            "category": "Raid",
            "requirements": "Complete Sentient Pest raid",
            "reward": "Pest Controller",
            "difficulty": "Hard",
            "percentage": 27.4,
            "rank": 15
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Typhoon",
            "description": "Complete the Augur raid",
            "category": "Raid",
            "requirements": "Complete Augur raid",
            "reward": "Storm Master",
            "difficulty": "Hard",
            "percentage": 31.2,
            "rank": 31
        },
        {
            "id": str(uuid.uuid4()),
            "name": "True Arbiter",
            "description": "Complete the Equilibrious Beast raid",
            "category": "Raid",
            "requirements": "Complete Equilibrious Beast raid",
            "reward": "True Arbiter Title",
            "difficulty": "Very Hard",
            "percentage": 19.5,
            "rank": 5
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Old Gaol",
            "description": "Complete the oldest gaol",
            "category": "Raid",
            "requirements": "Complete oldest gaol",
            "reward": "Gaol Breaker",
            "difficulty": "Very Hard",
            "percentage": 14.3,
            "rank": 3
        },
        # Challenge Achievement
        {
            "id": str(uuid.uuid4()),
            "name": "A Champion's Path",
            "description": "Defeat the Nightlord using all characters",
            "category": "Challenge",
            "requirements": "Complete expedition with each character",
            "reward": "Champion Title",
            "difficulty": "Extreme",
            "percentage": 2.1,
            "rank": 2
        },
        # Additional Equipment Achievement
        {
            "id": str(uuid.uuid4()),
            "name": "Master of Arms",
            "description": "Acquire all weapon types",
            "category": "Equipment",
            "requirements": "Collect all weapon categories",
            "reward": "Weapon Master Title",
            "difficulty": "Easy",
            "percentage": 72.6,
            "rank": 36
        }
    ]
    
    # Initialize all character walkthroughs (8 total)
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
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Duchess",
            "title": "Duchess's Remembrance Quest",
            "description": "Complete walkthrough for Duchess's remembrance questline",
            "chapters": [
                {
                    "chapter": 3,
                    "title": "Golden Dew",
                    "objective": "Find the Golden Dew in Limveld",
                    "steps": [
                        "During an expedition, locate the Golden Dew in the southern region of Limveld",
                        "Collecting it completes this chapter"
                    ],
                    "reward": "Golden Dew Relic"
                },
                {
                    "chapter": 5,
                    "title": "Wylder's Offering",
                    "objective": "Interact with Wylder and Iron Menial in Roundtable Hold",
                    "steps": [
                        "Find Wylder sitting against a wall in the western part of Roundtable Hold",
                        "Examine the plate of Pita Bread beside him and choose to eat it",
                        "Initiate conversation with Wylder",
                        "Speak with Iron Menial in the dressing room about the Pita Bread"
                    ],
                    "reward": "Duchess's Chalice"
                },
                {
                    "chapter": 6,
                    "title": "Weathervane's Words",
                    "objective": "Speak to Raider, obtain Weathervane's Words from Limveld, and duel Revenant",
                    "steps": [
                        "Talk to Raider in the dining room of Roundtable Hold",
                        "Choose the dialogue option 'Maybe we shouldn't defeat the Nightlord' and then 'Explain'",
                        "Embark on an expedition to Limveld and head to the northeastern part of the map",
                        "Defeat the Fallen Mercenaries guarding the area",
                        "Examine the tombstone to acquire Weathervane's Words",
                        "Return to Raider, then proceed to the southeastern beach to duel Revenant"
                    ],
                    "reward": "Crown Medal Relic"
                },
                {
                    "chapter": 8,
                    "title": "Blessing the Iron Coin",
                    "objective": "Bless the Iron Coin, give it to Iron Menial, speak to Wylder, then return to Iron Menial",
                    "steps": [
                        "Bless the Iron Coin during an expedition",
                        "Give the blessed coin to Iron Menial in Roundtable Hold",
                        "Speak to Wylder about the coin",
                        "Return to Iron Menial to conclude the quest"
                    ],
                    "reward": "Blessed Iron Coin Relic and Duchess's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Raider",
            "title": "Raider's Remembrance Quest",
            "description": "Complete walkthrough for Raider's remembrance questline",
            "chapters": [
                {
                    "chapter": 2,
                    "title": "Torn Braided Cord",
                    "objective": "Defeat the Onestrike Gladiator and obtain the Torn Braided Cord",
                    "steps": [
                        "Engage and defeat the Onestrike Gladiator in the Tournament Arena",
                        "Loot the Torn Braided Cord from the fallen enemy",
                        "Show the cord to Iron Menial in Roundtable Hold"
                    ],
                    "reward": "Torn Braided Cord Relic"
                },
                {
                    "chapter": 4,
                    "title": "Blinding Elder Lion",
                    "objective": "Defeat the Blinding Elder Lion",
                    "steps": [
                        "Locate and defeat the Blinding Elder Lion in the Tournament Arena",
                        "After the battle, speak with Iron Menial"
                    ],
                    "reward": "Raider's Chalice"
                },
                {
                    "chapter": 7,
                    "title": "White Horn",
                    "objective": "Defeat White Horn",
                    "steps": [
                        "Engage and defeat White Horn in the Tournament Arena",
                        "Conclude the quest by speaking with Iron Menial"
                    ],
                    "reward": "Black Claw Necklace Relic and Raider's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Revenant",
            "title": "Revenant's Remembrance Quest",
            "description": "Complete walkthrough for Revenant's remembrance questline",
            "chapters": [
                {
                    "chapter": 1,
                    "title": "Nightlord Confrontation",
                    "objective": "Defeat either Nightlord Gladius or Nightlord Darkdrift Knight",
                    "steps": [
                        "Choose and defeat one of the Nightlords during an expedition"
                    ],
                    "reward": "Small Makeup Brush Relic"
                },
                {
                    "chapter": 5,
                    "title": "Corrosion's Demise",
                    "objective": "Speak to Duchess and Recluse, then defeat Corrosion",
                    "steps": [
                        "In Roundtable Hold, talk to Duchess and Recluse",
                        "Embark on an expedition to confront and defeat Corrosion"
                    ],
                    "reward": "Revenant's Chalice"
                },
                {
                    "chapter": 7,
                    "title": "Contaminant's End",
                    "objective": "Speak to Recluse, then defeat Contaminant",
                    "steps": [
                        "In Roundtable Hold, speak to Recluse and sit on the wooden bench to trigger a memory",
                        "Examine the blood-covered painting",
                        "Enter the adjacent room to face Contaminant",
                        "Utilize summons like Frederick, Sebastian, and Helen to assist in the battle"
                    ],
                    "reward": "Old Portrait Relic and Revenant's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Recluse",
            "title": "Recluse's Remembrance Quest",
            "description": "Complete walkthrough for Recluse's remembrance questline",
            "chapters": [
                {
                    "chapter": 2,
                    "title": "Night-Swallowed Golden Hippopotamus",
                    "objective": "Defeat the Night-Swallowed Golden Hippopotamus",
                    "steps": [
                        "Locate and defeat the Night-Swallowed Golden Hippopotamus in northeastern Limveld"
                    ],
                    "reward": "Recluse's Chalice"
                },
                {
                    "chapter": 4,
                    "title": "Vestige of Night",
                    "objective": "Retrieve the Vestige of Night from Iron Menial",
                    "steps": [
                        "Speak with Iron Menial in Roundtable Hold to obtain the Vestige of Night"
                    ],
                    "reward": "Vestige of Night Relic"
                },
                {
                    "chapter": 6,
                    "title": "Confronting Iron Menial",
                    "objective": "'Kill' Iron Menial, interact with NPCs, and defeat Nightlord Heolstor",
                    "steps": [
                        "Attempt to speak with Iron Menial; when unsuccessful, 'kill' him",
                        "Interact with various NPCs in Roundtable Hold to receive the Bone-Like Stone Relic",
                        "Defeat Nightlord Heolstor to trigger an alternative ending"
                    ],
                    "reward": "Bone-Like Stone Relic and Recluse's Remembrance skin"
                }
            ]
        },
        {
            "id": str(uuid.uuid4()),
            "character": "Executor",
            "title": "Executor's Remembrance Quest",
            "description": "Complete walkthrough for Executor's remembrance questline",
            "chapters": [
                {
                    "chapter": 2,
                    "title": "Blessed Flowers",
                    "objective": "Find the Blessed Flowers in Limveld",
                    "steps": [
                        "During an expedition, head to the northeastern gully in Limveld",
                        "Defeat the Stray Bloodhound Knight to obtain the Blessed Flowers",
                        "Return to Roundtable Hold and give the flowers to Iron Menial in the garden"
                    ],
                    "reward": "Executor's Chalice and Blessed Flowers Relic"
                },
                {
                    "chapter": 6,
                    "title": "Golden Sprout",
                    "objective": "Find the Golden Sprout in Limveld and defeat Executor's Cry",
                    "steps": [
                        "During an expedition, locate the Golden Sprout in Limveld after defeating the Erdtree Avatar",
                        "Return to Roundtable Hold; you'll be teleported to face Executor's Cry",
                        "Defeat Executor's Cry, then proceed to the shack to watch the final scene"
                    ],
                    "reward": "Golden Sprout Relic and Executor's Remembrance skin"
                }
            ]
        }
    ]
    
    # Initialize creatures and enemies database
    creatures = [
        {
            "id": str(uuid.uuid4()),
            "name": "Gladius, Beast of Night",
            "type": "Nightlord",
            "description": "A monstrous three-headed wolf resembling a cerberus, capable of splitting into three individual beasts",
            "location": "Tricephalos Expedition",
            "weaknesses": ["Holy"],
            "resistances": ["Dark", "Physical"],
            "damage_types": ["Fire", "Physical"],
            "threat_level": "Extreme",
            "notes": "Can split into three beasts and reunite at will. Wields chain-bound sword as projectile."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Maris, Fathom of Night",
            "type": "Nightlord",
            "description": "An enigmatic aquatic creature resembling a cnidarian with jellyfish and hydra summons",
            "location": "Augur Expedition",
            "weaknesses": ["Lightning"],
            "resistances": ["Water", "Sleep"],
            "damage_types": ["Water", "Sleep"],
            "threat_level": "Extreme",
            "notes": "Fills battlefield with explosive jellyfish and hostile hydras. Inflicts Sleep status."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gnoster, Wisdom of Night",
            "type": "Nightlord",
            "description": "Two gigantic insects acting as one entity - a massive moth and colossal arachnid",
            "location": "Sentient Pest Expedition",
            "weaknesses": ["Fire"],
            "resistances": ["Magic", "Poison"],
            "damage_types": ["Magic", "Poison"],
            "threat_level": "Extreme",
            "notes": "Moth unleashes magical attacks and poisonous clouds. Arachnid has subterranean mobility."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Adel, Baron of Night",
            "type": "Nightlord",
            "description": "A colossal draconic entity with a grotesquely twisted mouth",
            "location": "Gaping Jaw Expedition",
            "weaknesses": ["Poison"],
            "resistances": ["Lightning", "Physical"],
            "damage_types": ["Lightning", "Physical"],
            "threat_level": "Extreme",
            "notes": "Can seize and chew players. Causes seismic shocks and lightning explosions. Purges poison by vomiting."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Caligo, Miasma of Night",
            "type": "Nightlord",
            "description": "A fog-based Nightlord that creates battlefield confusion",
            "location": "Fissure in the Fog Expedition",
            "weaknesses": ["Fire"],
            "resistances": ["Fog", "Dark"],
            "damage_types": ["Fog", "Fire"],
            "threat_level": "Extreme",
            "notes": "Creates dense fog to separate and confuse players."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Libra, Creature of Night",
            "type": "Nightlord",
            "description": "A demon with goat-like head and multiple eyes, reminiscent of Baphomet",
            "location": "Equilibrious Beast Expedition",
            "weaknesses": ["Madness", "Fire"],
            "resistances": ["Alchemical", "Dark"],
            "damage_types": ["Madness", "Alchemical"],
            "threat_level": "Extreme",
            "notes": "Offers deals before combat. Uses alchemy to produce false gold inducing Madness."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fulghor, Champion of Nightglow",
            "type": "Nightlord",
            "description": "Swift and deadly Nightlord with rapid attack patterns",
            "location": "Darkdrift Knight Expedition",
            "weaknesses": ["Lightning"],
            "resistances": ["Dark", "Physical"],
            "damage_types": ["Dark", "Physical"],
            "threat_level": "Extreme",
            "notes": "Most challenging Nightlord with unpredictable movements and powerful attacks."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Heolstor, the Nightlord",
            "type": "Nightlord",
            "description": "The final boss with mastery over all night aspects",
            "location": "Night Aspect Expedition",
            "weaknesses": ["Holy"],
            "resistances": ["All Elements", "Dark"],
            "damage_types": ["Dark", "All Elements"],
            "threat_level": "Ultimate",
            "notes": "Two-phase battle. Ultimate challenge requiring mastery of all game mechanics."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dancer of the Boreal Valley",
            "type": "Elite Enemy",
            "description": "Swift and deadly warrior with unpredictable attack patterns",
            "location": "Night Encounters",
            "weaknesses": ["Lightning", "Frostbite"],
            "resistances": ["Dark", "Cold"],
            "damage_types": ["Dark", "Physical"],
            "threat_level": "High",
            "notes": "Returning enemy from Dark Souls 3 with enhanced mobility."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gaping Dragon",
            "type": "Elite Enemy",
            "description": "Grotesque, massive creature with acid-based attacks",
            "location": "Various Expeditions",
            "weaknesses": ["Lightning", "Holy"],
            "resistances": ["Acid", "Physical"],
            "damage_types": ["Acid", "Physical"],
            "threat_level": "High",
            "notes": "Coats battlefield in acid, instantly eliminating Spirit Summons."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Centipede Demon",
            "type": "Elite Enemy",
            "description": "Segmented insectoid creature with multiple attack phases",
            "location": "Various Expeditions",
            "weaknesses": ["Fire", "Lightning"],
            "resistances": ["Poison", "Physical"],
            "damage_types": ["Poison", "Physical"],
            "threat_level": "High",
            "notes": "Redesigned for Nightreign's faster-paced combat."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Draconic Tree Sentinel",
            "type": "Elite Enemy",
            "description": "Heavily armored dragon rider with fire-based abilities",
            "location": "Various Expeditions",
            "weaknesses": ["Lightning", "Magic"],
            "resistances": ["Fire", "Physical"],
            "damage_types": ["Fire", "Lightning"],
            "threat_level": "High",
            "notes": "Mounted combat specialist with powerful area attacks."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Morgott, the Fell Omen",
            "type": "Elite Enemy",
            "description": "Cursed omen with golden weapon manifestations",
            "location": "Roaming Enemy",
            "weaknesses": ["Holy", "Fire"],
            "resistances": ["Dark", "Curse"],
            "damage_types": ["Curse", "Physical"],
            "threat_level": "High",
            "notes": "First major boss of Elden Ring returns as roaming enemy."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Duke's Dear Freja",
            "type": "Elite Enemy",
            "description": "Giant two-headed spider surrounded by smaller arachnids",
            "location": "Various Expeditions",
            "weaknesses": ["Fire", "Lightning"],
            "resistances": ["Poison", "Dark"],
            "damage_types": ["Poison", "Physical"],
            "threat_level": "High",
            "notes": "Controls swarms of smaller spiders. Vulnerable when both heads are targeted."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Golden Hippopotamus",
            "type": "Large Enemy",
            "description": "Massive golden beast with powerful bite and charging attacks",
            "location": "Various Expeditions",
            "weaknesses": ["Lightning", "Pierce"],
            "resistances": ["Physical", "Blunt"],
            "damage_types": ["Physical", "Crush"],
            "threat_level": "Medium",
            "notes": "Charges with mouth wide open, slamming everything in its path."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Night-Swallowed Golden Hippopotamus",
            "type": "Large Enemy",
            "description": "Corrupted version of Golden Hippopotamus with dark powers",
            "location": "Northeastern Limveld",
            "weaknesses": ["Holy", "Lightning"],
            "resistances": ["Dark", "Physical"],
            "damage_types": ["Dark", "Physical"],
            "threat_level": "High",
            "notes": "Required for Recluse's remembrance quest. Enhanced with dark abilities."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Royal Cavalryman",
            "type": "Medium Enemy",
            "description": "Elite mounted warrior with spear and shield",
            "location": "Various Expeditions",
            "weaknesses": ["Strike", "Lightning"],
            "resistances": ["Pierce", "Physical"],
            "damage_types": ["Pierce", "Physical"],
            "threat_level": "Medium",
            "notes": "Often encountered in pairs or trios. Highly mobile mounted combat."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Onestrike Gladiator",
            "type": "Medium Enemy",
            "description": "Arena fighter specializing in devastating single attacks",
            "location": "Tournament Arena",
            "weaknesses": ["Magic", "Ranged"],
            "resistances": ["Physical"],
            "damage_types": ["Physical"],
            "threat_level": "Medium",
            "notes": "Required for Raider's remembrance quest. Focuses on powerful single strikes."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Blinding Elder Lion",
            "type": "Medium Enemy",
            "description": "Ancient lion with blinding light attacks",
            "location": "Tournament Arena",
            "weaknesses": ["Dark", "Blind"],
            "resistances": ["Light", "Physical"],
            "damage_types": ["Light", "Physical"],
            "threat_level": "Medium",
            "notes": "Required for Raider's remembrance quest. Uses blinding attacks to disorient."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "White Horn",
            "type": "Medium Enemy",
            "description": "Horned beast with charging and goring attacks",
            "location": "Tournament Arena",
            "weaknesses": ["Fire", "Lightning"],
            "resistances": ["Physical", "Ice"],
            "damage_types": ["Physical", "Ice"],
            "threat_level": "Medium",
            "notes": "Required for Raider's remembrance quest. Powerful charging attacks."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Night Huntsman",
            "type": "Medium Enemy",
            "description": "Stealthy hunter with bow and tracking abilities",
            "location": "Various Expeditions",
            "weaknesses": ["Holy", "Light"],
            "resistances": ["Dark", "Stealth"],
            "damage_types": ["Pierce", "Dark"],
            "threat_level": "Medium",
            "notes": "Required for Ironeye's remembrance quest. Carries the Traitor's Letter."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Stray Bloodhound Knight",
            "type": "Medium Enemy",
            "description": "Wandering knight with bloodhound companion",
            "location": "Northeastern Gully, Limveld",
            "weaknesses": ["Holy", "Fire"],
            "resistances": ["Bleed", "Physical"],
            "damage_types": ["Bleed", "Physical"],
            "threat_level": "Medium",
            "notes": "Required for Executor's remembrance quest. Guards the Blessed Flowers."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Erdtree Avatar",
            "type": "Large Enemy",
            "description": "Guardian of the Erdtree with nature-based attacks",
            "location": "Various Expeditions",
            "weaknesses": ["Fire", "Slash"],
            "resistances": ["Holy", "Nature"],
            "damage_types": ["Holy", "Nature"],
            "threat_level": "High",
            "notes": "Required for Executor's remembrance quest. Guards the Golden Sprout."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cracked Golem",
            "type": "Large Enemy",
            "description": "Ancient stone construct with structural weaknesses",
            "location": "Limveld",
            "weaknesses": ["Strike", "Lightning"],
            "resistances": ["Pierce", "Slash"],
            "damage_types": ["Physical", "Earth"],
            "threat_level": "Medium",
            "notes": "Required for Guardian's remembrance quest. Target weak points for efficiency."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mimic Troll",
            "type": "Large Enemy",
            "description": "Shape-shifting troll that mimics player abilities",
            "location": "Nolkateo Shifting Earth Event",
            "weaknesses": ["Magic", "True Damage"],
            "resistances": ["Mimicry", "Adaptive"],
            "damage_types": ["Variable", "Physical"],
            "threat_level": "High",
            "notes": "Required for Wylder's remembrance quest. Adapts to player tactics."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Corrosion",
            "type": "Elite Enemy",
            "description": "Acidic entity that corrodes equipment and environment",
            "location": "Special Expedition",
            "weaknesses": ["Ice", "Neutralization"],
            "resistances": ["Acid", "Corrosion"],
            "damage_types": ["Acid", "Corrosion"],
            "threat_level": "High",
            "notes": "Required for Revenant's remembrance quest. Degrades equipment over time."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Contaminant",
            "type": "Elite Enemy",
            "description": "Toxic creature that spreads contamination",
            "location": "Special Room, Roundtable Hold",
            "weaknesses": ["Holy", "Purification"],
            "resistances": ["Poison", "Disease"],
            "damage_types": ["Poison", "Disease"],
            "threat_level": "High",
            "notes": "Required for Revenant's remembrance quest. Use summons Frederick, Sebastian, and Helen."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Executor's Cry",
            "type": "Special Enemy",
            "description": "Manifestation of Executor's inner torment",
            "location": "Special Instance",
            "weaknesses": ["Inner Peace", "Acceptance"],
            "resistances": ["Despair", "Guilt"],
            "damage_types": ["Psychic", "Emotional"],
            "threat_level": "High",
            "notes": "Required for Executor's remembrance quest. Psychological battle more than physical."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fallen Mercenaries",
            "type": "Small Enemy",
            "description": "Groups of corrupted mercenaries",
            "location": "Northeastern Limveld",
            "weaknesses": ["Holy", "Fire"],
            "resistances": ["Dark", "Corruption"],
            "damage_types": ["Physical", "Dark"],
            "threat_level": "Low",
            "notes": "Required for Duchess's remembrance quest. Guard Weathervane's Words."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Spectral Merchant",
            "type": "Special Enemy",
            "description": "Ghostly merchant found in Roundtable Hold",
            "location": "Roundtable Hold",
            "weaknesses": ["Holy", "Exorcism"],
            "resistances": ["Physical", "Spectral"],
            "damage_types": ["Spectral", "Curse"],
            "threat_level": "Medium",
            "notes": "Required for Guardian's remembrance quest. Must be defeated after cutscene."
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Scale-Bearing Merchant",
            "type": "NPC Enemy",
            "description": "Merchant selling valuable tomes for high prices",
            "location": "Limveld",
            "weaknesses": ["None"],
            "resistances": ["Economic"],
            "damage_types": ["Economic Drain"],
            "threat_level": "Low",
            "notes": "Required for Guardian's remembrance quest. Sells Third Volume for 10,000 Runes."
        }
    ]
    
    # Initialize secrets
    secrets = [
        {
            "id": str(uuid.uuid4()),
            "name": "Duchess Character Unlock",
            "category": "Character Unlock",
            "description": "Unlock the Duchess character by completing the Tricephalos expedition and obtaining the Old Pocketwatch from Gladius.",
            "location": "Roundtable Hold",
            "how_to_find": "Defeat Gladius in the Tricephalos expedition to obtain the Old Pocketwatch. Show it to the Priestess at the Roundtable Hold.",
            "reward": "Duchess Character",
            "difficulty": "Medium"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Revenant Character Unlock",
            "category": "Character Unlock", 
            "description": "Unlock the Revenant character after unlocking the Duchess. Purchase the Besmirched Frame at the Small Jar Bazaar and defeat the Revenant boss.",
            "location": "Roundtable Hold",
            "how_to_find": "After unlocking the Duchess, buy the Besmirched Frame for 1500 Murk and defeat the Revenant boss at the marked location near the sparring grounds.",
            "reward": "Revenant Character",
            "difficulty": "Hard"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Crater",
            "category": "Location Secret",
            "description": "A giant crater appears in the northern section of the map, allowing players to upgrade weapons to Legendary.",
            "location": "Northern section of the map",
            "how_to_find": "Travel to the eastern side of the map, locate the opening with lava flowing, and defeat the Magma Wyrm in the underground temple.",
            "reward": "Special Smithing Table, Legendary Weapon Upgrades",
            "difficulty": "Hard"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mountaintop",
            "category": "Location Secret",
            "description": "A snowy terrain that grants the Favor of the Mountaintop buff, reducing frostbite damage and boosting attack.",
            "location": "Northwestern section of the map",
            "how_to_find": "Reach the area east of the crevice and use the Spectral Hawk to access the Mountaintop. Interact with blue crystals to gain the buff.",
            "reward": "Favor of the Mountaintop, Dormant Power",
            "difficulty": "Medium"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Rotted Woods",
            "category": "Location Secret",
            "description": "A land ravaged by Scarlet Rot that provides the Favor of the Forest buff, nullifying scarlet rot effects and increasing max HP.",
            "location": "Southeastern region of Limveld",
            "how_to_find": "Travel to the fort in the southwest, interact with the map to reveal the location of the secret, and reach the red flower atop a large tree.",
            "reward": "Favor of the Forest, Max HP Increase",
            "difficulty": "Medium"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Noklateo",
            "category": "Location Secret",
            "description": "A large structure with massive walls that holds the Favor of Noklateo, allowing players to rise from near-death once.",
            "location": "Southwestern region of Limveld", 
            "how_to_find": "Go to the center of Noklateo, defeat the Naturalborn of the Void, and access the small room inside the arena to obtain the favor.",
            "reward": "Favor of Noklateo, Near-death Recovery",
            "difficulty": "Very Hard"
        }
    ]
    
    # Initialize weapon skills
    weapon_skills = [
        {
            "id": str(uuid.uuid4()),
            "name": "Alabaster Lord's Pull",
            "fp_cost": 15,
            "description": "Thrust the armament into the ground to create a gravity well, dealing damage and pulling enemies in.",
            "effect": "Creates gravity well with area damage and enemy pull",
            "usable_with": "Specific armaments",
            "category": "Gravity",
            "damage_type": "Physical + Gravity"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ancient Lightning Spear",
            "fp_cost": 24,
            "description": "Imbue the armament with the ancient dragons' red lightning, then throw it as a spear.",
            "effect": "Ranged lightning spear attack, can be charged for increased power",
            "usable_with": "Specific armaments",
            "category": "Lightning",
            "damage_type": "Lightning"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Angel's Wings",
            "fp_cost": 17,
            "description": "Jump and imbue the wing-blade of the armament with light, then deliver a slashing attack.",
            "effect": "Aerial light-imbued attack that impedes flask recovery",
            "usable_with": "Specific armaments",
            "category": "Holy",
            "damage_type": "Physical + Holy"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Assassin's Gambit",
            "fp_cost": 5,
            "description": "Skill that masks the user's presence at the cost of a self-inflicted wound.",
            "effect": "Near-invisibility and silenced footsteps",
            "usable_with": "Small and medium straight swords, thrusting swords",
            "category": "Stealth",
            "damage_type": "Self-inflicted"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Barbaric Roar",
            "fp_cost": 16,
            "description": "Let loose a bestial roar to rally the spirit and increase attack power.",
            "effect": "Increases attack power, strong attacks become savage combos",
            "usable_with": "Melee armaments (excluding daggers, thrusting swords, and whips)",
            "category": "Buff",
            "damage_type": "Physical Enhancement"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bloodblade Dance",
            "fp_cost": 20,
            "description": "Leap forward and perform a series of spinning blade attacks that build up blood loss.",
            "effect": "Multi-hit spinning attack with blood loss buildup",
            "usable_with": "Curved swords, katanas",
            "category": "Blood",
            "damage_type": "Physical + Bleed"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Carian Grandeur",
            "fp_cost": 26,
            "description": "Imbue the armament with glintstone magic to unleash a powerful magical shockwave.",
            "effect": "Wide-range magical shockwave attack",
            "usable_with": "Swords, greatswords",
            "category": "Magic",
            "damage_type": "Magic"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Flame of the Redmanes",
            "fp_cost": 20,
            "description": "Skill of the Redmane Knights. Create a surge of flames that deals fire damage.",
            "effect": "Fire damage with high stance break potential",
            "usable_with": "Various melee weapons",
            "category": "Fire",
            "damage_type": "Fire"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Hoarfrost Stomp",
            "fp_cost": 10,
            "description": "Stomp hard to create a trail of freezing mist that deals magic damage.",
            "effect": "Creates freezing mist trail with frostbite buildup",
            "usable_with": "Various weapons",
            "category": "Frost",
            "damage_type": "Magic + Frostbite"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Lightning Ram",
            "fp_cost": 18,
            "description": "Surround the armament with lightning and charge forward with tremendous force.",
            "effect": "Lightning-enhanced charge attack",
            "usable_with": "Heavy weapons",
            "category": "Lightning",
            "damage_type": "Physical + Lightning"
        }
    ]
    
    # Initialize weapon passive abilities
    weapon_passives = [
        {
            "id": str(uuid.uuid4()),
            "name": "Add Holy to Weapon",
            "category": "Damage Enhancement",
            "description": "Infuses attacks with additional Holy damage.",
            "effect": "+30 Holy damage to all attacks",
            "compatible_characters": ["Guardian", "Revenant", "Wylder"],
            "weapon_types": ["Swords", "Halberds", "Maces"],
            "scaling": "Faith"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Add Magic to Weapon",
            "category": "Damage Enhancement", 
            "description": "Infuses attacks with additional Magic damage.",
            "effect": "+30 Magic damage to all attacks",
            "compatible_characters": ["Recluse", "Revenant", "Wylder"],
            "weapon_types": ["Staves", "Swords", "Catalysts"],
            "scaling": "Intelligence"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Attack Up when Wielding Two Armaments",
            "category": "Damage Enhancement",
            "description": "Boosts attack power when dual-wielding weapons.",
            "effect": "+7% to +10% attack power with dual weapons",
            "compatible_characters": ["Duchess", "Executor", "Raider"],
            "weapon_types": ["Daggers", "Curved Swords", "Axes"],
            "scaling": "Dexterity/Strength"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Improved Attack Power at Full HP",
            "category": "Conditional Damage",
            "description": "Increases attack power when health is full.",
            "effect": "+7% to +14% attack power at full health",
            "compatible_characters": ["Guardian", "Raider", "Wylder"],
            "weapon_types": ["All weapons"],
            "scaling": "Health dependent"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Improved Attack Power at Low HP",
            "category": "Conditional Damage",
            "description": "Increases attack power when health is low.",
            "effect": "+7% to +21% attack power at low health",
            "compatible_characters": ["Executor", "Duchess", "Ironeye"],
            "weapon_types": ["All weapons"],
            "scaling": "Health dependent"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Attacks Inflict Poison",
            "category": "Status Infliction",
            "description": "Adds poison buildup to attacks.",
            "effect": "+23 poison buildup per attack",
            "compatible_characters": ["Duchess", "Recluse", "Executor"],
            "weapon_types": ["Daggers", "Whips", "Claws"],
            "scaling": "Arcane"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Attacks Inflict Sleep",
            "category": "Status Infliction",
            "description": "Adds sleep buildup to attacks.",
            "effect": "+18 to +30 sleep buildup per attack",
            "compatible_characters": ["Recluse", "Revenant", "Duchess"],
            "weapon_types": ["Staves", "Arrows", "Mist weapons"],
            "scaling": "Intelligence/Arcane"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Continuous HP Recovery",
            "category": "Health Management",
            "description": "Gradually restores health over time.",
            "effect": "+1 HP per second",
            "compatible_characters": ["Guardian", "Revenant", "Wylder"],
            "weapon_types": ["Sacred weapons", "Blessed armaments"],
            "scaling": "Faith"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Defeating Enemies Restores HP",
            "category": "Health Management",
            "description": "Restores health upon defeating enemies.",
            "effect": "+20 HP per enemy defeated",
            "compatible_characters": ["Raider", "Executor", "Guardian"],
            "weapon_types": ["All weapons"],
            "scaling": "Kill dependent"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "HP Restoration Upon Attacks",
            "category": "Health Management",
            "description": "Restores health with each successful attack.",
            "effect": "+3 to +6 HP per successful hit",
            "compatible_characters": ["Executor", "Duchess", "Raider"],
            "weapon_types": ["Fast weapons", "Multi-hit weapons"],
            "scaling": "Hit frequency"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "FP Restoration Upon Attacks",
            "category": "Resource Management",
            "description": "Restores Focus Points with each successful attack.",
            "effect": "+1 to +2 FP per successful hit",
            "compatible_characters": ["Recluse", "Revenant", "Wylder"],
            "weapon_types": ["Caster weapons", "Hybrid weapons"],
            "scaling": "Hit frequency"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Critical Hit HP Restoration",
            "category": "Critical Effects",
            "description": "Restores health upon landing critical hits.",
            "effect": "+10% HP restoration on critical hits",
            "compatible_characters": ["Ironeye", "Executor", "Duchess"],
            "weapon_types": ["Bows", "Daggers", "Rapiers"],
            "scaling": "Critical hit rate"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Critical Hit FP Restoration",
            "category": "Critical Effects",
            "description": "Restores FP upon landing critical hits.",
            "effect": "+10% FP restoration on critical hits",
            "compatible_characters": ["Ironeye", "Recluse", "Executor"],
            "weapon_types": ["Bows", "Staves", "Precision weapons"],
            "scaling": "Critical hit rate"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dmg Negation Up While Casting Spells",
            "category": "Defensive Enhancement",
            "description": "Reduces damage taken while casting spells.",
            "effect": "+24% to +30% damage negation during casting",
            "compatible_characters": ["Recluse", "Revenant"],
            "weapon_types": ["Staves", "Catalysts"],
            "scaling": "Spell usage"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Guard Counters Activate Holy Attacks",
            "category": "Special Effects",
            "description": "Triggers Holy damage upon successful guard counters.",
            "effect": "Holy damage burst on guard counter",
            "compatible_characters": ["Guardian", "Wylder"],
            "weapon_types": ["Shields", "Defensive weapons"],
            "scaling": "Faith"
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
    creatures_collection.delete_many({})
    
    bosses_collection.insert_many(bosses)
    characters_collection.insert_many(characters)
    builds_collection.insert_many(builds)
    achievements_collection.insert_many(achievements)
    walkthroughs_collection.insert_many(walkthroughs)
    creatures_collection.insert_many(creatures)
    
    # Create text indices for search
    bosses_collection.create_index([("name", "text"), ("description", "text")])
    characters_collection.create_index([("name", "text"), ("description", "text")])
    builds_collection.create_index([("name", "text"), ("description", "text")])
    achievements_collection.create_index([("name", "text"), ("description", "text")])
    creatures_collection.create_index([("name", "text"), ("description", "text"), ("type", "text")])

# Initialize data on startup
initialize_data()

@app.get("/")
async def root():
    return {"message": "Elden Ring Nightreign Boss Guide API", "version": "3.0"}

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
    achievements = list(achievements_collection.find({}, {"_id": 0}).sort("rank", 1))
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

@app.get("/api/creatures")
async def get_creatures():
    creatures = list(creatures_collection.find({}, {"_id": 0}))
    return {"creatures": creatures}

@app.get("/api/creatures/{creature_id}")
async def get_creature(creature_id: str):
    creature = creatures_collection.find_one({"id": creature_id}, {"_id": 0})
    if not creature:
        raise HTTPException(status_code=404, detail="Creature not found")
    return creature

@app.get("/api/search")
async def search(query: str):
    try:
        # Search across bosses, characters, builds, achievements, and creatures
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
        
        creature_results = list(creatures_collection.find(
            {"$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"type": {"$regex": query, "$options": "i"}},
                {"location": {"$regex": query, "$options": "i"}},
                {"weaknesses": {"$regex": query, "$options": "i"}}
            ]}, 
            {"_id": 0}
        ))
        
        return {
            "query": query,
            "bosses": boss_results,
            "characters": character_results,
            "builds": build_results,
            "achievements": achievement_results,
            "creatures": creature_results,
            "total_results": len(boss_results) + len(character_results) + len(build_results) + len(achievement_results) + len(creature_results)
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

@app.get("/api/filter-creatures")
async def filter_creatures(
    type: Optional[str] = None,
    threat_level: Optional[str] = None,
    weakness: Optional[str] = None
):
    filter_criteria = {}
    
    if type:
        filter_criteria["type"] = {"$regex": type, "$options": "i"}
    
    if threat_level:
        filter_criteria["threat_level"] = {"$regex": threat_level, "$options": "i"}
    
    if weakness:
        filter_criteria["weaknesses"] = {"$in": [weakness]}
    
    creatures = list(creatures_collection.find(filter_criteria, {"_id": 0}))
    return {"creatures": creatures, "filters_applied": filter_criteria}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)