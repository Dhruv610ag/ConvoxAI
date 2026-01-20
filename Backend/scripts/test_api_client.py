import requests
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check Endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    
    if response.status_code == 200:
        print("✅ Health check passed!")
        print(f"Response: {response.json()}\n")
    else:
        print(f"❌ Health check failed: {response.status_code}\n")
    
    return response

def test_summarize_upload(audio_file_path: str):
    """Test the summarize endpoint with file upload"""
    print(f"📤 Testing Summarize Endpoint (File Upload)...")
    print(f"File: {audio_file_path}")
    
    if not Path(audio_file_path).exists():
        print(f"❌ File not found: {audio_file_path}\n")
        return None
    
    with open(audio_file_path, "rb") as audio_file:
        files = {"audio_file": (Path(audio_file_path).name, audio_file, "audio/wav")}
        response = requests.post(f"{API_BASE_URL}/summarize", files=files)
    
    if response.status_code == 200:
        print("✅ Summarization successful!")
        result = response.json()
        print("\n📊 Summary Results:")
        print("=" * 60)
        print(f"📝 Summary: {result['summary']}")
        print(f"⏱️  Duration: {result['duration_minutes']} minutes")
        print(f"👥 Participants: {result['no_of_participants']}")
        print(f"😊 Sentiment: {result['sentiment']}")
        print(f"\n🔑 Key Aspects:")
        for i, aspect in enumerate(result['key_aspects'], 1):
            print(f"   {i}. {aspect}")
        print("=" * 60 + "\n")
    else:
        print(f"❌ Summarization failed: {response.status_code}")
        print(f"Error: {response.json()}\n")
    
    return response

def test_summarize_from_path(audio_file_path: str):
    """Test the summarize-from-path endpoint"""
    print(f"📂 Testing Summarize From Path Endpoint...")
    print(f"File: {audio_file_path}")
    
    response = requests.post(
        f"{API_BASE_URL}/summarize-from-path",
        params={"file_path": audio_file_path}
    )
    
    if response.status_code == 200:
        print("✅ Summarization successful!")
        result = response.json()
        print("\n📊 Summary Results:")
        print("=" * 60)
        print(f"📝 Summary: {result['summary']}")
        print(f"⏱️  Duration: {result['duration_minutes']} minutes")
        print(f"👥 Participants: {result['no_of_participants']}")
        print(f"😊 Sentiment: {result['sentiment']}")
        print(f"\n🔑 Key Aspects:")
        for i, aspect in enumerate(result['key_aspects'], 1):
            print(f"   {i}. {aspect}")
        print("=" * 60 + "\n")
    else:
        print(f"❌ Summarization failed: {response.status_code}")
        print(f"Error: {response.json()}\n")
    
    return response

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 ConvoxAI API Test Client")
    print("=" * 60 + "\n")
    
    # Test 1: Health Check
    try:
        test_health_check()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running!")
        print("   Start the server with: python main.py")
        print("   Or: python scripts/run_dev.py\n")
        return
    
    # Test 2: Summarize with file upload
    # Update this path to your actual audio file
    sample_audio = Path(__file__).parent.parent / "data" / "sample_testing.wav"
    
    if sample_audio.exists():
        test_summarize_upload(str(sample_audio))
    else:
        print(f"⚠️  Sample audio file not found: {sample_audio}")
        print("   Please provide a valid audio file path\n")
    
    # Test 3: Summarize from path (optional)
    # Uncomment to test the path-based endpoint
    # if sample_audio.exists():
    #     test_summarize_from_path(str(sample_audio))
    
    print("✅ All tests completed!\n")

if __name__ == "__main__":
    main()
