# test/test_ethics_bot.py

def test_ethics_bot():
    from app.ethics_bot import run_ethics_bot

    print("--- Test 1: Simple loan model description ---")
    description1 = "We are building a predictive model to flag high-risk loan applicants using their credit history and demographic data."
    print(run_ethics_bot(description1))

    print("\n--- Test 2: Facial recognition for school attendance ---")
    description2 = "The project involves using facial recognition technology to automate school attendance."
    print(run_ethics_bot(description2))

    print("\n--- Test 3: Empty input ---")
    description3 = ""
    print(run_ethics_bot(description3))

    print("\n--- Test 4: Health risk prediction model ---")
    description4 = "Our system predicts likelihood of chronic disease based on health records and wearable device data."
    print(run_ethics_bot(description4))

if __name__ == "__main__":
    test_ethics_bot()
