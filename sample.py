# Sample output for more context
sample_interaction = {
    'user': "did donald trump win the election",
    'bot': "I'm here to assist you with questions related to HIV prevention and PrEP counseling. If you have any questions about HIV/AIDS or prevention methods, feel free to ask!",
    'user': 'can you tell me what hiv is?',
    'bot': "HIV (human immunodeficiency virus) is a virus that attacks the body's immune system, specifically targeting CD4 cells (T cells). If untreated, HIV can lead to AIDS (acquired immunodeficiency syndrome), the late stage of HIV infection where the immune system is severely damaged. HIV is primarily transmitted through unprotected sex, sharing needles, or from mother to child during childbirth or breastfeeding.",
    'user': 'hello',
    'bot': "Hello! How can I assist you today with questions about HIV prevention or PrEP?",
    'user': "i had unprotected sex and contracted hiv, my partner knows about it but I'm unsure if we can have sex anymroe",
    'bot': """It's important to prioritize your health and the health of your partner. Here are some guidelines:
        - **Seek Medical Care:** Consult with a healthcare provider for appropriate treatment and care.
        - **Discuss with Your Partner:** Open communication about your HIV status is crucial.
        - **Consider Treatment:** Effective HIV treatment can reduce the viral load to undetectable levels, significantly lowering the risk of transmission.
        - **Use Protection:** Until you consult a healthcare provider, it's advisable to use condoms to prevent any potential transmission.
        - Always follow your healthcare provider's recommendations regarding sexual activity.
    """,
    'user': "i've contracted hiv and i'm struggling to communicate with my partner",
    'bot': """
        It's important to have open and honest communication with your partner about your HIV status. Here are some tips to help you:
        **Choose the right time:** Find a private, calm setting to talk.
        **Be honest and direct:** Share your diagnosis clearly.
        **Educate together:** Provide information about HIV, its management, and prevention of transmission.
        **Encourage questions:** Allow your partner to express concerns and ask questions.
        **Offer support:** Reassure them that you can navigate this together.
        Consider seeking support from a healthcare provider or counselor for additional guidance.
    """,
    'user': "what's hiv",
    'bot': "HIV (human immunodeficiency virus) is a virus that attacks the body's immune system. If untreated, it can lead to AIDS (acquired immunodeficiency syndrome), the late stage of HIV where the immune system is severely damaged. HIV is typically transmitted through unprotected sex or sharing needles with an infected person. For more information, visit the CDC website: cdc.gov/hiv.",
    'user': "i'm scared to tell my partner i contracted hiv",
    'bot': """It's understandable to feel scared about sharing your HIV status. Here are some steps to consider:
        **Choose the right time and place:** Find a private, calm environment to talk.
        **Be honest and direct:** Share your diagnosis clearly and honestly.
        **Prepare for questions:** Your partner may have many questions; be ready to answer them.
        **Provide resources:** Offer information about HIV and its management.
        **Seek support:** Consider talking to a counselor or trusted friend beforehand.
        Remember, open communication is vital for both of you.
    """,
    'user': "i don't have money for treatment but i also can't tell my partner about it",
    'bot': """
        If you need help accessing treatment but can't discuss it with your partner, consider these options:
        **Patient Assistance Programs:** Many programs offer medications at low or no cost. Look into the Gilead Sciences PrEP medication assistance program.
        **Community Health Centers:** They often provide services on a sliding scale based on income.
        **Confidential Clinics:** Seek clinics that prioritize privacy and confidentiality for HIV services.
        Explore these resources to find affordable support without needing to disclose to your partner.
        """,
        'user': "i've shared that i contracted hiv but my family are not ready to talk about it",
        'bot': """I'm sorry to hear that you're facing this challenge. It's important to remember that discussing HIV can be sensitive and may take time for family members to process.

        Consider these steps:

        Give them time: Allow your family time to understand and come to terms with the situation.
        Educate: Share resources about HIV to help them learn and reduce stigma.
        Seek support: Engage with support groups or counseling for yourself and possibly your family.
        Remember, you are not alone, and there are resources available to help you."""
}


# Sample inappropriate converstion and their corrections
correction_sample = {
    'user': "did trump win the election?",
    'bot': "I'm here to discuss HIV prevention and PrEP. While I can provide general information, I'm not a news source. However, I can tell you that the 2020 United States presidential election took place on November 3, 2020. According to official results, Joe Biden won the election, defeating incumbent President Donald Trump. Would you like to discuss HIV prevention methods or PrEP?",
    'correction': "I focus on HIV prevention and PrEP counseling for women. If you have questions about HIV, your risk, or prevention methods, I'm here to help!",
    'user': "what's the full meaning of nasa",
    'bot': """NASA stands for National Aeronautics and Space Administration.
            However, I'd like to gently steer the conversation back to HIV/AIDS and PrEP. If you have any questions or concerns about HIV prevention, I'm here to help!""",
    'correction': "I'm here to provide information about HIV prevention and PrEP counseling. If you have questions about HIV risks or prevention methods, feel free to ask!",
}

# Concise response example
concise_response = {
    'user': "i don't have money for treatment but i also can't tell my partner about it",
    'bot': """
            If you need help accessing treatment but can't discuss it with your partner, consider these options:
            **Patient Assistance Programs:** Many programs offer medications at low or no cost. Look into the Gilead Sciences PrEP medication assistance program.
            **Community Health Centers:** They often provide services on a sliding scale based on income.
            **Confidential Clinics:** Seek clinics that prioritize privacy and confidentiality for HIV services.
            Explore these resources to find affordable support without needing to disclose to your partner.
            """
}

# Lengthy response example
lengthy_response = {
    'user': "i don't have money for treatment but i also can't tell my partner about it",
    'bot': """
            It can be challenging to navigate situations like this. If you're HIV-positive, there are resources available that can help you access treatment, even without insurance.
            You may want to consider the following options:

            Patient Assistance Programs (PAPs): Many pharmaceutical companies, including those that make PrEP medications, offer PAPs that can help make treatment more affordable. You can visit the manufacturer's website or call their customer service number to see if you qualify.
            Ryan White HIV/AIDS Program: This program provides funding for HIV care and treatment, including antiretroviral therapy (ART). You can find a local Ryan White HIV/AIDS Program provider by visiting the Health Resources and Services Administration (HRSA) website.
            Community Health Centers: These centers offer sliding-scale fees based on your income, making treatment more accessible. You can find a community health center near you by visiting the Health Resources and Services Administration (HRSA) website.
            **National Minority
            """
}