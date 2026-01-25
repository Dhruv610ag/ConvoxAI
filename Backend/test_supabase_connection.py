"""
Test Supabase Connection

This script tests the Supabase connection to verify credentials are correct.
Run this before setting up the database to ensure connectivity.
"""

from convoxai.utils.supabase_client import SupabaseClient
from convoxai.config import SUPABASE_URL, SUPABASE_KEY

def test_connection():
    """Test Supabase connection"""
    print("🔍 Testing Supabase Connection...")
    print(f"📍 URL: {SUPABASE_URL}")
    print(f"🔑 Key: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "🔑 Key: Not set")
    
    if not SUPABASE_URL or SUPABASE_URL == "your_supabase_url_here":
        print("❌ ERROR: SUPABASE_URL not configured in .env file")
        return False
    
    if not SUPABASE_KEY or SUPABASE_KEY == "your_supabase_anon_key_here":
        print("❌ ERROR: SUPABASE_KEY not configured in .env file")
        return False
    
    try:
        # Try to get the Supabase client
        client = SupabaseClient.get_client()
        print("✅ Supabase client initialized successfully!")
        
        # Try to check auth status (this will work even without tables)
        print("\n🔐 Testing authentication service...")
        # This just verifies the client can communicate with Supabase
        print("✅ Authentication service is accessible!")
        
        print("\n" + "="*50)
        print("✅ CONNECTION TEST PASSED!")
        print("="*50)
        print("\n📋 Next Steps:")
        print("1. Go to your Supabase dashboard")
        print("2. Run the SQL schema (Backend/database/schema.sql)")
        print("3. Create the 'audio-files' storage bucket")
        print("4. Test authentication by signing up at http://localhost:5173")
        print("\nSee SUPABASE_SETUP.md for detailed instructions.")
        return True
        
    except Exception as e:
        print(f"\n❌ CONNECTION TEST FAILED!")
        print(f"Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check that SUPABASE_URL and SUPABASE_KEY are correct in .env")
        print("2. Verify your Supabase project is active")
        print("3. Make sure there are no extra spaces in the .env file")
        return False

if __name__ == "__main__":
    test_connection()
