from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

MONGO_URI = "mongodb+srv://dylanwinter27:5bIDbHGPStLTjgBi@tp3.kuv09.mongodb.net/?retryWrites=true&w=majority&appName=TP3"
client = AsyncIOMotorClient(MONGO_URI)
db = client["voitures_db"]

from pydantic import BaseModel
from typing import List

class Vendeur(BaseModel):
    nom: str
    courriel: str
    proprietaire: str

class Offre(BaseModel):
    prix: int
    annee: int
    km: int
    transmission: str
    image_url: str
    modele: str
    marque: str
    posted_by_me: bool = False
    vendeur: Vendeur

@app.get("/offres", response_model=List[Offre])
async def get_offres():
    offres = await db.offres.find().to_list(100)
    return offres

@app.post("/offres")
async def ajouter_offre(offre: Offre):
    result = await db.offres.insert_one(offre.dict())
    return {"message": "Offre ajoutée", "id": str(result.inserted_id)}

@app.get("/marques")
async def get_marques():
    marques = await db.offres.distinct("marque")
    return marques

@app.get("/modeles/{marque}")
async def get_modeles(marque: str):
    modeles = await db.offres.distinct("modele", {"marque": marque})
    if not modeles:
        raise HTTPException(status_code=404, detail="Aucun modèle trouvé pour cette marque")
    return modeles
