import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import SessionLocal
from repos import crud, models, schemas
from datetime import datetime, timedelta, timezone

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def request_repos_api(org_name: str, page: int = 1):
    r = requests.get(f'https://api.github.com/orgs/{org_name}/repos?per_page=100&sort=updated&page={page}', headers={'Authorization': f'Bearer {settings.GITHUB_REST_API_KEY}'})
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail="Error about Github API")
    
    return r

def is_one_day_passed(a, b):
    time_difference = a - b
    days_difference = time_difference.days
    return days_difference >= 1

@router.get("/{org_name}")
def get_api(org_name:str, db: Session = Depends(get_db)):
    org = crud.get_org(db=db, org=org_name)
    if not org:
        response = request_repos_api(org_name)
        if response != False:
            org = schemas.OrgCreate(name=org_name, repos=response.text)
            return crud.create_org(db=db, org=org)
        return response
    else:
        if is_one_day_passed(datetime.now(timezone.utc), org.updated_at):
            repos = request_repos_api(org_name).text
            crud.update_org(db=db, org=org, repos=repos)
            return repos
    
    return org.repos