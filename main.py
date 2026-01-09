from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from database import engine, Base, get_db
from models import User, Event, Registration, Announcement
from schemas import UserCreate, LoginRequest, EventCreate, EventUpdate , AnnouncementCreate  
from security import hash_password, verify_password, create_access_token, get_current_user, require_admin 




Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


@app.post("/create-event")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    new_event = Event(
        title=event.title,
        description=event.description,
        slots=event.slots,
        created_by=admin.id
    )
    db.add(new_event)
    db.commit()
    return {"message": "Event created"}

@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@app.put("/update-event/{event_id}")
def update_event(
    event_id: int,
    event: EventUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db_event.title = event.title
    db_event.description = event.description
    db_event.slots = event.slots
    db.commit()

    return {"message": "Event updated"}

@app.delete("/delete-event/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}


@app.post("/register-event/{event_id}")
def register_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.slots <= 0:
        raise HTTPException(status_code=400, detail="Event is full")

    already = db.query(Registration).filter(
        Registration.user_id == user.id,
        Registration.event_id == event_id
    ).first()

    if already:
        raise HTTPException(status_code=400, detail="Already registered")

    ticket = str(uuid.uuid4())

    registration = Registration(
        user_id=user.id,
        event_id=event_id,
        ticket_code=ticket
    )

    event.slots -= 1

    db.add(registration)
    db.commit()

    return {
        "message": "Registered successfully",
        "ticket": ticket
    }

@app.post("/events/{event_id}/announcements")
def create_announcement(
    event_id: int,
    announcement: AnnouncementCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
   
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    
    new_announcement = Announcement(
        event_id=event_id,
        message=announcement.message
    )

    
    db.add(new_announcement)
    db.commit()

    return {"message": "Announcement created successfully"}

@app.get("/events/{event_id}/announcements")
def get_announcement(
    event_id: int,
    db: Session = Depends(get_db),
):

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    

    announcements = db.query(Announcement).filter(Announcement.event_id == event_id).all()
    
    return announcements
