import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('bosses');
  const [bosses, setBosses] = useState([]);
  const [characters, setCharacters] = useState([]);
  const [builds, setBuilds] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [walkthroughs, setWalkthroughs] = useState([]);
  const [customBuilds, setCustomBuilds] = useState([]);
  const [creatures, setCreatures] = useState([]);
  const [secrets, setSecrets] = useState([]);
  const [weaponSkills, setWeaponSkills] = useState([]);
  const [weaponPassives, setWeaponPassives] = useState([]);
  const [selectedBoss, setSelectedBoss] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [selectedBuild, setSelectedBuild] = useState(null);
  const [selectedAchievement, setSelectedAchievement] = useState(null);
  const [selectedWalkthrough, setSelectedWalkthrough] = useState(null);
  const [selectedCreature, setSelectedCreature] = useState(null);
  const [selectedSecret, setSelectedSecret] = useState(null);
  const [selectedWeaponSkill, setSelectedWeaponSkill] = useState(null);
  const [selectedWeaponPassive, setSelectedWeaponPassive] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [bossRecommendations, setBossRecommendations] = useState(null);
  const [filters, setFilters] = useState({
    difficulty: '',
    weakness: '',
    playstyle: '',
    minLevel: '',
    maxLevel: '',
    creatureType: '',
    threatLevel: ''
  });
  const [showCustomBuildForm, setShowCustomBuildForm] = useState(false);
  const [customBuildData, setCustomBuildData] = useState({
    name: '',
    character: '',
    type: '',
    description: '',
    primary_weapon: '',
    secondary_weapon: '',
    strategy: ''
  });

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [bossesRes, charactersRes, buildsRes, achievementsRes, walkthroughsRes, customBuildsRes, creaturesRes, secretsRes, weaponSkillsRes, weaponPassivesRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/bosses`),
        fetch(`${API_BASE_URL}/api/characters`),
        fetch(`${API_BASE_URL}/api/builds`),
        fetch(`${API_BASE_URL}/api/achievements`),
        fetch(`${API_BASE_URL}/api/walkthroughs`),
        fetch(`${API_BASE_URL}/api/custom-builds`),
        fetch(`${API_BASE_URL}/api/creatures`),
        fetch(`${API_BASE_URL}/api/secrets`),
        fetch(`${API_BASE_URL}/api/weapon-skills`),
        fetch(`${API_BASE_URL}/api/weapon-passives`)
      ]);

      const bossesData = await bossesRes.json();
      const charactersData = await charactersRes.json();
      const buildsData = await buildsRes.json();
      const achievementsData = await achievementsRes.json();
      const walkthroughsData = await walkthroughsRes.json();
      const customBuildsData = await customBuildsRes.json();
      const creaturesData = await creaturesRes.json();
      const secretsData = await secretsRes.json();
      const weaponSkillsData = await weaponSkillsRes.json();
      const weaponPassivesData = await weaponPassivesRes.json();

      setBosses(bossesData.bosses || []);
      setCharacters(charactersData.characters || []);
      setBuilds(buildsData.builds || []);
      setAchievements(achievementsData.achievements || []);
      setWalkthroughs(walkthroughsData.walkthroughs || []);
      setCustomBuilds(customBuildsData.custom_builds || []);
      setCreatures(creaturesData.creatures || []);
      setSecrets(secretsData.secrets || []);
      setWeaponSkills(weaponSkillsData.weapon_skills || []);
      setWeaponPassives(weaponPassivesData.weapon_passives || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/search?query=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const handleFilterBosses = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.weakness) params.append('weakness', filters.weakness);
      if (filters.minLevel) params.append('min_level', filters.minLevel);
      if (filters.maxLevel) params.append('max_level', filters.maxLevel);

      const response = await fetch(`${API_BASE_URL}/api/filter-bosses?${params}`);
      const data = await response.json();
      setBosses(data.bosses || []);
    } catch (error) {
      console.error('Error filtering bosses:', error);
    }
  };

  const handleFilterCharacters = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.playstyle) params.append('playstyle', filters.playstyle);

      const response = await fetch(`${API_BASE_URL}/api/filter-characters?${params}`);
      const data = await response.json();
      setCharacters(data.characters || []);
    } catch (error) {
      console.error('Error filtering characters:', error);
    }
  };

  const handleFilterCreatures = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.creatureType) params.append('type', filters.creatureType);
      if (filters.threatLevel) params.append('threat_level', filters.threatLevel);
      if (filters.weakness) params.append('weakness', filters.weakness);

      const response = await fetch(`${API_BASE_URL}/api/filter-creatures?${params}`);
      const data = await response.json();
      setCreatures(data.creatures || []);
    } catch (error) {
      console.error('Error filtering creatures:', error);
    }
  };

  const clearFilters = () => {
    setFilters({
      difficulty: '',
      weakness: '',
      playstyle: '',
      minLevel: '',
      maxLevel: '',
      creatureType: '',
      threatLevel: ''
    });
    fetchData();
  };

  const fetchBossRecommendations = async (bossId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/boss-recommendations/${bossId}`);
      const data = await response.json();
      setBossRecommendations(data);
    } catch (error) {
      console.error('Error fetching boss recommendations:', error);
    }
  };

  const handleBossSelect = (boss) => {
    setSelectedBoss(boss);
    fetchBossRecommendations(boss.id);
  };

  const handleCustomBuildSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/api/custom-build`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(customBuildData),
      });

      if (response.ok) {
        setShowCustomBuildForm(false);
        setCustomBuildData({
          name: '',
          character: '',
          type: '',
          description: '',
          primary_weapon: '',
          secondary_weapon: '',
          strategy: ''
        });
        fetchData(); // Refresh custom builds
      }
    } catch (error) {
      console.error('Error creating custom build:', error);
    }
  };

  const getDifficultyColor = (rating) => {
    if (rating >= 9) return 'text-red-500';
    if (rating >= 7) return 'text-orange-500';
    if (rating >= 5) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getDifficultyText = (rating) => {
    if (rating >= 9) return 'Extreme';
    if (rating >= 7) return 'Hard';
    if (rating >= 5) return 'Medium';
    return 'Easy';
  };

  const getAchievementColor = (difficulty) => {
    switch (difficulty) {
      case 'Platinum': return 'text-yellow-400';
      case 'Extreme': return 'text-red-500';
      case 'Very Hard': return 'text-orange-500';
      case 'Hard': return 'text-yellow-500';
      case 'Medium': return 'text-blue-500';
      default: return 'text-green-500';
    }
  };

  const getThreatColor = (level) => {
    switch (level) {
      case 'Ultimate': return 'text-red-600';
      case 'Extreme': return 'text-red-500';
      case 'High': return 'text-orange-500';
      case 'Medium': return 'text-yellow-500';
      default: return 'text-green-500';
    }
  };

  const BossCard = ({ boss }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => handleBossSelect(boss)}
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{boss.name}</h3>
          <span className={`text-sm font-bold ${getDifficultyColor(boss.difficulty_rating)}`}>
            {getDifficultyText(boss.difficulty_rating)}
          </span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{boss.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Level Range:</span>
            <span className="text-white text-sm">{boss.min_level} - {boss.max_level}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Weaknesses:</span>
            <span className="text-yellow-400 text-sm">{boss.weaknesses.join(', ')}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Expedition:</span>
            <span className="text-blue-400 text-sm">{boss.expedition_name}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const CharacterCard = ({ character }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => setSelectedCharacter(character)}
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{character.name}</h3>
          <span className="text-sm font-bold text-blue-400">
            {character.playstyle}
          </span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{character.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Primary Stat:</span>
            <span className="text-white text-sm">{character.primary_stat}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Weapon Type:</span>
            <span className="text-yellow-400 text-sm">{character.weapon_type}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Max Level:</span>
            <span className="text-green-400 text-sm">{character.max_level}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const BuildCard = ({ build }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => setSelectedBuild(build)}
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{build.name}</h3>
          <span className="text-sm font-bold text-purple-400">{build.type}</span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{build.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Character:</span>
            <span className="text-white text-sm">{build.character}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Primary Weapon:</span>
            <span className="text-yellow-400 text-sm">{build.primary_weapon}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const AchievementCard = ({ achievement }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => setSelectedAchievement(achievement)}
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{achievement.name}</h3>
          <div className="text-right">
            <span className={`text-sm font-bold ${getAchievementColor(achievement.difficulty)}`}>
              {achievement.difficulty}
            </span>
            <div className="text-xs text-gray-400">#{achievement.rank}</div>
          </div>
        </div>
        <p className="text-gray-300 text-sm mb-3">{achievement.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Category:</span>
            <span className="text-white text-sm">{achievement.category}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Completion:</span>
            <span className="text-green-400 text-sm">{achievement.percentage}%</span>
          </div>
        </div>
      </div>
    </div>
  );

  const CreatureCard = ({ creature }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => setSelectedCreature(creature)}
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{creature.name}</h3>
          <span className={`text-sm font-bold ${getThreatColor(creature.threat_level)}`}>
            {creature.threat_level}
          </span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{creature.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Type:</span>
            <span className="text-white text-sm">{creature.type}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Location:</span>
            <span className="text-blue-400 text-sm text-right">{creature.location}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Weaknesses:</span>
            <span className="text-yellow-400 text-sm">{creature.weaknesses.join(', ')}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const WalkthroughCard = ({ walkthrough }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105 border border-gray-700"
      onClick={() => setSelectedWalkthrough(walkthrough)}
    >
      <div className="p-4">
        <h3 className="text-xl font-bold text-white mb-2">{walkthrough.title}</h3>
        <p className="text-gray-300 text-sm mb-3">{walkthrough.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Character:</span>
            <span className="text-white text-sm">{walkthrough.character}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Chapters:</span>
            <span className="text-yellow-400 text-sm">{walkthrough.chapters.length}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const SecretCard = ({ secret }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700"
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{secret.name}</h3>
          <span className="text-sm font-bold text-purple-400">{secret.category}</span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{secret.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Location:</span>
            <span className="text-blue-400 text-sm">{secret.location}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Difficulty:</span>
            <span className="text-orange-400 text-sm">{secret.difficulty}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const WeaponSkillCard = ({ skill }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700"
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{skill.name}</h3>
          <span className="text-sm font-bold text-blue-400">{skill.fp_cost} FP</span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{skill.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Category:</span>
            <span className="text-white text-sm">{skill.category}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Damage Type:</span>
            <span className="text-red-400 text-sm">{skill.damage_type}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const WeaponPassiveCard = ({ passive }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700"
    >
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-white">{passive.name}</h3>
          <span className="text-sm font-bold text-green-400">{passive.category}</span>
        </div>
        <p className="text-gray-300 text-sm mb-3">{passive.description}</p>
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Effect:</span>
            <span className="text-yellow-400 text-sm">{passive.effect}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-purple-400 text-sm">Compatible Characters:</span>
            <span className="text-blue-400 text-sm">{passive.compatible_characters.slice(0, 2).join(', ')}</span>
          </div>
        </div>
      </div>
    </div>
  );

  const SearchResults = () => (
    <div className="bg-gray-800 rounded-lg p-6 mb-6">
      <h3 className="text-xl font-bold text-white mb-4">
        Search Results for "{searchResults.query}" ({searchResults.total_results} results)
      </h3>
      
      {searchResults.bosses.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Bosses</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.bosses.map((boss) => (
              <BossCard key={boss.id} boss={boss} />
            ))}
          </div>
        </div>
      )}
      
      {searchResults.characters.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Characters</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.characters.map((character) => (
              <CharacterCard key={character.id} character={character} />
            ))}
          </div>
        </div>
      )}
      
      {searchResults.builds.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Builds</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.builds.map((build) => (
              <BuildCard key={build.id} build={build} />
            ))}
          </div>
        </div>
      )}
      
      {searchResults.achievements.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Achievements</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.achievements.map((achievement) => (
              <AchievementCard key={achievement.id} achievement={achievement} />
            ))}
          </div>
        </div>
      )}

      {searchResults.creatures && searchResults.creatures.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Creatures & Enemies</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.creatures.map((creature) => (
              <CreatureCard key={creature.id} creature={creature} />
            ))}
          </div>
        </div>
      )}

      {searchResults.secrets && searchResults.secrets.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Secrets</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.secrets.map((secret) => (
              <SecretCard key={secret.id} secret={secret} />
            ))}
          </div>
        </div>
      )}

      {searchResults.weapon_skills && searchResults.weapon_skills.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Weapon Skills</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.weapon_skills.map((skill) => (
              <WeaponSkillCard key={skill.id} skill={skill} />
            ))}
          </div>
        </div>
      )}

      {searchResults.weapon_passives && searchResults.weapon_passives.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-purple-400 mb-3">Weapon Passives</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {searchResults.weapon_passives.map((passive) => (
              <WeaponPassiveCard key={passive.id} passive={passive} />
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const FilterPanel = () => (
    <div className="bg-gray-800 rounded-lg p-4 mb-6">
      <h3 className="text-lg font-bold text-white mb-4">Filters</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {activeTab === 'bosses' && (
          <>
            <select
              value={filters.difficulty}
              onChange={(e) => setFilters({...filters, difficulty: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
              <option value="extreme">Extreme</option>
            </select>
            <select
              value={filters.weakness}
              onChange={(e) => setFilters({...filters, weakness: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Weaknesses</option>
              <option value="Holy">Holy</option>
              <option value="Lightning">Lightning</option>
              <option value="Fire">Fire</option>
              <option value="Poison">Poison</option>
              <option value="Madness">Madness</option>
            </select>
            <input
              type="number"
              placeholder="Min Level"
              value={filters.minLevel}
              onChange={(e) => setFilters({...filters, minLevel: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <input
              type="number"
              placeholder="Max Level"
              value={filters.maxLevel}
              onChange={(e) => setFilters({...filters, maxLevel: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </>
        )}
        
        {activeTab === 'characters' && (
          <select
            value={filters.playstyle}
            onChange={(e) => setFilters({...filters, playstyle: e.target.value})}
            className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">All Playstyles</option>
            <option value="Tank">Tank</option>
            <option value="DPS">DPS</option>
            <option value="Support">Support</option>
            <option value="Versatile">Versatile</option>
            <option value="Marksman">Marksman</option>
            <option value="Spellcaster">Spellcaster</option>
          </select>
        )}

        {activeTab === 'creatures' && (
          <>
            <select
              value={filters.creatureType}
              onChange={(e) => setFilters({...filters, creatureType: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Types</option>
              <option value="Nightlord">Nightlord</option>
              <option value="Elite Enemy">Elite Enemy</option>
              <option value="Large Enemy">Large Enemy</option>
              <option value="Medium Enemy">Medium Enemy</option>
              <option value="Small Enemy">Small Enemy</option>
              <option value="Special Enemy">Special Enemy</option>
            </select>
            <select
              value={filters.threatLevel}
              onChange={(e) => setFilters({...filters, threatLevel: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Threat Levels</option>
              <option value="Ultimate">Ultimate</option>
              <option value="Extreme">Extreme</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
            <select
              value={filters.weakness}
              onChange={(e) => setFilters({...filters, weakness: e.target.value})}
              className="px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="">All Weaknesses</option>
              <option value="Holy">Holy</option>
              <option value="Lightning">Lightning</option>
              <option value="Fire">Fire</option>
              <option value="Poison">Poison</option>
              <option value="Madness">Madness</option>
              <option value="Magic">Magic</option>
              <option value="Strike">Strike</option>
              <option value="Pierce">Pierce</option>
            </select>
          </>
        )}
      </div>
      <div className="flex space-x-2 mt-4">
        <button
          onClick={() => {
            if (activeTab === 'bosses') handleFilterBosses();
            else if (activeTab === 'characters') handleFilterCharacters();
            else if (activeTab === 'creatures') handleFilterCreatures();
          }}
          className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-md text-white font-semibold"
        >
          Apply Filters
        </button>
        <button
          onClick={clearFilters}
          className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-md text-white font-semibold"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );

  const CustomBuildForm = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <form onSubmit={handleCustomBuildSubmit} className="p-6">
          <h2 className="text-2xl font-bold text-white mb-4">Create Custom Build</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Build Name"
              value={customBuildData.name}
              onChange={(e) => setCustomBuildData({...customBuildData, name: e.target.value})}
              className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <select
              value={customBuildData.character}
              onChange={(e) => setCustomBuildData({...customBuildData, character: e.target.value})}
              className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            >
              <option value="">Select Character</option>
              {characters.map(char => (
                <option key={char.id} value={char.name}>{char.name}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Build Type"
              value={customBuildData.type}
              onChange={(e) => setCustomBuildData({...customBuildData, type: e.target.value})}
              className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <input
              type="text"
              placeholder="Primary Weapon"
              value={customBuildData.primary_weapon}
              onChange={(e) => setCustomBuildData({...customBuildData, primary_weapon: e.target.value})}
              className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <input
              type="text"
              placeholder="Secondary Weapon"
              value={customBuildData.secondary_weapon}
              onChange={(e) => setCustomBuildData({...customBuildData, secondary_weapon: e.target.value})}
              className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          
          <textarea
            placeholder="Description"
            value={customBuildData.description}
            onChange={(e) => setCustomBuildData({...customBuildData, description: e.target.value})}
            className="w-full px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 mt-4"
            rows="3"
            required
          />
          
          <textarea
            placeholder="Strategy"
            value={customBuildData.strategy}
            onChange={(e) => setCustomBuildData({...customBuildData, strategy: e.target.value})}
            className="w-full px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 mt-4"
            rows="3"
            required
          />
          
          <div className="flex space-x-4 mt-6">
            <button
              type="submit"
              className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-md text-white font-semibold"
            >
              Create Build
            </button>
            <button
              type="button"
              onClick={() => setShowCustomBuildForm(false)}
              className="bg-gray-600 hover:bg-gray-700 px-6 py-2 rounded-md text-white font-semibold"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // Modal components remain the same but updated for new level system
  const BossDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedBoss.name}</h2>
            <button 
              onClick={() => setSelectedBoss(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Boss Information</h3>
              <p className="text-gray-300 mb-3">{selectedBoss.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">Difficulty:</span>
                  <span className={`font-bold ${getDifficultyColor(selectedBoss.difficulty_rating)}`}>
                    {getDifficultyText(selectedBoss.difficulty_rating)} ({selectedBoss.difficulty_rating}/10)
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Level Range:</span>
                  <span className="text-white">{selectedBoss.min_level} - {selectedBoss.max_level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Expedition:</span>
                  <span className="text-blue-400">{selectedBoss.expedition_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Weaknesses:</span>
                  <span className="text-yellow-400">{selectedBoss.weaknesses.join(', ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Damage Types:</span>
                  <span className="text-red-400">{selectedBoss.damage_types.join(', ')}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Strategies</h3>
                <ul className="space-y-2">
                  {selectedBoss.recommended_strategies.map((strategy, index) => (
                    <li key={index} className="text-gray-300 flex items-start">
                      <span className="text-green-400 mr-2">•</span>
                      {strategy}
                    </li>
                  ))}
                </ul>
              </div>
              
              {bossRecommendations && (
                <>
                  <div className="bg-gray-800 p-4 rounded-lg mb-4">
                    <h3 className="text-xl font-bold text-white mb-2">Recommended Team</h3>
                    <div className="grid grid-cols-1 gap-2">
                      {bossRecommendations.recommended_characters.map((char, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <span className="text-blue-400">{char.name}</span>
                          <span className="text-gray-400">({char.playstyle})</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <h3 className="text-xl font-bold text-white mb-2">Recommended Builds</h3>
                    <div className="grid grid-cols-1 gap-2">
                      {bossRecommendations.recommended_builds.map((build, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <span className="text-purple-400">{build.name}</span>
                          <span className="text-gray-400">({build.type})</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const CharacterDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedCharacter.name}</h2>
            <button 
              onClick={() => setSelectedCharacter(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Character Information</h3>
              <p className="text-gray-300 mb-3">{selectedCharacter.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">Primary Stat:</span>
                  <span className="text-white">{selectedCharacter.primary_stat}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Weapon Type:</span>
                  <span className="text-white">{selectedCharacter.weapon_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Playstyle:</span>
                  <span className="text-blue-400">{selectedCharacter.playstyle}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Max Level:</span>
                  <span className="text-green-400">{selectedCharacter.max_level}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Damage Types:</span>
                  <span className="text-red-400">{selectedCharacter.damage_types.join(', ')}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Abilities</h3>
                <ul className="space-y-2">
                  {selectedCharacter.abilities.map((ability, index) => (
                    <li key={index} className="text-gray-300 flex items-start">
                      <span className="text-green-400 mr-2">•</span>
                      {ability}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Starting Equipment</h3>
                <ul className="space-y-1">
                  {selectedCharacter.starting_equipment.map((item, index) => (
                    <li key={index} className="text-gray-300">{item}</li>
                  ))}
                </ul>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Recommended Builds</h3>
                <div className="space-y-1">
                  {selectedCharacter.recommended_builds.map((build, index) => (
                    <div key={index} className="text-purple-400">{build}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const BuildDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedBuild.name}</h2>
            <button 
              onClick={() => setSelectedBuild(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Build Overview</h3>
                <p className="text-gray-300 mb-3">{selectedBuild.description}</p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-purple-400">Character:</span>
                    <span className="text-white">{selectedBuild.character}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-purple-400">Type:</span>
                    <span className="text-white">{selectedBuild.type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-purple-400">Strategy:</span>
                    <span className="text-white text-sm">{selectedBuild.strategy}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Equipment</h3>
                <div className="space-y-2">
                  <div>
                    <span className="text-purple-400">Primary Weapon:</span>
                    <span className="text-white ml-2">{selectedBuild.primary_weapon}</span>
                  </div>
                  <div>
                    <span className="text-purple-400">Secondary Weapon:</span>
                    <span className="text-white ml-2">{selectedBuild.secondary_weapon}</span>
                  </div>
                  <div>
                    <span className="text-purple-400">Armor Set:</span>
                    <span className="text-white ml-2">{selectedBuild.armor_set}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Talismans</h3>
                <ul className="space-y-1">
                  {selectedBuild.talismans.map((talisman, index) => (
                    <li key={index} className="text-gray-300 flex items-start">
                      <span className="text-yellow-400 mr-2">•</span>
                      {talisman}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Recommended Stats (Level 15)</h3>
                <div className="space-y-1">
                  {Object.entries(selectedBuild.recommended_stats).map(([stat, value]) => (
                    <div key={stat} className="flex justify-between">
                      <span className="text-purple-400">{stat}:</span>
                      <span className="text-white">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Best For</h3>
                <div className="space-y-1">
                  {selectedBuild.best_for.map((character, index) => (
                    <div key={index} className="text-blue-400">{character}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const AchievementDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedAchievement.name}</h2>
            <button 
              onClick={() => setSelectedAchievement(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="bg-gray-800 p-4 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-2">Achievement Details</h3>
            <p className="text-gray-300 mb-4">{selectedAchievement.description}</p>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-purple-400">Rank:</span>
                <span className="text-white">#{selectedAchievement.rank} / 37</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-400">Category:</span>
                <span className="text-white">{selectedAchievement.category}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-400">Difficulty:</span>
                <span className={`font-bold ${getAchievementColor(selectedAchievement.difficulty)}`}>
                  {selectedAchievement.difficulty}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-400">Completion Rate:</span>
                <span className="text-green-400">{selectedAchievement.percentage}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-400">Reward:</span>
                <span className="text-yellow-400">{selectedAchievement.reward}</span>
              </div>
              <div>
                <span className="text-purple-400">Requirements:</span>
                <p className="text-white mt-1">{selectedAchievement.requirements}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const CreatureDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedCreature.name}</h2>
            <button 
              onClick={() => setSelectedCreature(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Creature Information</h3>
              <p className="text-gray-300 mb-3">{selectedCreature.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">Type:</span>
                  <span className="text-white">{selectedCreature.type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Threat Level:</span>
                  <span className={`font-bold ${getThreatColor(selectedCreature.threat_level)}`}>
                    {selectedCreature.threat_level}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Location:</span>
                  <span className="text-blue-400">{selectedCreature.location}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Weaknesses:</span>
                  <span className="text-yellow-400">{selectedCreature.weaknesses.join(', ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Resistances:</span>
                  <span className="text-red-400">{selectedCreature.resistances.join(', ')}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Combat Details</h3>
                <div className="space-y-2">
                  <div>
                    <span className="text-purple-400">Damage Types:</span>
                    <span className="text-red-400 ml-2">{selectedCreature.damage_types.join(', ')}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Notes & Strategy</h3>
                <p className="text-gray-300">{selectedCreature.notes}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const WalkthroughDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedWalkthrough.title}</h2>
            <button 
              onClick={() => setSelectedWalkthrough(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <p className="text-gray-300 mb-6">{selectedWalkthrough.description}</p>
          
          <div className="space-y-6">
            {selectedWalkthrough.chapters.map((chapter, index) => (
              <div key={index} className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">
                  Chapter {chapter.chapter}: {chapter.title}
                </h3>
                <p className="text-gray-300 mb-3">{chapter.objective}</p>
                <div className="mb-4">
                  <h4 className="text-lg font-semibold text-purple-400 mb-2">Steps:</h4>
                  <ol className="space-y-1">
                    {chapter.steps.map((step, stepIndex) => (
                      <li key={stepIndex} className="text-gray-300 flex items-start">
                        <span className="text-green-400 mr-2">{stepIndex + 1}.</span>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Reward:</span>
                  <span className="text-yellow-400">{chapter.reward}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading Elden Ring Nightreign Guide...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-black bg-opacity-50 backdrop-blur-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-white">Elden Ring Nightreign</h1>
              <span className="ml-2 text-sm text-gray-400">Complete Guide</span>
            </div>
            <div className="flex items-center space-x-4">
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={handleSearch}
                className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-md text-white font-semibold"
              >
                Search
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative h-96 bg-gradient-to-r from-purple-900 to-black">
        <div className="absolute inset-0 bg-black opacity-50"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
          <div className="text-center w-full">
            <h2 className="text-4xl md:text-6xl font-bold mb-4">
              Master the <span className="text-purple-400">Nightreign</span>
            </h2>
            <p className="text-xl md:text-2xl text-gray-300 mb-8">
              Complete boss guides, character builds, achievements, walkthroughs, and creature database
            </p>
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => setActiveTab('bosses')}
                className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                Boss Guides
              </button>
              <button
                onClick={() => setActiveTab('characters')}
                className="bg-gray-700 hover:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                Characters
              </button>
              <button
                onClick={() => setActiveTab('achievements')}
                className="bg-gray-700 hover:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-colors"
              >
                Achievements
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <nav className="bg-gray-800 sticky top-16 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 overflow-x-auto">
            {['bosses', 'characters', 'builds', 'achievements', 'walkthroughs', 'creatures', 'secrets', 'weapon-skills', 'weapon-passives'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-2 border-b-2 font-medium text-sm capitalize whitespace-nowrap ${
                  activeTab === tab
                    ? 'border-purple-500 text-purple-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                {tab === 'creatures' ? 'Creatures & Enemies' : 
                 tab === 'weapon-skills' ? 'Weapon Skills' :
                 tab === 'weapon-passives' ? 'Weapon Passives' : tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Results */}
        {searchResults && <SearchResults />}

        {/* Filter Panel */}
        {(activeTab === 'bosses' || activeTab === 'characters' || activeTab === 'creatures') && <FilterPanel />}

        {/* Build Creation Button */}
        {activeTab === 'builds' && (
          <div className="mb-6">
            <button
              onClick={() => setShowCustomBuildForm(true)}
              className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-semibold"
            >
              Create Custom Build
            </button>
          </div>
        )}

        {/* Content Sections */}
        {activeTab === 'bosses' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Nightlord Bosses ({bosses.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bosses.map((boss) => (
                <BossCard key={boss.id} boss={boss} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'characters' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Nightfarer Characters ({characters.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {characters.map((character) => (
                <CharacterCard key={character.id} character={character} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'builds' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Character Builds ({builds.length + customBuilds.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {builds.map((build) => (
                <BuildCard key={build.id} build={build} />
              ))}
              {customBuilds.map((build) => (
                <BuildCard key={build.id} build={build} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'achievements' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Achievements & Trophies ({achievements.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {achievements.map((achievement) => (
                <AchievementCard key={achievement.id} achievement={achievement} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'walkthroughs' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Remembrance Quest Walkthroughs ({walkthroughs.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {walkthroughs.map((walkthrough) => (
                <WalkthroughCard key={walkthrough.id} walkthrough={walkthrough} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'creatures' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Creatures & Enemies ({creatures.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {creatures.map((creature) => (
                <CreatureCard key={creature.id} creature={creature} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'secrets' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Secrets ({secrets.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {secrets.map((secret) => (
                <SecretCard key={secret.id} secret={secret} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'weapon-skills' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Weapon Skills ({weaponSkills.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {weaponSkills.map((skill) => (
                <WeaponSkillCard key={skill.id} skill={skill} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'weapon-passives' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Weapon Passive Abilities ({weaponPassives.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {weaponPassives.map((passive) => (
                <WeaponPassiveCard key={passive.id} passive={passive} />
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Modals */}
      {selectedBoss && <BossDetailModal />}
      {selectedCharacter && <CharacterDetailModal />}
      {selectedBuild && <BuildDetailModal />}
      {selectedAchievement && <AchievementDetailModal />}
      {selectedWalkthrough && <WalkthroughDetailModal />}
      {selectedCreature && <CreatureDetailModal />}
      {selectedSecret && <SecretDetailModal />}
      {selectedWeaponSkill && <WeaponSkillDetailModal />}
      {selectedWeaponPassive && <WeaponPassiveDetailModal />}
      {showCustomBuildForm && <CustomBuildForm />}
    </div>
  );

  const SecretDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedSecret.name}</h2>
            <button 
              onClick={() => setSelectedSecret(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Secret Information</h3>
              <p className="text-gray-300 mb-3">{selectedSecret.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">Category:</span>
                  <span className="text-white">{selectedSecret.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Location:</span>
                  <span className="text-blue-400">{selectedSecret.location}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Difficulty:</span>
                  <span className="text-orange-400">{selectedSecret.difficulty}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Reward:</span>
                  <span className="text-yellow-400">{selectedSecret.reward}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">How to Find</h3>
                <p className="text-gray-300">{selectedSecret.how_to_find}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const WeaponSkillDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedWeaponSkill.name}</h2>
            <button 
              onClick={() => setSelectedWeaponSkill(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Skill Information</h3>
              <p className="text-gray-300 mb-3">{selectedWeaponSkill.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">FP Cost:</span>
                  <span className="text-blue-400">{selectedWeaponSkill.fp_cost}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Category:</span>
                  <span className="text-white">{selectedWeaponSkill.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Damage Type:</span>
                  <span className="text-red-400">{selectedWeaponSkill.damage_type}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Effect</h3>
                <p className="text-gray-300">{selectedWeaponSkill.effect}</p>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Usable With</h3>
                <p className="text-gray-300">{selectedWeaponSkill.usable_with}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const WeaponPassiveDetailModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-3xl font-bold text-white">{selectedWeaponPassive.name}</h2>
            <button 
              onClick={() => setSelectedWeaponPassive(null)}
              className="text-gray-400 hover:text-white text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-xl font-bold text-white mb-2">Passive Information</h3>
              <p className="text-gray-300 mb-3">{selectedWeaponPassive.description}</p>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-purple-400">Category:</span>
                  <span className="text-green-400">{selectedWeaponPassive.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Effect:</span>
                  <span className="text-yellow-400">{selectedWeaponPassive.effect}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Scaling:</span>
                  <span className="text-blue-400">{selectedWeaponPassive.scaling}</span>
                </div>
              </div>
            </div>
            
            <div>
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <h3 className="text-xl font-bold text-white mb-2">Compatible Characters</h3>
                <div className="space-y-1">
                  {selectedWeaponPassive.compatible_characters.map((character, index) => (
                    <div key={index} className="text-blue-400">{character}</div>
                  ))}
                </div>
              </div>
              
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Weapon Types</h3>
                <div className="space-y-1">
                  {selectedWeaponPassive.weapon_types.map((type, index) => (
                    <div key={index} className="text-gray-300">{type}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;