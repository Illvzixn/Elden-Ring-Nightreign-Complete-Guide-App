import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('bosses');
  const [bosses, setBosses] = useState([]);
  const [characters, setCharacters] = useState([]);
  const [builds, setBuilds] = useState([]);
  const [selectedBoss, setSelectedBoss] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [selectedBuild, setSelectedBuild] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [bossRecommendations, setBossRecommendations] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [bossesRes, charactersRes, buildsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/bosses`),
        fetch(`${API_BASE_URL}/api/characters`),
        fetch(`${API_BASE_URL}/api/builds`)
      ]);

      const bossesData = await bossesRes.json();
      const charactersData = await charactersRes.json();
      const buildsData = await buildsRes.json();

      setBosses(bossesData.bosses || []);
      setCharacters(charactersData.characters || []);
      setBuilds(buildsData.builds || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
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

  const getDifficultyColor = (rating) => {
    if (rating >= 9) return 'text-red-500';
    if (rating >= 7) return 'text-orange-500';
    if (rating >= 5) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getDifficultyText = (rating) => {
    if (rating >= 9) return 'Extremely Hard';
    if (rating >= 7) return 'Hard';
    if (rating >= 5) return 'Medium';
    return 'Easy';
  };

  const BossCard = ({ boss }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105"
      onClick={() => handleBossSelect(boss)}
    >
      <div className="relative">
        <img 
          src={boss.image} 
          alt={boss.name}
          className="w-full h-48 object-cover"
        />
        <div className="absolute top-4 right-4 bg-black bg-opacity-70 px-2 py-1 rounded">
          <span className={`text-sm font-bold ${getDifficultyColor(boss.difficulty_rating)}`}>
            {getDifficultyText(boss.difficulty_rating)}
          </span>
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-xl font-bold text-white mb-2">{boss.name}</h3>
        <p className="text-gray-300 text-sm mb-3">{boss.description}</p>
        <div className="flex justify-between items-center">
          <span className="text-purple-400 text-sm">Min Level: {boss.min_level}</span>
          <span className="text-yellow-400 text-sm">
            Weaknesses: {boss.weaknesses.join(', ')}
          </span>
        </div>
      </div>
    </div>
  );

  const CharacterCard = ({ character }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105"
      onClick={() => setSelectedCharacter(character)}
    >
      <div className="relative">
        <img 
          src={character.image} 
          alt={character.name}
          className="w-full h-48 object-cover"
        />
        <div className="absolute top-4 right-4 bg-black bg-opacity-70 px-2 py-1 rounded">
          <span className="text-sm font-bold text-blue-400">
            {character.playstyle}
          </span>
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-xl font-bold text-white mb-2">{character.name}</h3>
        <p className="text-gray-300 text-sm mb-3">{character.description}</p>
        <div className="flex justify-between items-center">
          <span className="text-purple-400 text-sm">Primary: {character.primary_stat}</span>
          <span className="text-yellow-400 text-sm">
            {character.weapon_type}
          </span>
        </div>
      </div>
    </div>
  );

  const BuildCard = ({ build }) => (
    <div 
      className="bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer transform transition-transform hover:scale-105"
      onClick={() => setSelectedBuild(build)}
    >
      <div className="p-4">
        <h3 className="text-xl font-bold text-white mb-2">{build.name}</h3>
        <p className="text-gray-300 text-sm mb-3">{build.description}</p>
        <div className="mb-3">
          <span className="text-purple-400 text-sm font-semibold">Type: </span>
          <span className="text-white text-sm">{build.type}</span>
        </div>
        <div className="mb-3">
          <span className="text-purple-400 text-sm font-semibold">Primary Weapon: </span>
          <span className="text-white text-sm">{build.primary_weapon}</span>
        </div>
        <div className="text-yellow-400 text-sm">
          Best for: {build.best_for.join(', ')}
        </div>
      </div>
    </div>
  );

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
            <div>
              <img 
                src={selectedBoss.image} 
                alt={selectedBoss.name}
                className="w-full h-64 object-cover rounded-lg mb-4"
              />
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Boss Info</h3>
                <p className="text-gray-300 mb-3">{selectedBoss.description}</p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-purple-400">Difficulty:</span>
                    <span className={`font-bold ${getDifficultyColor(selectedBoss.difficulty_rating)}`}>
                      {getDifficultyText(selectedBoss.difficulty_rating)} ({selectedBoss.difficulty_rating}/10)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-purple-400">Min Level:</span>
                    <span className="text-white">{selectedBoss.min_level}</span>
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
            <div>
              <img 
                src={selectedCharacter.image} 
                alt={selectedCharacter.name}
                className="w-full h-64 object-cover rounded-lg mb-4"
              />
              <div className="bg-gray-800 p-4 rounded-lg">
                <h3 className="text-xl font-bold text-white mb-2">Character Info</h3>
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
                <h3 className="text-xl font-bold text-white mb-2">Recommended Stats</h3>
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
              <span className="ml-2 text-sm text-gray-400">Boss Guide</span>
            </div>
            <div className="flex items-center space-x-4">
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="px-3 py-2 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
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
              Complete boss guides, character builds, and battle strategies
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
            </div>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <nav className="bg-gray-800 sticky top-16 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {['bosses', 'characters', 'builds'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-2 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab
                    ? 'border-purple-500 text-purple-400'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'bosses' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Nightlord Bosses</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {bosses.map((boss) => (
                <BossCard key={boss.id} boss={boss} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'characters' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Nightfarer Characters</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {characters.map((character) => (
                <CharacterCard key={character.id} character={character} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'builds' && (
          <div>
            <h2 className="text-3xl font-bold mb-8">Meta Builds</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {builds.map((build) => (
                <BuildCard key={build.id} build={build} />
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Modals */}
      {selectedBoss && <BossDetailModal />}
      {selectedCharacter && <CharacterDetailModal />}
      {selectedBuild && <BuildDetailModal />}
    </div>
  );
}

export default App;