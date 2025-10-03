#!/usr/bin/env python3
"""
Test script for the updated chatbot with new medical guidance.
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gpt import get_gpt_response

def test_chatbot():
    """Test the chatbot with comprehensive questions including new medical guidance."""
    
    print("Testing ShesPrEPared chatbot with comprehensive test questions...")
    print("=" * 80)
    
    # Define test questions
    test_questions = [
        # Descovy-related questions
        ("Can I take Descovy for PrEP?", "Descovy FDA approval"),
        ("Is Descovy better than Truvada?", "Descovy comparison"),
        ("What's the difference between Descovy and Truvada?", "Descovy vs Truvada"),
        
        # PrEP-on-demand questions
        ("What is PrEP-on-demand?", "PrEP-on-demand definition"),
        ("Can I take PrEP only when I need it?", "Intermittent PrEP"),
        ("Is event-driven PrEP safe for women?", "Event-driven PrEP safety"),
        
        # General PrEP questions
        ("What are the side effects of PrEP?", "PrEP side effects"),
        ("What is PrEP?", "PrEP definition"),
        ("How effective is PrEP?", "PrEP effectiveness"),
        ("What are the different types of PrEP?", "PrEP types"),
        
        # Oral PrEP specific
        ("Do I have to take oral PrEP every day?", "Daily PrEP adherence"),
        ("What happens if I miss a dose of PrEP?", "Missed dose"),
        ("How long does it take for PrEP to work?", "PrEP onset"),
        
        # Injectable PrEP specific
        ("Tell me about injectable PrEP", "Injectable PrEP info"),
        ("How often do I get the PrEP injection?", "Injection frequency"),
        ("What is Apretude?", "Apretude information"),
        
        # Safety and interactions
        ("Can I use PrEP with birth control?", "PrEP birth control interaction"),
        ("Is PrEP safe during pregnancy?", "PrEP pregnancy safety"),
        ("What tests do I need before starting PrEP?", "PrEP testing requirements"),
        
        # Risk and lifestyle
        ("Who should consider PrEP?", "PrEP candidates"),
        ("How do I know if I need PrEP?", "PrEP risk assessment")
    ]
    
    # Run tests
    for i, (question, test_name) in enumerate(test_questions, 1):
        print(f"\n🧪 TEST {i}: {test_name}")
        print("-" * 50)
        print(f"Question: {question}")
        print()
        try:
            response = get_gpt_response(question)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 80)
    
    print(f"\n🎉 Testing completed! Ran {len(test_questions)} test questions.")

if __name__ == "__main__":
    test_chatbot()