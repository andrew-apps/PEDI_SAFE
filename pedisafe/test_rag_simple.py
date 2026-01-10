"""
Simple diagnostic script to test RAG engine initialization
Run this first to verify setup before running full test suite
"""

import sys
from pathlib import Path

print("=" * 60)
print("PediSafe RAG Engine Diagnostic")
print("=" * 60)

# Check knowledge directory
knowledge_path = Path(__file__).parent / "knowledge"
print(f"\n1. Checking knowledge directory: {knowledge_path}")
print(f"   Exists: {knowledge_path.exists()}")

if knowledge_path.exists():
    md_files = list(knowledge_path.glob("*.md"))
    print(f"   MD files found: {len(md_files)}")
    for f in md_files:
        print(f"      - {f.name}")
else:
    print("   ❌ ERROR: Knowledge directory not found!")
    sys.exit(1)

if not md_files:
    print("   ❌ ERROR: No .md files in knowledge directory!")
    sys.exit(1)

# Try to import RAG engine
print("\n2. Testing RAG engine import...")
try:
    from rag_engine import PediSafeRAG
    print("   ✅ RAG engine imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try to initialize RAG engine
print("\n3. Initializing RAG engine...")
try:
    api_key = "csk-59knkfwehxxxckxcdw8f56mjxj3v8f6hm3239rtnxwf6cmjf"
    engine = PediSafeRAG(
        api_key=api_key,
        knowledge_dir=str(knowledge_path),
        language="en",
        provider="cerebras"
    )
    print("   ✅ RAG engine initialized successfully")
except Exception as e:
    print(f"   ❌ Failed to initialize: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test a simple query
print("\n4. Testing simple query...")
try:
    response = engine.get_response("2 meses, 38.5°C")
    print("   ✅ Query executed successfully")
    print(f"\n   Response preview:\n   {response[:200]}...")
except Exception as e:
    print(f"   ❌ Query failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL DIAGNOSTICS PASSED!")
print("=" * 60)
print("\nYou can now run the full test suite:")
print("   python -m pytest test_pedisafe.py -v")
