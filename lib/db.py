<<<<<<< HEAD
import firebase_admin, os, json
from firebase_admin import credentials, firestore
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
ASTROLEARNJSON = "/etc/secrets/astrolearn_service_account.json"
if not os.path.exists(ASTROLEARNJSON):
    ASTROLEARNJSON = os.path.join(DATA_DIR, "astrolearn.json")

cred = credentials.Certificate(ASTROLEARNJSON)
app = firebase_admin.initialize_app(cred)
db = firestore.client(app)
schoolstuffs = db.collection('SchoolStuffs')

homeworks = schoolstuffs.document("homeworks")
exams = schoolstuffs.document("exams")
assigned_to_study = schoolstuffs.document("assignedtostudy")

def db_update_homework(subject, chapter, title, description, due):
    subject_homeworks = homeworks.get().to_dict().get(subject, [])
    subject_homeworks.append({
        "chapter": chapter,
        "homework_title": title,
        "description": description,
        "due": due  # Firestore will automatically convert this to a Firestore timestamp
    })
    homeworks.update({
        subject: subject_homeworks
    })

def remove_homework(subject, title):
    subject_homeworks = homeworks.get().to_dict().get(subject, [])
    updated_homeworks = [hw for hw in subject_homeworks if hw["homework_title"] != title]
    homeworks.update({
        subject: updated_homeworks
    })

def get_homeworks():
    homeworks_data = homeworks.get().to_dict()
    for subject, hw_list in homeworks_data.items():
        for hw in hw_list:
            if hasattr(hw["due"],"isoformat"):hw["due"] = hw["due"].isoformat()  # Convert datetime to ISO string for JSON serialization
    return homeworks_data
=======
import firebase_admin, os, json
from firebase_admin import credentials, firestore
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
ASTROLEARNJSON = "/etc/secrets/astrolearn_service_account.json"
if not os.path.exists(ASTROLEARNJSON):
    ASTROLEARNJSON = os.path.join(DATA_DIR, "astrolearn.json")

cred = credentials.Certificate(ASTROLEARNJSON)
app = firebase_admin.initialize_app(cred)
db = firestore.client(app)
schoolstuffs = db.collection('SchoolStuffs')

homeworks = schoolstuffs.document("homeworks")
exams = schoolstuffs.document("exams")
assigned_to_study = schoolstuffs.document("assignedtostudy")

def db_update_homework(subject, chapter, title, description, due):
    subject_homeworks = homeworks.get().to_dict().get(subject, [])
    subject_homeworks.append({
        "chapter": chapter,
        "homework_title": title,
        "description": description,
        "due": due  # Firestore will automatically convert this to a Firestore timestamp
    })
    homeworks.update({
        subject: subject_homeworks
    })

def remove_homework(subject, title):
    subject_homeworks = homeworks.get().to_dict().get(subject, [])
    updated_homeworks = [hw for hw in subject_homeworks if hw["homework_title"] != title]
    homeworks.update({
        subject: updated_homeworks
    })

def get_homeworks():
    homeworks_data = homeworks.get().to_dict()
    for subject, hw_list in homeworks_data.items():
        for hw in hw_list:
            if hasattr(hw["due"],"isoformat"):hw["due"] = hw["due"].isoformat()  # Convert datetime to ISO string for JSON serialization
    return homeworks_data
>>>>>>> 77990087da15310786318a82e2d150ed2cfa2a62
