#!/usr/bin/env python3
"""
Test Script for Enhanced WhineAboutAI API
Tests all OpenAI-powered endpoints to ensure they work correctly
"""

import requests
import json
import os
import time
from typing import Dict, Any

class WhineAboutAITester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, response: Dict[Any, Any] = None, error: str = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "response": response,
            "error": error
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if error:
            print(f"   Error: {error}")
        if response and success:
            print(f"   Response: {str(response)[:100]}...")
        print()
    
    def test_health_check(self):
        """Test the health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, data)
                return True
            else:
                self.log_test("Health Check", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, error=str(e))
            return False
    
    def test_complaint_enhancement(self):
        """Test complaint enhancement with different styles"""
        test_complaint = "My smart speaker keeps playing the wrong music"
        styles = ["sarcastic", "dramatic", "absurd", "professional"]
        
        overall_success = True
        
        for style in styles:
            try:
                response = requests.post(
                    f"{self.base_url}/enhance-complaint",
                    json={"text": test_complaint, "style": style},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and data.get("enhanced"):
                        self.log_test(f"Complaint Enhancement ({style})", True, {
                            "original": data.get("original", "")[:50] + "...",
                            "enhanced": data.get("enhanced", "")[:50] + "...",
                            "style": data.get("style")
                        })
                    else:
                        self.log_test(f"Complaint Enhancement ({style})", False, error="No enhanced text returned")
                        overall_success = False
                else:
                    self.log_test(f"Complaint Enhancement ({style})", False, error=f"Status code: {response.status_code}")
                    overall_success = False
                    
            except Exception as e:
                self.log_test(f"Complaint Enhancement ({style})", False, error=str(e))
                overall_success = False
        
        return overall_success
    
    def test_whinebot_chat(self):
        """Test the enhanced WhineBot chat"""
        test_messages = [
            "Why does autocorrect hate me?",
            "My AI assistant is dumber than a rock",
            "Can you help me feel better about AI failures?"
        ]
        
        conversation_id = f"test_{int(time.time())}"
        overall_success = True
        
        for i, message in enumerate(test_messages):
            try:
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={"message": message, "conversation_id": conversation_id},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and data.get("response"):
                        self.log_test(f"WhineBot Chat (Message {i+1})", True, {
                            "message": message[:30] + "...",
                            "response": data.get("response", "")[:50] + "...",
                            "conversation_id": data.get("conversation_id")
                        })
                    else:
                        self.log_test(f"WhineBot Chat (Message {i+1})", False, error="No response returned")
                        overall_success = False
                else:
                    self.log_test(f"WhineBot Chat (Message {i+1})", False, error=f"Status code: {response.status_code}")
                    overall_success = False
                    
            except Exception as e:
                self.log_test(f"WhineBot Chat (Message {i+1})", False, error=str(e))
                overall_success = False
                
            # Small delay between messages
            time.sleep(1)
        
        return overall_success
    
    def test_ai_fail_predictor(self):
        """Test AI fail prediction"""
        test_scenario = "Going to an important job interview tomorrow"
        
        try:
            response = requests.post(
                f"{self.base_url}/predict-fail",
                json={"scenario": test_scenario},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("prediction"):
                    self.log_test("AI Fail Predictor", True, {
                        "scenario": data.get("scenario", "")[:30] + "...",
                        "prediction": data.get("prediction", "")[:50] + "...",
                        "confidence": data.get("confidence")
                    })
                    return True
                else:
                    self.log_test("AI Fail Predictor", False, error="No prediction returned")
                    return False
            else:
                self.log_test("AI Fail Predictor", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("AI Fail Predictor", False, error=str(e))
            return False
    
    def test_comeback_generator(self):
        """Test comeback generation"""
        test_complaint = "Autocorrect changed 'meeting' to 'mating' in my work email"
        
        try:
            response = requests.post(
                f"{self.base_url}/generate-comeback",
                json={"complaint": test_complaint},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("comeback"):
                    self.log_test("Comeback Generator", True, {
                        "complaint": data.get("complaint", "")[:30] + "...",
                        "comeback": data.get("comeback", "")[:50] + "..."
                    })
                    return True
                else:
                    self.log_test("Comeback Generator", False, error="No comeback returned")
                    return False
            else:
                self.log_test("Comeback Generator", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Comeback Generator", False, error=str(e))
            return False
    
    def test_meme_generator(self):
        """Test meme text generation"""
        test_complaint = "My smart doorbell thinks I'm a burglar every morning"
        
        try:
            response = requests.post(
                f"{self.base_url}/create-meme",
                json={"complaint": test_complaint},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and (data.get("top_text") or data.get("bottom_text")):
                    self.log_test("Meme Generator", True, {
                        "top_text": data.get("top_text", "")[:30] + "...",
                        "bottom_text": data.get("bottom_text", "")[:30] + "...",
                        "meme_type": data.get("meme_type")
                    })
                    return True
                else:
                    self.log_test("Meme Generator", False, error="No meme text returned")
                    return False
            else:
                self.log_test("Meme Generator", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Meme Generator", False, error=str(e))
            return False
    
    def test_battle_commentary(self):
        """Test complaint battle commentary"""
        complaint1 = "AI autocorrect ruined my love letter"
        complaint2 = "Smart doorbell locked me out of my own house"
        
        try:
            response = requests.post(
                f"{self.base_url}/battle-commentary",
                json={"complaint1": complaint1, "complaint2": complaint2},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("commentary"):
                    self.log_test("Battle Commentary", True, {
                        "commentary": data.get("commentary", "")[:100] + "..."
                    })
                    return True
                else:
                    self.log_test("Battle Commentary", False, error="No commentary returned")
                    return False
            else:
                self.log_test("Battle Commentary", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Battle Commentary", False, error=str(e))
            return False
    
    def test_stats_endpoint(self):
        """Test the stats endpoint"""
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Stats Endpoint", True, data)
                return True
            else:
                self.log_test("Stats Endpoint", False, error=f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Stats Endpoint", False, error=str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🧪 Starting WhineAboutAI API Tests...")
        print("=" * 50)
        
        # Check if OpenAI API key is set
        if not os.getenv('OPENAI_API_KEY'):
            print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
            print("   Some tests may fail or use fallback responses")
            print()
        
        # Run all tests
        tests = [
            self.test_health_check,
            self.test_stats_endpoint,
            self.test_complaint_enhancement,
            self.test_whinebot_chat,
            self.test_ai_fail_predictor,
            self.test_comeback_generator,
            self.test_meme_generator,
            self.test_battle_commentary
        ]
        
        start_time = time.time()
        
        for test in tests:
            test()
        
        end_time = time.time()
        
        # Summary
        print("=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Total Time: {end_time - start_time:.2f} seconds")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result['error']}")
        
        print("\n🎯 Next Steps:")
        if failed_tests == 0:
            print("   ✅ All tests passed! Your API is ready to go!")
            print("   🚀 Start the frontend and begin testing the UI")
        else:
            print("   🔧 Fix the failing tests before proceeding")
            print("   📝 Check server logs for more detailed error information")
            if not os.getenv('OPENAI_API_KEY'):
                print("   🔑 Make sure to set your OPENAI_API_KEY environment variable")
        
        return failed_tests == 0

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test WhineAboutAI Enhanced API')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Base URL for the API (default: http://localhost:5000)')
    parser.add_argument('--output', help='Save test results to JSON file')
    
    args = parser.parse_args()
    
    tester = WhineAboutAITester(args.url)
    success = tester.run_all_tests()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(tester.test_results, f, indent=2)
        print(f"\n💾 Test results saved to {args.output}")
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main()