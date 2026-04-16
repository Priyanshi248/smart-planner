from datetime import datetime, timedelta

def recommend_time(priority):
    now = datetime.now()

    if priority == "high":
        recommended = now + timedelta(hours=1)
    elif priority == "medium":
        recommended = now + timedelta(hours=3)
    else:
        recommended = now + timedelta(hours=6)

    return recommended.strftime("%I:%M %p")
