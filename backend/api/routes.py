import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from financial_data import fetch_financial_data
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


@router.get("/api/download-financial-data")
def download_financial_data(company: str):
    """Fetch financial data for a company and return the Excel file as a stream."""
    try:
        # Create an in-memory buffer
        buffer = io.BytesIO()

        # Generate the Excel file in memory
        fetch_financial_data(company, buffer)

        # Reset the buffer's position to the beginning
        buffer.seek(0)

        # Return the file as a streaming response
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=financial_statements_{company}.xlsx"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))