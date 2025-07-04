from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Dict, Optional
import os
import uuid
from datetime import datetime

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
weapons_collection = db.weapons
achievements_collection = db.achievements

# Sample data initialization
def initialize_data():
    # Initialize bosses
    bosses = [
        {
            "id": str(uuid.uuid4()),
            "name": "Everdark Sovereign",
            "image": "https://images.unsplash.com/photo-1505635552518-3448ff116af3",
            "description": "A powerful Nightlord that poses a significant challenge to players.",
            "weaknesses": ["Holy"],
            "damage_types": ["Dark", "Physical"],
            "difficulty_rating": 9,
            "min_level": 60,
            "recommended_strategies": [
                "Use holy damage attacks to exploit weaknesses",
                "Maintain distance during dark magic phases",
                "Focus on teamwork for coordinated attacks"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Guardian", "Ironeye", "Recluse"],
            "recommended_builds": ["Colossal Titan", "Lunar Overlord"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Adel Baron of Night",
            "image": "https://images.unsplash.com/photo-1653539779206-893f95e7608a",
            "description": "A formidable foe that requires careful planning to defeat.",
            "weaknesses": ["Poison"],
            "damage_types": ["Dark", "Bleed"],
            "difficulty_rating": 8,
            "min_level": 50,
            "recommended_strategies": [
                "Utilize poison attacks to weaken the boss",
                "Watch for bleed buildup attacks",
                "Use ranged characters to maintain safe distance"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Duchess", "Executor", "Ironeye"],
            "recommended_builds": ["Shadow Dancer", "Colossal Titan"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Libra Creature of Night",
            "image": "https://images.pexels.com/photos/5416320/pexels-photo-5416320.jpeg",
            "description": "A creature that embodies the essence of night, challenging players with its unique abilities.",
            "weaknesses": ["Madness"],
            "damage_types": ["Psychic", "Dark"],
            "difficulty_rating": 7,
            "min_level": 45,
            "recommended_strategies": [
                "Employ madness-inducing attacks to gain an advantage",
                "Avoid prolonged eye contact",
                "Use mental resistance items"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Recluse", "Revenant", "Wylder"],
            "recommended_builds": ["Lunar Overlord", "Shadow Dancer"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Gladius",
            "image": "https://images.unsplash.com/photo-1623994903889-3be4a8c16b46",
            "description": "A beast of night that presents a significant challenge to players.",
            "weaknesses": ["Lightning"],
            "damage_types": ["Physical", "Dark"],
            "difficulty_rating": 8,
            "min_level": 55,
            "recommended_strategies": [
                "Use lightning attacks to exploit its weaknesses",
                "Focus on mobility to avoid charging attacks",
                "Coordinate team attacks during stun phases"
            ],
            "loot_drops": ["Relics", "Sovereign Sigils"],
            "recommended_team": ["Raider", "Guardian", "Ironeye"],
            "recommended_builds": ["Colossal Titan", "Shadow Dancer"]
        }
    ]
    
    # Initialize characters
    characters = [
        {
            "id": str(uuid.uuid4()),
            "name": "Ironeye",
            "description": "A dexterity-based archer excelling in ranged combat. His 'Marking' skill enhances team damage.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Dexterity",
            "weapon_type": "Bow",
            "abilities": ["Marking", "Distance Revival"],
            "recommended_builds": ["Shadow Dancer", "Lunar Overlord"],
            "starting_equipment": ["Composite Bow", "Leather Armor"],
            "playstyle": "Ranged DPS"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Executor",
            "description": "A skilled duelist wielding a katana, specializing in parrying and high damage output.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Dexterity",
            "weapon_type": "Katana",
            "abilities": ["Suncatcher", "Aspect of the Crucible"],
            "recommended_builds": ["Shadow Dancer", "Colossal Titan"],
            "starting_equipment": ["Katana", "Light Armor"],
            "playstyle": "Melee DPS"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Raider",
            "description": "A strength-focused warrior using colossal weapons. His 'Retaliate' skill provides damage negation.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Strength",
            "weapon_type": "Colossal Weapon",
            "abilities": ["Retaliate", "Dual Wield"],
            "recommended_builds": ["Colossal Titan"],
            "starting_equipment": ["Great Hammer", "Heavy Armor"],
            "playstyle": "Tank DPS"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Guardian",
            "description": "A tank class with high defensive capabilities, wielding a halberd and greatshield.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Strength",
            "weapon_type": "Halberd",
            "abilities": ["Steel Guard", "Wings of Salvation"],
            "recommended_builds": ["Colossal Titan"],
            "starting_equipment": ["Halberd", "Greatshield", "Plate Armor"],
            "playstyle": "Tank"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Duchess",
            "description": "A dexterity-focused character with the 'Restage' ability, offering significant burst potential.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Dexterity",
            "weapon_type": "Daggers",
            "abilities": ["Restage", "Swift Escape"],
            "recommended_builds": ["Shadow Dancer"],
            "starting_equipment": ["Twin Daggers", "Thief Outfit"],
            "playstyle": "Burst DPS"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Recluse",
            "description": "A magic-based character specializing in ranged attacks and crowd control.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Intelligence",
            "weapon_type": "Staff",
            "abilities": ["Sorcery Mastery", "Crowd Control"],
            "recommended_builds": ["Lunar Overlord"],
            "starting_equipment": ["Sorcerer's Staff", "Robes"],
            "playstyle": "Magic DPS"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wylder",
            "description": "An all-rounder knight with solid stats and a grappling hook for agility.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Balanced",
            "weapon_type": "Sword",
            "abilities": ["Claw Shot", "Onslaught Stake"],
            "recommended_builds": ["Colossal Titan", "Shadow Dancer"],
            "starting_equipment": ["Longsword", "Chain Mail"],
            "playstyle": "Versatile"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Revenant",
            "description": "A support character capable of summoning allies and providing invincibility.",
            "image": "https://images.unsplash.com/photo-1657954563624-25c38c199f3b",
            "primary_stat": "Faith",
            "weapon_type": "Catalyst",
            "abilities": ["Summon Allies", "Invincibility"],
            "recommended_builds": ["Lunar Overlord"],
            "starting_equipment": ["Sacred Catalyst", "Ritual Robes"],
            "playstyle": "Support"
        }
    ]
    
    # Initialize builds
    builds = [
        {
            "id": str(uuid.uuid4()),
            "name": "Colossal Titan",
            "type": "Strength",
            "description": "Focus on tanking damage and delivering devastating hits with colossal weapons.",
            "primary_weapon": "Crescent Moon Greatblade",
            "secondary_weapon": "Axe of Godfrey",
            "armor_set": "Lion Knight's Bulwark",
            "talismans": [
                "Radagon's Scarseal",
                "Great-Jar's Arsenal",
                "Dragoncrest Greatshield Talisman"
            ],
            "recommended_stats": {
                "Strength": 60,
                "Vigor": 50,
                "Endurance": 40
            },
            "strategy": "Tank damage and deliver devastating hits with wide trajectories",
            "best_for": ["Raider", "Guardian", "Wylder"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Shadow Dancer",
            "type": "Dexterity",
            "description": "Utilize poison and bleed effects with rapid combos and high mobility.",
            "primary_weapon": "Twin Scaled Fang Daggers",
            "secondary_weapon": "Red-Moon Wakizashi",
            "armor_set": "Nightweave Attire",
            "talismans": [
                "Rotten Winged Sword Insignia",
                "Bloodlord's Emblem",
                "Assassin's Cerulean Dagger"
            ],
            "recommended_stats": {
                "Dexterity": 60,
                "Vigor": 35,
                "Endurance": 45
            },
            "strategy": "Rapid combos with poison and bleed effects, maintaining high mobility",
            "best_for": ["Duchess", "Executor", "Ironeye"]
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Lunar Overlord",
            "type": "Intelligence",
            "description": "Employ high-damage sorceries while managing FP efficiently.",
            "primary_weapon": "Moonlight Crescent Staff",
            "secondary_weapon": "Crystal Sword",
            "armor_set": "Sage of the Cosmos",
            "talismans": [
                "Radagon Icon",
                "Moonveil Crest",
                "Cerulean Amber Medallion"
            ],
            "recommended_stats": {
                "Intelligence": 60,
                "Vigor": 30,
                "Mind": 50
            },
            "strategy": "High-damage sorceries with efficient FP management",
            "best_for": ["Recluse", "Revenant", "Wylder"]
        }
    ]
    
    # Clear existing data and insert new
    bosses_collection.delete_many({})
    characters_collection.delete_many({})
    builds_collection.delete_many({})
    
    bosses_collection.insert_many(bosses)
    characters_collection.insert_many(characters)
    builds_collection.insert_many(builds)

# Initialize data on startup
initialize_data()

@app.get("/")
async def root():
    return {"message": "Elden Ring Nightreign Boss Guide API"}

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

@app.get("/api/search")
async def search(query: str):
    # Search across bosses, characters, and builds
    boss_results = list(bosses_collection.find(
        {"$text": {"$search": query}}, 
        {"_id": 0}
    ))
    
    character_results = list(characters_collection.find(
        {"$text": {"$search": query}}, 
        {"_id": 0}
    ))
    
    build_results = list(builds_collection.find(
        {"$text": {"$search": query}}, 
        {"_id": 0}
    ))
    
    return {
        "bosses": boss_results,
        "characters": character_results,
        "builds": build_results
    }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)