from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


def get_org(db: Session, org: str):
    return db.query(models.Org).filter(models.Org.name == org).first()

def create_org(db: Session, org: schemas.OrgCreate):    
    db_repo = models.Org(name=org.name, repos=org.repos, created_at = org.created_at, updated_at = org.updated_at)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo

def update_org(db: Session, org: schemas.Org, repos: str):    
    setattr(org, 'repos', repos)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org