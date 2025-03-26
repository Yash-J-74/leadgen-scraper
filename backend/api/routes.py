from fastapi import APIRouter, HTTPException
from competitor_finder import find_competitors, fetch_competitors
from scraper import scrape_business, scrape_multiple_businesses

router = APIRouter()

@router.get("/api/business-details")
def get_business_details(query: str, location: str):
    """
    Endpoint to scrape Google Maps for business details.
    """
    try:
        result = scrape_business(query, location)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return {"message": "Business details retrieved successfully", "data": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/businesses-by-category")
def get_businesses_by_category(query: str, location: str):
    """
    Endpoint to scrape Google Maps for businesses by category.
    """
    try:
        result = scrape_multiple_businesses(query, location)
        if not result:
            raise HTTPException(status_code=404, detail="No businesses found.")
        return {"message": "Businesses retrieved successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/get-competitors")
def get_competitors(query: str, location: str):
    """
    Endpoint to find competitors for a given query and location.
    """
    try:
        result = fetch_competitors(query, location)
        if not result:
            raise HTTPException(status_code=404, detail="No competitors found.")
        return {"message": "Competitors retrieved successfully", "data": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
