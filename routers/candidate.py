from fastapi import APIRouter,HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from db.engine import db
from schemas.candidates import Candidates,CandidateObject, VerifyUser
from auth.oauth2 import get_current_user
from schemas.user import UserModel
from auth.hashing import Hasher
import pandas as pd
from starlette.responses import FileResponse
    
from bson import ObjectId

candidate_router = APIRouter(tags=["Candidate"])


@candidate_router.get("/candidate")
async def all_candidate(currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    candidates = []

    for i in db.candidates.find({"user_id":user.id}):
        candidates.append(Candidates(**i))
    return candidates


@candidate_router.post("/candidate/")
async def create_candidates(request: CandidateObject,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    candidate = db.candidates.find_one({"email":request.email})
    if candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Aleady Register!")

    insert_data = request.dict(exclude_unset=True)
    insert_data['UUID'] = Hasher.get_password_hash(insert_data['UUID'])
    insert_data['user_id'] = user.id
    db.candidates.insert_one(insert_data)
    return JSONResponse(content={}, status_code=201)


@candidate_router.put("/candidate/{id}")
async def update_candidate(id: str,request: CandidateObject,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    if candidate['email'] != request.email:
        candidate_email = db.candidates.find_one({"email":request.email})
        if candidate_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Email Aleady Register!")

    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    candidate_data = request.dict(exclude_unset=True)
    candidate_data['UUID'] = Hasher.get_password_hash(candidate_data['UUID'])
    candidate = db.candidates.find_one_and_update(
        {"_id":ObjectId(f"{id}")},
        {'$set':candidate_data}
    )
    return JSONResponse(content={}, status_code=200)


@candidate_router.get("/candidate/{id}")
async def get_one_candidate(id: str,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    candidate = Candidates(**candidate)
    return candidate 


@candidate_router.delete("/candidate/{id}")
async def delete_candidate(id: str,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    db.candidates.delete_one({"_id":ObjectId(f"{id}")})
    return JSONResponse(content={}, status_code=200)


@candidate_router.get("/all-candidates")
async def all_candidate(request:Request, currentuser: UserModel = Depends(get_current_user)):
    params = request.query_params._dict
    candidates = list()
    for i in db.candidates.find(params):
        candidates.append(Candidates(**i))

    return candidates


@candidate_router.get("/generate-report")
async def generate_report(currentuser: UserModel = Depends(get_current_user)):
    allCandidate = list(db.candidates.find())
    df = pd.DataFrame(allCandidate)
    filename = "candidate_report.csv"
    df.to_csv(filename)

    return FileResponse(filename, media_type='application/octet-stream',filename=filename)