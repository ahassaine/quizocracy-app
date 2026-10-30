"""Delete every family whose account email is on the test domain, with all its data."""
from conftest import DB

fams = {a["family_id"] for a in DB.accounts.find({"email": {"$regex": r"@example\.test$"}}, {"family_id": 1})}
pupils = [p["_id"] for p in DB.pupils.find({"family_id": {"$in": list(fams)}}, {"_id": 1})]
for c in ("maths_lab_q", "maths_attempts", "maths_mastery"):
    DB[c].delete_many({"pupil": {"$in": pupils}})
for c in ("accounts", "pupils", "sessions", "attempts", "tables_facts", "spelling_words", "verbs_state", "items"):
    DB[c].delete_many({"family_id": {"$in": list(fams)}})
DB.families.delete_many({"_id": {"$in": list(fams)}})
DB.outbox.delete_many({"to": {"$regex": r"@example\.test$"}})
DB.codes.delete_many({"email": {"$regex": r"@example\.test$"}})
DB.login_failures.delete_many({"email": {"$in": [f"pin:{p}" for p in pupils]}})
DB.login_failures.delete_many({"email": {"$regex": r"@example\.test$"}})
print(f"removed {len(fams)} test families and {len(pupils)} test children")
