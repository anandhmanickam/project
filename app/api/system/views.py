from sqlmodel import SQLModel, Session, select
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from db.models.models import Team
from api.system.schemas import TeamCreate, TeamRead, TeamUpdate
from db.db import async_engine, db_session


# Create Migrations

def create_db_and_tables():
    SQLModel.metadata.create_all(async_engine)
    
        
        
        
router = FastAPI()


@router.on_event('startup')
def on_startup():
    create_db_and_tables()
    
    
@router.post("/teams/", response_model=TeamRead)
async def create_team(*, session: Session = Depends(db_session), team: TeamCreate):
    with Session(async_engine) as session:
        db_team = Team.from_orm(team)

        session.add(db_team)
        await session.commit()
        await session.refresh(db_team)
        
        return db_team
        
        
@router.get("/teams/", response_model=List[TeamRead])
async def read_teams(*, session: Session = Depends(db_session)):
    with Session(async_engine) as session:
        teams = await session.exec(select(Team))
        teamss = teams.all()
        if not teamss:
            raise HTTPException(status_code=404, detail="No Data")
        
        return teamss
    
    
@router.get("/teams/{team_id}", response_model=TeamRead)
async def read_team(*, session: Session = Depends(db_session), team_id: int):
    with Session(async_engine) as session:
        teams  = await session.get(Team, team_id)
        
        if not teams:
            raise HTTPException(status_code=404, detail="Team Not Found")
        
        return teams
    
    
@router.patch("/teams/{team_id}", response_model=TeamRead)
async def update_team(*, session: Session = Depends(db_session), team_id: int, team: TeamUpdate):
    with Session(async_engine) as session:
        db_team = await session.get(Team, team_id)
        
        if not db_team:
            raise HTTPException(status_code=404, detail="Team Not Found")
    
        team_data = team.dict(exclude_unset=True)
        
        for key,value in team_data.items():
            setattr (db_team, key, value)
            
        session.add(db_team)
        await session.commit()
        await session.refresh(db_team)
        
        return db_team
    
    
@router.delete("/teams/{team_id}")
async def delete_team(*, session: Session = Depends(db_session), team_id: int):
    with Session(async_engine) as session:
        db_team = await session.get(Team, team_id)
        
        if not db_team:
            raise HTTPException(status_code=404, detail="Team Not Found")
        
        session.delete(db_team)
        await session.commit()
        
        return {"Deleted": True}


