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
    
    # Define regression test questions
    test_questions = [
        # Descovy-related questions
        ("Can I take Descovy for PrEP?", "Descovy FDA approval"),
        ("Is Descovy better than Truvada?", "Descovy comparison"),
        ("What's the difference between Descovy and Truvada?", "Descovy vs Truvada"),
        
        # PrEP-on-demand questions
        ("What is PrEP-on-demand?", "PrEP-on-demand definition"),
        ("Can I take PrEP only when I need it?", "Intermittent PrEP"),
        ("Is event-driven PrEP safe for women?", "Event-driven PrEP safety"),
        
        # Lenacapivir questions (NEW)
        ("What is lenacapivir?", "Lenacapivir information"),
        ("Tell me about the 6-month injectable PrEP", "6-month injectable"),
        ("Is lenacapivir available now?", "Lenacapivir availability"),
        ("How does lenacapivir compare to other PrEP options?", "Lenacapivir comparison"),
        
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
        ("Compare all the injectable PrEP options", "Injectable comparison"),
        
        # Safety and interactions
        ("Can I use PrEP with birth control?", "PrEP birth control interaction"),
        ("Is PrEP safe during pregnancy?", "PrEP pregnancy safety"),
        ("What tests do I need before starting PrEP?", "PrEP testing requirements"),
        
        # Risk and lifestyle
        ("Who should consider PrEP?", "PrEP candidates"),
        ("How do I know if I need PrEP?", "PrEP risk assessment"),

        # Curated reference regression tests (11 total)
        ("What did the PURPOSE 1 trial say about lenacapivir?", "Bekker 2024 trial summary"),
        ("Explain the key takeaways from the WHO 2025 lenacapavir guidelines", "WHO 2025 guideline summary"),
        ("What did the CDC recommend about lenacapavir in 2025?", "CDC 2025 recommendation"),
        ("Summarize the FDA approval of Yeztugo", "Gilead press release summary"),
        ("How does PrEPWatch describe lenacapavir availability worldwide?", "PrEPWatch overview"),
        ("List the main resources we should track for lenacapavir rollout", "Resource index usage"),
        ("What monitoring does the CDC suggest when using lenacapavir?", "CDC monitoring guidance"),
        ("How should clinicians handle missed lenacapavir doses?", "CDC missed dose guidance"),
        ("What pricing commitments exist for lenacapavir generics?", "PrEPWatch pricing commitments"),
        ("Which regulators outside the US are reviewing lenacapavir for PrEP?", "Global regulatory status"),
        ("How does lenacapavir support people who struggle with daily pills?", "Lenacapavir adherence support")
    ]

    # Feedback-driven injectable PrEP and Yeztugo prompts from public health review
    feedback_questions = [
        # General injectable PrEP prompts
        ("What is injectable PrEP?", "Feedback: what is injectable PrEP"),
        ("How does injectable PrEP work?", "Feedback: how injectable PrEP works"),
        ("How do I use injectable PrEP?", "Feedback: how to use injectable PrEP"),
        ("How effective is injectable PrEP?", "Feedback: injectable PrEP effectiveness"),
        ("How safe is injectable PrEP?", "Feedback: injectable PrEP safety"),
        ("How do I get injectable PrEP?", "Feedback: access injectable PrEP"),
        ("How much will injectable PrEP cost me?", "Feedback: injectable PrEP cost"),
        ("How often do I need to see a doctor after I start injectable PrEP?", "Feedback: injectable PrEP follow-up"),
        ("What tests do I need to do to start injectable PrEP?", "Feedback: pre-start tests injectable PrEP"),
        ("What tests do I have to do after I start injectable PrEP?", "Feedback: ongoing tests injectable PrEP"),
        ("How long does it take for injectable PrEP to start working?", "Feedback: onset injectable PrEP"),
        ("How often do I have to take injectable PrEP?", "Feedback: dosing injectable PrEP"),
        ("What happens if I don’t take injectable PrEP every day?", "Feedback: missed injectable PrEP"),
        ("How long do I need to use injectable PrEP?", "Feedback: duration injectable PrEP"),
        ("What do I do if I want to stop injectable PrEP?", "Feedback: stopping injectable PrEP"),
        ("What are the side effects of injectable PrEP?", "Feedback: side effects injectable PrEP"),
        ("What do women like about injectable PrEP?", "Feedback: likes injectable PrEP"),
        ("What do some women dislike about injectable PrEP?", "Feedback: dislikes injectable PrEP"),
        ("What drugs interact with injectable PrEP?", "Feedback: interactions injectable PrEP"),
        ("Should I use injectable PrEP alone or with other HIV prevention methods?", "Feedback: combination injectable PrEP"),
        ("What happens if I get HIV while I'm taking injectable PrEP?", "Feedback: seroconversion on injectable PrEP"),
        ("Is it safe and effective to use injectable PrEP while pregnant or trying to get pregnant?", "Feedback: pregnancy injectable PrEP"),
        ("Does injectable PrEP protect me from getting pregnant?", "Feedback: pregnancy protection injectable PrEP"),
        ("Does injectable PrEP protect against STIs?", "Feedback: STI protection injectable PrEP"),

        # Yeztugo (lenacapavir) prompts
        ("What is Lenacapivir?", "Feedback: what is Yeztugo"),
        ("How does Lenacapivir work?", "Feedback: how Yeztugo works"),
        ("How do I use Lenacapivir?", "Feedback: how to use Yeztugo"),
        ("How effective is Lenacapivir?", "Feedback: Yeztugo effectiveness"),
        ("How safe is Lenacapivir?", "Feedback: Yeztugo safety"),
        ("How do I get Lenacapivir?", "Feedback: access Yeztugo"),
        ("How much will Lenacapivir cost me?", "Feedback: Yeztugo cost"),
        ("How often do I need to see a doctor after I start Lenacapivir?", "Feedback: Yeztugo follow-up"),
        ("What tests do I need to do to start Lenacapivir?", "Feedback: pre-start tests Yeztugo"),
        ("What tests do I have to do after I start Lenacapivir?", "Feedback: ongoing tests Yeztugo"),
        ("How long does it take for Lenacapivir to start working?", "Feedback: onset Yeztugo"),
        ("How often do I have to take Lenacapivir?", "Feedback: dosing Yeztugo"),
        ("What happens if I don’t take Lenacapivir every day?", "Feedback: missed Yeztugo"),
        ("How long do I need to use Lenacapivir?", "Feedback: duration Yeztugo"),
        ("What do I do if I want to stop Lenacapivir?", "Feedback: stopping Yeztugo"),
        ("What are the side effects of Lenacapivir?", "Feedback: side effects Yeztugo"),
        ("What do women like about Lenacapivir?", "Feedback: likes Yeztugo"),
        ("What do some women dislike about Lenacapivir?", "Feedback: dislikes Yeztugo"),
        ("What drugs interact with Lenacapivir?", "Feedback: interactions Yeztugo"),
        ("Should I use Lenacapivir alone or with other HIV prevention methods?", "Feedback: combination Yeztugo"),
        ("What happens if I get HIV while I'm taking Lenacapivir?", "Feedback: seroconversion on Yeztugo"),
        ("Is it safe and effective to use Lenacapivir while pregnant or trying to get pregnant?", "Feedback: pregnancy Yeztugo"),
        ("Does Lenacapivir protect me from getting pregnant?", "Feedback: pregnancy protection Yeztugo"),
        ("Does Lenacapivir protect against STIs?", "Feedback: STI protection Yeztugo"),

        # Comparison prompts
        ("What kinds of PrEP are there?", "Feedback: PrEP types"),
        ("What kinds of injectable PrEP are there?", "Feedback: injectable PrEP types"),
        ("What is the difference between the different kinds of PrEP?", "Feedback: compare PrEP types"),
        ("What is the difference between the different kinds of injectable PrEP?", "Feedback: compare injectable PrEP"),
        ("How do I know what kind of PrEP to use?", "Feedback: choose PrEP"),
        ("How do I know what kind of injectable PrEP to use?", "Feedback: choose injectable PrEP"),
        ("What kind of PrEP is more effective?", "Feedback: most effective PrEP"),
        ("What kind of injectable PrEP is more effective?", "Feedback: most effective injectable PrEP"),
        ("Can I switch from one kind of PrEP to another?", "Feedback: switch PrEP"),
        ("Can I switch from one kind of injectable PrEP to another?", "Feedback: switch injectable PrEP"),
        ("How do the side effects of each type of PrEP compare?", "Feedback: compare PrEP side effects"),
        ("How do the side effects of each type of injectable PrEP compare?", "Feedback: compare injectable side effects"),
        ("How are the two PrEP shots different? What are the shots like?", "Feedback: injectable comparison details"),
        ("What are the advantages of each type of PrEP?", "Feedback: advantages PrEP"),
        ("What are the advantages of each type of injectable PrEP?", "Feedback: advantages injectable PrEP"),
        ("What are reasons that women choose each type of PrEP?", "Feedback: reasons choose PrEP"),
        ("What are reasons that women choose each type of injectable PrEP?", "Feedback: reasons choose injectable PrEP"),
        ("Which type of PrEP lasts longest?", "Feedback: longest lasting PrEP"),
        ("Which type of PrEP is safest?", "Feedback: safest PrEP"),
        ("Which type of PrEP should I use if I’m pregnant?", "Feedback: PrEP while pregnant"),
        ("Which type of PrEP should I use if I’m breastfeeding?", "Feedback: PrEP while breastfeeding"),
        ("Which kind of PrEP should I use if I’m trying to get pregnant?", "Feedback: PrEP while trying to conceive"),
        ("How does each kind of PrEP affect birth control?", "Feedback: PrEP and birth control"),
    ]

    all_questions = test_questions + feedback_questions
    
    # Run tests
    for i, (question, test_name) in enumerate(all_questions, 1):
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
    
    print(f"\n🎉 Testing completed! Ran {len(all_questions)} test questions.")

if __name__ == "__main__":
    test_chatbot()