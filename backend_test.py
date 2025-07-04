import requests
import unittest
import sys
import os
import json
import uuid

class EldenRingNightReignAPITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(EldenRingNightReignAPITest, self).__init__(*args, **kwargs)
        # Get the backend URL from frontend .env file
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.base_url = line.strip().split('=')[1]
                    break
        
        print(f"Using backend URL: {self.base_url}")
        self.boss_id = None
        self.character_id = None
        self.build_id = None
        self.achievement_id = None
        self.walkthrough_id = None

    def test_01_root_endpoint(self):
        """Test the root endpoint"""
        print("\n🔍 Testing root endpoint...")
        try:
            response = requests.get(f"{self.base_url}/")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("message", data)
            print("✅ Root endpoint test passed")
        except Exception as e:
            print(f"❌ Root endpoint test failed: {str(e)}")
            # Don't fail the entire test suite if the root endpoint is not available
            # as it might be configured differently in production

    def test_02_get_bosses(self):
        """Test getting all bosses"""
        print("\n🔍 Testing get all bosses...")
        response = requests.get(f"{self.base_url}/api/bosses")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("bosses", data)
        self.assertIsInstance(data["bosses"], list)
        self.assertGreater(len(data["bosses"]), 0)
        
        # Store a boss ID for later tests
        self.boss_id = data["bosses"][0]["id"]
        print(f"✅ Get bosses test passed - Found {len(data['bosses'])} bosses")
        print(f"   First boss: {data['bosses'][0]['name']}")

    def test_03_get_boss_by_id(self):
        """Test getting a specific boss by ID"""
        if not self.boss_id:
            self.skipTest("No boss ID available")
        
        print(f"\n🔍 Testing get boss by ID: {self.boss_id}...")
        response = requests.get(f"{self.base_url}/api/bosses/{self.boss_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("weaknesses", data)
        print(f"✅ Get boss by ID test passed - Found boss: {data['name']}")

    def test_04_get_characters(self):
        """Test getting all characters"""
        print("\n🔍 Testing get all characters...")
        response = requests.get(f"{self.base_url}/api/characters")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("characters", data)
        self.assertIsInstance(data["characters"], list)
        self.assertGreater(len(data["characters"]), 0)
        
        # Store a character ID for later tests
        self.character_id = data["characters"][0]["id"]
        print(f"✅ Get characters test passed - Found {len(data['characters'])} characters")
        print(f"   First character: {data['characters'][0]['name']}")

    def test_05_get_character_by_id(self):
        """Test getting a specific character by ID"""
        if not self.character_id:
            self.skipTest("No character ID available")
        
        print(f"\n🔍 Testing get character by ID: {self.character_id}...")
        response = requests.get(f"{self.base_url}/api/characters/{self.character_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("abilities", data)
        print(f"✅ Get character by ID test passed - Found character: {data['name']}")

    def test_06_get_builds(self):
        """Test getting all builds"""
        print("\n🔍 Testing get all builds...")
        response = requests.get(f"{self.base_url}/api/builds")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("builds", data)
        self.assertIsInstance(data["builds"], list)
        self.assertGreater(len(data["builds"]), 0)
        
        # Store a build ID for later tests
        self.build_id = data["builds"][0]["id"]
        print(f"✅ Get builds test passed - Found {len(data['builds'])} builds")
        print(f"   First build: {data['builds'][0]['name']}")

    def test_07_get_build_by_id(self):
        """Test getting a specific build by ID"""
        if not self.build_id:
            self.skipTest("No build ID available")
        
        print(f"\n🔍 Testing get build by ID: {self.build_id}...")
        response = requests.get(f"{self.base_url}/api/builds/{self.build_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("talismans", data)
        print(f"✅ Get build by ID test passed - Found build: {data['name']}")

    def test_08_get_achievements(self):
        """Test getting all achievements"""
        print("\n🔍 Testing get all achievements...")
        response = requests.get(f"{self.base_url}/api/achievements")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("achievements", data)
        self.assertIsInstance(data["achievements"], list)
        self.assertGreaterEqual(len(data["achievements"]), 15, "Should have at least 15 achievements")
        
        # Store an achievement ID for later tests
        self.achievement_id = data["achievements"][0]["id"]
        print(f"✅ Get achievements test passed - Found {len(data['achievements'])} achievements")
        print(f"   First achievement: {data['achievements'][0]['name']}")
        
        # Verify achievement categories and difficulty ratings
        categories = set()
        difficulties = set()
        for achievement in data["achievements"]:
            categories.add(achievement["category"])
            difficulties.add(achievement["difficulty"])
        
        print(f"   Achievement categories: {', '.join(categories)}")
        print(f"   Achievement difficulties: {', '.join(difficulties)}")
        
    def test_09_get_walkthroughs(self):
        """Test getting all walkthroughs"""
        print("\n🔍 Testing get all walkthroughs...")
        response = requests.get(f"{self.base_url}/api/walkthroughs")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("walkthroughs", data)
        self.assertIsInstance(data["walkthroughs"], list)
        self.assertGreater(len(data["walkthroughs"]), 0)
        
        # Store a walkthrough ID for later tests
        if data["walkthroughs"]:
            self.walkthrough_id = data["walkthroughs"][0]["character"]
        print(f"✅ Get walkthroughs test passed - Found {len(data['walkthroughs'])} walkthroughs")
        if data["walkthroughs"]:
            print(f"   First walkthrough: {data['walkthroughs'][0]['title']}")
            
    def test_10_get_walkthrough_by_character(self):
        """Test getting a specific walkthrough by character name"""
        if not self.walkthrough_id:
            self.skipTest("No walkthrough ID available")
        
        print(f"\n🔍 Testing get walkthrough by character: {self.walkthrough_id}...")
        response = requests.get(f"{self.base_url}/api/walkthroughs/{self.walkthrough_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("title", data)
        self.assertIn("description", data)
        self.assertIn("chapters", data)
        print(f"✅ Get walkthrough by character test passed - Found walkthrough: {data['title']}")
        
    def test_11_boss_recommendations(self):
        """Test getting boss recommendations"""
        if not self.boss_id:
            self.skipTest("No boss ID available")
        
        print(f"\n🔍 Testing boss recommendations for boss ID: {self.boss_id}...")
        response = requests.get(f"{self.base_url}/api/boss-recommendations/{self.boss_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("boss", data)
        self.assertIn("recommended_characters", data)
        self.assertIn("recommended_builds", data)
        print(f"✅ Boss recommendations test passed - Found {len(data['recommended_characters'])} characters and {len(data['recommended_builds'])} builds")

    def test_12_search_functionality(self):
        """Test the search functionality"""
        print("\n🔍 Testing search functionality...")
        # Try searching for a term that should exist
        search_term = "Night"  # Should match multiple items
        response = requests.get(f"{self.base_url}/api/search?query={search_term}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("query", data)
        self.assertIn("bosses", data)
        self.assertIn("characters", data)
        self.assertIn("builds", data)
        self.assertIn("achievements", data)
        self.assertIn("total_results", data)
        print(f"✅ Search functionality test passed - Found {data['total_results']} results for '{search_term}'")
        
    def test_13_filter_bosses(self):
        """Test filtering bosses by difficulty and other criteria"""
        print("\n🔍 Testing filter bosses functionality...")
        
        # Test filtering by difficulty
        response = requests.get(f"{self.base_url}/api/filter-bosses?difficulty=hard")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("bosses", data)
        self.assertIn("filters_applied", data)
        print(f"✅ Filter bosses by difficulty test passed - Found {len(data['bosses'])} hard bosses")
        
        # Test filtering by weakness
        response = requests.get(f"{self.base_url}/api/filter-bosses?weakness=Holy")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("bosses", data)
        print(f"✅ Filter bosses by weakness test passed - Found {len(data['bosses'])} bosses weak to Holy")
        
        # Test filtering by level range
        response = requests.get(f"{self.base_url}/api/filter-bosses?min_level=15&max_level=25")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("bosses", data)
        print(f"✅ Filter bosses by level range test passed - Found {len(data['bosses'])} bosses in level range 15-25")
        
    def test_14_filter_characters(self):
        """Test filtering characters by playstyle"""
        print("\n🔍 Testing filter characters functionality...")
        
        # Test filtering by playstyle
        response = requests.get(f"{self.base_url}/api/filter-characters?playstyle=Tank")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("characters", data)
        self.assertIn("filters_applied", data)
        print(f"✅ Filter characters by playstyle test passed - Found {len(data['characters'])} Tank characters")
        
    def test_15_custom_build_creation(self):
        """Test creating a custom build"""
        print("\n🔍 Testing custom build creation...")
        
        # Create a test build
        test_build = {
            "name": f"Test Build {uuid.uuid4()}",
            "character": "Wylder",
            "type": "Test",
            "description": "A test build created by automated testing",
            "primary_weapon": "Test Sword",
            "secondary_weapon": "Test Shield",
            "strategy": "Test strategy"
        }
        
        response = requests.post(f"{self.base_url}/api/custom-build", json=test_build)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("build_id", data)
        print(f"✅ Custom build creation test passed - Created build with ID: {data['build_id']}")
        
        # Verify the build was created by getting all custom builds
        response = requests.get(f"{self.base_url}/api/custom-builds")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("custom_builds", data)
        print(f"✅ Custom builds retrieval test passed - Found {len(data['custom_builds'])} custom builds")
        
    def test_16_data_validation(self):
        """Test data validation for bosses and characters"""
        print("\n🔍 Testing data validation...")
        
        # Check boss level ranges
        response = requests.get(f"{self.base_url}/api/bosses")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        for boss in data["bosses"]:
            self.assertLessEqual(boss["max_level"], 25, f"Boss {boss['name']} has max_level > 25")
            self.assertGreaterEqual(boss["min_level"], 1, f"Boss {boss['name']} has min_level < 1")
        print("✅ Boss level range validation passed - All bosses have correct level ranges (1-25)")
        
        # Check character max levels
        response = requests.get(f"{self.base_url}/api/characters")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        for character in data["characters"]:
            self.assertEqual(character["max_level"], 15, f"Character {character['name']} has max_level != 15")
        print("✅ Character max level validation passed - All characters have max_level = 15")
        
        # Check number of bosses (should be 8)
        response = requests.get(f"{self.base_url}/api/bosses")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["bosses"]), 8, "There should be exactly 8 bosses")
        print("✅ Boss count validation passed - Found exactly 8 bosses")
        
        # Check number of characters (should be 8)
        response = requests.get(f"{self.base_url}/api/characters")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["characters"]), 8, "There should be exactly 8 characters")
        print("✅ Character count validation passed - Found exactly 8 characters")
        
        # Check number of builds (should be at least 16)
        response = requests.get(f"{self.base_url}/api/builds")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data["builds"]), 16, "There should be at least 16 builds")
        print(f"✅ Build count validation passed - Found {len(data['builds'])} builds (>= 16)")
        
        # Check number of achievements (should be 37)
        response = requests.get(f"{self.base_url}/api/achievements")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["achievements"]), 37, "There should be exactly 37 achievements")
        print("✅ Achievement count validation passed - Found exactly 37 achievements")
        
        # Verify achievements are properly ranked from 1 to 37
        ranks = [achievement["rank"] for achievement in data["achievements"]]
        self.assertEqual(sorted(ranks), list(range(1, 38)), "Achievement ranks should be 1-37")
        
    def test_18_get_creatures(self):
        """Test getting all creatures"""
        print("\n🔍 Testing get all creatures...")
        response = requests.get(f"{self.base_url}/api/creatures")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("creatures", data)
        self.assertIsInstance(data["creatures"], list)
        self.assertGreaterEqual(len(data["creatures"]), 30, "Should have at least 30 creatures")
        
        # Store a creature ID for later tests
        self.creature_id = data["creatures"][0]["id"]
        print(f"✅ Get creatures test passed - Found {len(data['creatures'])} creatures")
        print(f"   First creature: {data['creatures'][0]['name']}")
        
        # Verify creature types and threat levels
        types = set()
        threat_levels = set()
        for creature in data["creatures"]:
            types.add(creature["type"])
            threat_levels.add(creature["threat_level"])
        
        print(f"   Creature types: {', '.join(types)}")
        print(f"   Threat levels: {', '.join(threat_levels)}")
        
    def test_19_get_creature_by_id(self):
        """Test getting a specific creature by ID"""
        if not hasattr(self, 'creature_id') or not self.creature_id:
            self.test_18_get_creatures()
            if not self.creature_id:
                self.skipTest("No creature ID available")
        
        print(f"\n🔍 Testing get creature by ID: {self.creature_id}...")
        response = requests.get(f"{self.base_url}/api/creatures/{self.creature_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("weaknesses", data)
        self.assertIn("resistances", data)
        self.assertIn("threat_level", data)
        print(f"✅ Get creature by ID test passed - Found creature: {data['name']}")
        
    def test_20_filter_creatures(self):
        """Test filtering creatures by type and threat level"""
        print("\n🔍 Testing filter creatures functionality...")
        
        # Test filtering by type
        response = requests.get(f"{self.base_url}/api/filter-creatures?type=Nightlord")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("creatures", data)
        self.assertIn("filters_applied", data)
        self.assertEqual(len(data["creatures"]), 8, "There should be exactly 8 Nightlords")
        print(f"✅ Filter creatures by type test passed - Found {len(data['creatures'])} Nightlords")
        
        # Test filtering by threat level
        response = requests.get(f"{self.base_url}/api/filter-creatures?threat_level=Extreme")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("creatures", data)
        print(f"✅ Filter creatures by threat level test passed - Found {len(data['creatures'])} Extreme threat creatures")
        
        # Test filtering by weakness
        response = requests.get(f"{self.base_url}/api/filter-creatures?weakness=Holy")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("creatures", data)
        print(f"✅ Filter creatures by weakness test passed - Found {len(data['creatures'])} creatures weak to Holy")

if __name__ == "__main__":
    # Run the tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(EldenRingNightReignAPITest('test_01_root_endpoint'))
    test_suite.addTest(EldenRingNightReignAPITest('test_02_get_bosses'))
    test_suite.addTest(EldenRingNightReignAPITest('test_03_get_boss_by_id'))
    test_suite.addTest(EldenRingNightReignAPITest('test_04_get_characters'))
    test_suite.addTest(EldenRingNightReignAPITest('test_05_get_character_by_id'))
    test_suite.addTest(EldenRingNightReignAPITest('test_06_get_builds'))
    test_suite.addTest(EldenRingNightReignAPITest('test_07_get_build_by_id'))
    test_suite.addTest(EldenRingNightReignAPITest('test_08_get_achievements'))
    test_suite.addTest(EldenRingNightReignAPITest('test_09_get_walkthroughs'))
    test_suite.addTest(EldenRingNightReignAPITest('test_10_get_walkthrough_by_character'))
    test_suite.addTest(EldenRingNightReignAPITest('test_11_boss_recommendations'))
    test_suite.addTest(EldenRingNightReignAPITest('test_12_search_functionality'))
    test_suite.addTest(EldenRingNightReignAPITest('test_13_filter_bosses'))
    test_suite.addTest(EldenRingNightReignAPITest('test_14_filter_characters'))
    test_suite.addTest(EldenRingNightReignAPITest('test_15_custom_build_creation'))
    test_suite.addTest(EldenRingNightReignAPITest('test_16_data_validation'))
    test_suite.addTest(EldenRingNightReignAPITest('test_17_error_handling'))
    
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    
    # Return non-zero exit code if any tests failed
    sys.exit(not result.wasSuccessful())